from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet, NumberFilter, CharFilter, BooleanFilter
from django.db.models import Q
from .models import Player
from .serializers import (
    PlayerListSerializer, 
    PlayerDetailSerializer, 
    PlayerStatsSerializer,
    LeaderboardSerializer
)
from .sorting import PlayerSortingManager, get_sort_options, is_valid_sort_option, apply_sorting
from .vector_search import find_similar_players


class PlayerFilter(FilterSet):
    """
    Custom filter set for advanced player filtering.
    """
    # Position filters
    position = CharFilter(field_name='position', lookup_expr='icontains')
    position_exact = CharFilter(field_name='position', lookup_expr='exact')
    
    # Competition/League filters
    competition = CharFilter(field_name='competition', lookup_expr='icontains')
    league = CharFilter(field_name='competition', lookup_expr='icontains')  # Alias
    
    # Team/Squad filters
    squad = CharFilter(field_name='squad', lookup_expr='icontains')
    team = CharFilter(field_name='squad', lookup_expr='icontains')  # Alias
    
    # Nationality filter
    nation = CharFilter(field_name='nation', lookup_expr='icontains')
    nationality = CharFilter(field_name='nation', lookup_expr='icontains')  # Alias
    
    # Age range filters
    age_min = NumberFilter(field_name='age', lookup_expr='gte')
    age_max = NumberFilter(field_name='age', lookup_expr='lte')
    
    # Goals filters
    goals_min = NumberFilter(field_name='goals', lookup_expr='gte')
    goals_max = NumberFilter(field_name='goals', lookup_expr='lte')
    
    # Assists filters
    assists_min = NumberFilter(field_name='assists', lookup_expr='gte')
    assists_max = NumberFilter(field_name='assists', lookup_expr='lte')
    
    # Minutes/Games filters
    min_matches = NumberFilter(field_name='matches_played', lookup_expr='gte')
    min_minutes = NumberFilter(field_name='minutes', lookup_expr='gte')
    
    class Meta:
        model = Player
        fields = {
            'position': ['exact', 'icontains'],
            'competition': ['exact', 'icontains'],
            'squad': ['exact', 'icontains'],
            'nation': ['exact', 'icontains'],
            'age': ['exact', 'gte', 'lte'],
            'goals': ['exact', 'gte', 'lte'],
            'assists': ['exact', 'gte', 'lte'],
            'matches_played': ['gte'],
            'minutes': ['gte'],
        }


class PlayerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for player CRUD operations with comprehensive filtering and search.
    
    Provides:
    - List view with pagination and filtering
    - Detail view for individual players
    - Search functionality
    - Custom actions for leaderboards and statistics
    """
    queryset = Player.objects.all()
    serializer_class = PlayerListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = PlayerFilter
    search_fields = ['name', 'squad', 'nation', 'position']
    
    def get_serializer_class(self):
        """
        Return different serializers based on action.
        """
        if self.action == 'retrieve':
            return PlayerDetailSerializer
        elif self.action in ['stats', 'leaderboard']:
            return PlayerStatsSerializer if self.action == 'stats' else LeaderboardSerializer
        return PlayerListSerializer
    
    def get_queryset(self):
        """
        Optionally filter queryset based on query parameters.
        """
        queryset = Player.objects.all()
        
        # Additional custom filtering logic
        top_performers = self.request.query_params.get('top_performers', None)
        if top_performers:
            queryset = queryset.filter(
                Q(goals__gte=5) | Q(assists__gte=5) | Q(goals_assists__gte=8)
            )
        
        regular_players = self.request.query_params.get('regular_players', None)
        if regular_players:
            queryset = queryset.filter(matches_played__gte=5, minutes__gte=450)
        
        # Apply custom sorting if specified
        sort_by = self.request.query_params.get('sort_by', None)
        sort_order = self.request.query_params.get('sort_order', 'desc')
        
        if sort_by and is_valid_sort_option(sort_by):
            reverse = sort_order.lower() == 'desc'
            queryset = apply_sorting(queryset, sort_by, reverse)
        else:
            # Default sorting
            queryset = queryset.order_by('-goals', '-assists')
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        Enhanced search endpoint with fuzzy matching.
        """
        query = request.query_params.get('q', '')
        if not query:
            return Response({'error': 'Search query parameter "q" is required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # Fuzzy search across multiple fields
        queryset = self.get_queryset().filter(
            Q(name__icontains=query) |
            Q(squad__icontains=query) |
            Q(nation__icontains=query) |
            Q(position__icontains=query)
        )
        
        # Apply additional filters if provided
        queryset = self.filter_queryset(queryset)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def leaderboard(self, request):
        """
        Get leaderboards for different statistics using the extensible sorting system.
        """
        stat = request.query_params.get('stat', 'goals')
        limit = min(int(request.query_params.get('limit', 50)), 100)  # Max 100
        
        # Use the sorting system to validate and get the field
        if not is_valid_sort_option(stat):
            valid_options = list(get_sort_options().keys())
            return Response(
                {'error': f'Invalid stat. Choose from: {valid_options}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Apply sorting using the extensible system
        queryset = self.filter_queryset(
            self.get_queryset().filter(matches_played__gte=3)  # Minimum games filter
        )
        queryset = apply_sorting(queryset, stat, reverse=True)[:limit]
        
        serializer = LeaderboardSerializer(queryset, many=True)
        return Response({
            'stat': stat,
            'stat_info': get_sort_options().get(stat, {}),
            'players': serializer.data,
            'total_count': queryset.count()
        })
    
    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """
        Get detailed statistics for a specific player.
        """
        player = self.get_object()
        serializer = PlayerStatsSerializer(player)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def similar(self, request, pk=None):
        """
        Get similar players using advanced vector search.
        """
        player = self.get_object()
        
        # Get parameters
        limit = min(int(request.query_params.get('limit', 10)), 20)  # Max 20
        method = request.query_params.get('method', 'hybrid')  # statistical, nlp, or hybrid
        
        # Validate method
        valid_methods = ['statistical', 'nlp', 'hybrid']
        if method not in valid_methods:
            return Response(
                {'error': f'Invalid method. Choose from: {valid_methods}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Find similar players using vector search
            similar_players = find_similar_players(player, limit, method)
            
            serializer = PlayerListSerializer(similar_players, many=True)
            return Response({
                'player': PlayerListSerializer(player).data,
                'similar_players': serializer.data,
                'method': method,
                'limit': limit,
                'total_found': len(similar_players)
            })
            
        except Exception as e:
            return Response(
                {'error': f'Error finding similar players: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def positions(self, request):
        """
        Get available positions.
        """
        positions = Player.objects.values_list('position', flat=True).distinct().order_by('position')
        return Response(list(positions))
    
    @action(detail=False, methods=['get'])
    def competitions(self, request):
        """
        Get available competitions/leagues.
        """
        competitions = Player.objects.values_list('competition', flat=True).distinct().order_by('competition')
        return Response(list(competitions))
    
    @action(detail=False, methods=['get'])
    def teams(self, request):
        """
        Get available teams/squads.
        """
        teams = Player.objects.values_list('squad', flat=True).distinct().order_by('squad')
        return Response(list(teams))
    
    @action(detail=False, methods=['get'])
    def nations(self, request):
        """
        Get available nationalities.
        """
        nations = Player.objects.values_list('nation', flat=True).distinct().order_by('nation')
        return Response(list(nations))
    
    @action(detail=False, methods=['get'])
    def sort_options(self, request):
        """
        Get all available sorting options with categories.
        """
        category = request.query_params.get('category', None)
        options = get_sort_options(category)
        
        # Group by category for better organization
        categories = {}
        for key, value in options.items():
            cat = value['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append({
                'key': key,
                'display_name': value['display_name'],
                'description': value['description']
            })
        
        return Response({
            'categories': categories,
            'all_options': options,
            'available_categories': PlayerSortingManager.get_categories()
        })
    
    @action(detail=False, methods=['get'])
    def sort_options_by_category(self, request):
        """
        Get sorting options grouped by category.
        """
        categories = PlayerSortingManager.get_categories()
        result = {}
        
        for category in categories:
            result[category] = get_sort_options(category)
        
        return Response(result)
