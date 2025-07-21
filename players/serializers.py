from rest_framework import serializers
from .models import Player


class PlayerListSerializer(serializers.ModelSerializer):
    """
    Serializer for player list view with essential fields for cards/search results.
    """
    goals_per_90 = serializers.ReadOnlyField()
    assists_per_90 = serializers.ReadOnlyField()
    goal_contribution_per_90 = serializers.ReadOnlyField()
    minutes_per_game = serializers.ReadOnlyField()
    
    class Meta:
        model = Player
        fields = [
            'id', 'name', 'position', 'squad', 'competition', 'nation', 'age',
            'goals', 'assists', 'goals_assists', 'matches_played', 'minutes',
            'yellow_cards', 'red_cards', 'goals_per_90', 'assists_per_90',
            'goal_contribution_per_90', 'minutes_per_game',
            # Advanced attacking stats
            'expected_goals', 'expected_assists', 'shots', 'shots_on_target',
            'shots_on_target_percentage', 'shots_per_90', 'shots_on_target_per_90',
            # Passing stats
            'passes_completed', 'passes_attempted', 'pass_completion_percentage',
            'key_passes', 'progressive_passes', 'progressive_receptions',
            # Defensive stats
            'tackles', 'tackles_won', 'interceptions', 'blocks', 'clearances',
            # Possession stats
            'touches', 'dribbles_attempted', 'dribbles_successful',
            'dribble_success_percentage', 'progressive_carries',
            # Goalkeeper stats
            'goals_against', 'goals_against_per_90', 'shots_faced', 'saves',
            'save_percentage', 'clean_sheets',
            # Other stats
            'starts', 'minutes_per_90', 'goals_minus_penalties',
            'penalties_scored', 'penalties_attempted'
        ]


class PlayerDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed player view with comprehensive statistics.
    """
    goals_per_90 = serializers.ReadOnlyField()
    assists_per_90 = serializers.ReadOnlyField()
    goal_contribution_per_90 = serializers.ReadOnlyField()
    minutes_per_game = serializers.ReadOnlyField()
    
    class Meta:
        model = Player
        fields = '__all__'


class PlayerStatsSerializer(serializers.ModelSerializer):
    """
    Serializer for player statistics focused on performance metrics.
    """
    goals_per_90 = serializers.ReadOnlyField()
    assists_per_90 = serializers.ReadOnlyField()
    goal_contribution_per_90 = serializers.ReadOnlyField()
    
    class Meta:
        model = Player
        fields = [
            'id', 'name', 'position', 'squad', 'competition',
            'goals', 'assists', 'goals_assists', 'expected_goals',
            'expected_assists', 'shots', 'shots_on_target',
            'shots_on_target_percentage', 'passes_completed',
            'pass_completion_percentage', 'tackles', 'interceptions',
            'goals_per_90', 'assists_per_90', 'goal_contribution_per_90'
        ]


class LeaderboardSerializer(serializers.ModelSerializer):
    """
    Serializer for leaderboard views with ranking information.
    """
    goals_per_90 = serializers.ReadOnlyField()
    assists_per_90 = serializers.ReadOnlyField()
    
    class Meta:
        model = Player
        fields = [
            'id', 'rank', 'name', 'position', 'squad', 'competition',
            'goals', 'assists', 'minutes_per_90', 'goals_per_90',
            'assists_per_90', 'expected_goals', 'shots_on_target_percentage',
            'pass_completion_percentage'
        ] 