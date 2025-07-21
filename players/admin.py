from django.contrib import admin
from .models import Player


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    """
    Custom admin interface for Player model.
    """
    list_display = [
        'name', 'position', 'squad', 'competition', 'nation', 'age',
        'goals', 'assists', 'matches_played', 'minutes'
    ]
    
    list_filter = [
        'position', 'competition', 'squad', 'nation', 'age',
        'goals', 'assists'
    ]
    
    search_fields = ['name', 'squad', 'nation', 'position']
    
    readonly_fields = ['created_at', 'updated_at']
    
    ordering = ['-goals', '-assists', 'name']
    
    list_per_page = 50
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'nation', 'position', 'squad', 'competition', 'age', 'born_year')
        }),
        ('Playing Time', {
            'fields': ('matches_played', 'starts', 'minutes', 'minutes_per_90')
        }),
        ('Goals & Assists', {
            'fields': ('goals', 'assists', 'goals_assists', 'goals_minus_penalties', 
                      'penalties_scored', 'penalties_attempted')
        }),
        ('Cards', {
            'fields': ('yellow_cards', 'red_cards')
        }),
        ('Advanced Stats', {
            'fields': ('expected_goals', 'expected_goals_non_penalty', 'expected_assists'),
            'classes': ('collapse',)
        }),
        ('Shooting', {
            'fields': ('shots', 'shots_on_target', 'shots_on_target_percentage', 
                      'shots_per_90', 'shots_on_target_per_90'),
            'classes': ('collapse',)
        }),
        ('Passing', {
            'fields': ('passes_completed', 'passes_attempted', 'pass_completion_percentage', 
                      'key_passes'),
            'classes': ('collapse',)
        }),
        ('Defense', {
            'fields': ('tackles', 'tackles_won', 'interceptions', 'blocks', 'clearances'),
            'classes': ('collapse',)
        }),
        ('Possession', {
            'fields': ('touches', 'dribbles_attempted', 'dribbles_successful', 
                      'dribble_success_percentage'),
            'classes': ('collapse',)
        }),
        ('Goalkeeper Stats', {
            'fields': ('goals_against', 'goals_against_per_90', 'shots_faced', 
                      'saves', 'save_percentage', 'clean_sheets'),
            'classes': ('collapse',)
        }),
        ('Performance', {
            'fields': ('progressive_carries', 'progressive_passes', 'progressive_receptions'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Optimize admin queryset."""
        return super().get_queryset(request).select_related()
