"""
URL configuration for soccerlens_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request, format=None):
    """
    API root view providing links to available endpoints.
    """
    return Response({
        'message': 'Welcome to SoccerLens API',
        'version': '1.0',
        'endpoints': {
            'players': reverse('player-list', request=request, format=format),
            'admin': '/admin/',
        },
        'documentation': {
            'players_list': '/api/players/ - List all players with filtering and search',
            'player_detail': '/api/players/{id}/ - Get specific player details',
            'player_search': '/api/players/search/?q=<query> - Search players',
            'leaderboards': '/api/players/leaderboard/?stat=<stat> - Get player leaderboards',
            'similar_players': '/api/players/{id}/similar/ - Get similar players',
            'positions': '/api/players/positions/ - Get available positions',
            'competitions': '/api/players/competitions/ - Get available leagues',
            'teams': '/api/players/teams/ - Get available teams',
            'nations': '/api/players/nations/ - Get available nationalities',
        }
    })


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', api_root, name='api-root'),
    path('', include('players.urls')),
]
