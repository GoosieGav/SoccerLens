from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlayerViewSet

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'players', PlayerViewSet, basename='player')

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('api/', include(router.urls)),
]

# Available endpoints:
# GET /api/players/ - List all players with pagination and filtering
# GET /api/players/{id}/ - Get specific player details
# GET /api/players/search/?q=<query> - Search players
# GET /api/players/leaderboard/?stat=<stat>&limit=<limit> - Get leaderboards
# GET /api/players/{id}/stats/ - Get player statistics
# GET /api/players/{id}/similar/ - Get similar players
# GET /api/players/positions/ - Get available positions
# GET /api/players/competitions/ - Get available competitions
# GET /api/players/teams/ - Get available teams
# GET /api/players/nations/ - Get available nations 