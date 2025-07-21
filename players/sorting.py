"""
Extensible sorting system for player statistics.
Makes it easy to add new sort options without breaking existing functionality.
"""

from django.db.models import F, Q, Case, When, Value, FloatField
from django.db.models.functions import Coalesce
from typing import Dict, List, Tuple, Optional, Any


class PlayerSortingManager:
    """
    Manages all available sorting options for players.
    Easy to extend with new sorting criteria.
    """
    
    # Define all available sorting options with their display names and field mappings
    SORT_OPTIONS = {
        # Basic info
        'name': {
            'display_name': 'Name (A-Z)',
            'field': 'last_name',
            'description': 'Sort by last name alphabetically',
            'category': 'basic'
        },
        # Basic stats
        'goals': {
            'display_name': 'Goals',
            'field': 'goals',
            'description': 'Total goals scored',
            'category': 'attacking'
        },
        'assists': {
            'display_name': 'Assists', 
            'field': 'assists',
            'description': 'Total assists provided',
            'category': 'attacking'
        },
        'goals_assists': {
            'display_name': 'Goals + Assists',
            'field': 'goals_assists', 
            'description': 'Combined goals and assists',
            'category': 'attacking'
        },
        'goals_per_90': {
            'display_name': 'Goals per 90',
            'field': 'goals_per_90',
            'description': 'Goals scored per 90 minutes',
            'category': 'attacking'
        },
        'assists_per_90': {
            'display_name': 'Assists per 90',
            'field': 'assists_per_90',
            'description': 'Assists per 90 minutes',
            'category': 'attacking'
        },
        'goal_contribution_per_90': {
            'display_name': 'Goal Contributions per 90',
            'field': 'goal_contribution_per_90',
            'description': 'Goals + assists per 90 minutes',
            'category': 'attacking'
        },
        
        # Advanced attacking stats
        'expected_goals': {
            'display_name': 'Expected Goals (xG)',
            'field': 'expected_goals',
            'description': 'Expected goals based on shot quality',
            'category': 'advanced_attacking'
        },
        'expected_assists': {
            'display_name': 'Expected Assists (xA)',
            'field': 'expected_assists',
            'description': 'Expected assists based on pass quality',
            'category': 'advanced_attacking'
        },
        'shots_on_target_percentage': {
            'display_name': 'Shot Accuracy %',
            'field': 'shots_on_target_percentage',
            'description': 'Percentage of shots on target',
            'category': 'shooting'
        },
        
        # Passing stats
        'pass_completion_percentage': {
            'display_name': 'Pass Accuracy %',
            'field': 'pass_completion_percentage',
            'description': 'Pass completion percentage',
            'category': 'passing'
        },
        'key_passes': {
            'display_name': 'Key Passes',
            'field': 'key_passes',
            'description': 'Passes leading to shots',
            'category': 'passing'
        },
        
        # Defensive stats
        'tackles': {
            'display_name': 'Tackles',
            'field': 'tackles',
            'description': 'Total tackles made',
            'category': 'defensive'
        },
        'interceptions': {
            'display_name': 'Interceptions',
            'field': 'interceptions',
            'description': 'Total interceptions',
            'category': 'defensive'
        },
        'blocks': {
            'display_name': 'Blocks',
            'field': 'blocks',
            'description': 'Total blocks',
            'category': 'defensive'
        },
        
        # Possession stats
        'dribble_success_percentage': {
            'display_name': 'Dribble Success %',
            'field': 'dribble_success_percentage',
            'description': 'Successful dribble percentage',
            'category': 'possession'
        },
        'progressive_carries': {
            'display_name': 'Progressive Carries',
            'field': 'progressive_carries',
            'description': 'Carries that advance the ball',
            'category': 'possession'
        },
        'progressive_passes': {
            'display_name': 'Progressive Passes',
            'field': 'progressive_passes',
            'description': 'Passes that advance the ball',
            'category': 'possession'
        },
        
        # Goalkeeper stats
        'save_percentage': {
            'display_name': 'Save %',
            'field': 'save_percentage',
            'description': 'Save percentage (goalkeepers only)',
            'category': 'goalkeeper'
        },
        'clean_sheets': {
            'display_name': 'Clean Sheets',
            'field': 'clean_sheets',
            'description': 'Clean sheets kept (goalkeepers only)',
            'category': 'goalkeeper'
        },
        'goals_against_per_90': {
            'display_name': 'Goals Against per 90',
            'field': 'goals_against_per_90',
            'description': 'Goals conceded per 90 (goalkeepers only)',
            'category': 'goalkeeper'
        },
        
        # Playing time
        'matches_played': {
            'display_name': 'Matches Played',
            'field': 'matches_played',
            'description': 'Total matches played',
            'category': 'playing_time'
        },
        'minutes': {
            'display_name': 'Minutes Played',
            'field': 'minutes',
            'description': 'Total minutes played',
            'category': 'playing_time'
        },
        'minutes_per_game': {
            'display_name': 'Minutes per Game',
            'field': 'minutes_per_game',
            'description': 'Average minutes per match',
            'category': 'playing_time'
        },
        
        # Discipline
        'yellow_cards': {
            'display_name': 'Yellow Cards',
            'field': 'yellow_cards',
            'description': 'Total yellow cards',
            'category': 'discipline'
        },
        'red_cards': {
            'display_name': 'Red Cards',
            'field': 'red_cards',
            'description': 'Total red cards',
            'category': 'discipline'
        },
        

        'age': {
            'display_name': 'Age',
            'field': 'age',
            'description': 'Player age',
            'category': 'basic'
        },

    }
    
    @classmethod
    def get_sort_options(cls, category: Optional[str] = None) -> Dict[str, Dict]:
        """
        Get available sorting options, optionally filtered by category.
        
        Args:
            category: Optional category filter (e.g., 'attacking', 'defensive')
            
        Returns:
            Dictionary of sort options
        """
        if category:
            return {
                key: value for key, value in cls.SORT_OPTIONS.items()
                if value['category'] == category
            }
        return cls.SORT_OPTIONS
    
    @classmethod
    def get_categories(cls) -> List[str]:
        """
        Get all available categories for sorting.
        
        Returns:
            List of category names
        """
        return list(set(option['category'] for option in cls.SORT_OPTIONS.values()))
    
    @classmethod
    def is_valid_sort_option(cls, sort_key: str) -> bool:
        """
        Check if a sort option is valid.
        
        Args:
            sort_key: The sort option key to validate
            
        Returns:
            True if valid, False otherwise
        """
        return sort_key in cls.SORT_OPTIONS
    
    @classmethod
    def get_sort_field(cls, sort_key: str) -> str:
        """
        Get the database field name for a sort option.
        
        Args:
            sort_key: The sort option key
            
        Returns:
            Database field name
            
        Raises:
            ValueError: If sort_key is invalid
        """
        if not cls.is_valid_sort_option(sort_key):
            raise ValueError(f"Invalid sort option: {sort_key}")
        
        return cls.SORT_OPTIONS[sort_key]['field']
    
    @classmethod
    def apply_sorting(cls, queryset, sort_key: str, reverse: bool = False) -> Any:
        """
        Apply sorting to a queryset.
        
        Args:
            queryset: Django queryset to sort
            sort_key: Sort option key
            reverse: Whether to reverse the sort order
            
        Returns:
            Sorted queryset
            
        Raises:
            ValueError: If sort_key is invalid
        """
        if not cls.is_valid_sort_option(sort_key):
            raise ValueError(f"Invalid sort option: {sort_key}")
        
        field = cls.get_sort_field(sort_key)
        
        # Handle special cases for calculated fields
        if field in ['goals_per_90', 'assists_per_90', 'goal_contribution_per_90', 'minutes_per_game']:
            # These are calculated properties, need special handling
            return cls._apply_calculated_sort(queryset, field, reverse)
        
        # Standard field sorting
        if reverse:
            return queryset.order_by(f'-{field}')
        else:
            return queryset.order_by(field)
    
    @classmethod
    def _apply_calculated_sort(cls, queryset, field: str, reverse: bool) -> Any:
        """
        Apply sorting for calculated fields that aren't in the database.
        
        Args:
            queryset: Django queryset
            field: Calculated field name
            reverse: Whether to reverse sort order
            
        Returns:
            Sorted queryset
        """
        # For calculated fields, we need to annotate them first
        if field == 'goals_per_90':
            queryset = queryset.annotate(
                goals_per_90_calc=Case(
                    When(minutes_per_90__gt=0, 
                         then=F('goals') / F('minutes_per_90')),
                    default=Value(0.0),
                    output_field=FloatField()
                )
            )
            sort_field = 'goals_per_90_calc'
        elif field == 'assists_per_90':
            queryset = queryset.annotate(
                assists_per_90_calc=Case(
                    When(minutes_per_90__gt=0, 
                         then=F('assists') / F('minutes_per_90')),
                    default=Value(0.0),
                    output_field=FloatField()
                )
            )
            sort_field = 'assists_per_90_calc'
        elif field == 'goal_contribution_per_90':
            queryset = queryset.annotate(
                goal_contribution_per_90_calc=Case(
                    When(minutes_per_90__gt=0, 
                         then=F('goals_assists') / F('minutes_per_90')),
                    default=Value(0.0),
                    output_field=FloatField()
                )
            )
            sort_field = 'goal_contribution_per_90_calc'
        elif field == 'minutes_per_game':
            queryset = queryset.annotate(
                minutes_per_game_calc=Case(
                    When(matches_played__gt=0, 
                         then=F('minutes') / F('matches_played')),
                    default=Value(0.0),
                    output_field=FloatField()
                )
            )
            sort_field = 'minutes_per_game_calc'
        else:
            # Fallback to original field
            sort_field = field
        
        if reverse:
            return queryset.order_by(f'-{sort_field}')
        else:
            return queryset.order_by(sort_field)
    
    @classmethod
    def add_sort_option(cls, key: str, display_name: str, field: str, 
                       description: str, category: str) -> None:
        """
        Add a new sort option dynamically.
        
        Args:
            key: Unique key for the sort option
            display_name: Human-readable name
            field: Database field name
            description: Description of what this sorts by
            category: Category for grouping
        """
        cls.SORT_OPTIONS[key] = {
            'display_name': display_name,
            'field': field,
            'description': description,
            'category': category
        }
    
    @classmethod
    def remove_sort_option(cls, key: str) -> bool:
        """
        Remove a sort option.
        
        Args:
            key: Sort option key to remove
            
        Returns:
            True if removed, False if not found
        """
        if key in cls.SORT_OPTIONS:
            del cls.SORT_OPTIONS[key]
            return True
        return False


# Convenience functions for easy access
def get_sort_options(category: Optional[str] = None) -> Dict[str, Dict]:
    """Get available sorting options."""
    return PlayerSortingManager.get_sort_options(category)

def is_valid_sort_option(sort_key: str) -> bool:
    """Check if a sort option is valid."""
    return PlayerSortingManager.is_valid_sort_option(sort_key)

def apply_sorting(queryset, sort_key: str, reverse: bool = False) -> Any:
    """Apply sorting to a queryset."""
    return PlayerSortingManager.apply_sorting(queryset, sort_key, reverse)

def add_sort_option(key: str, display_name: str, field: str, 
                   description: str, category: str) -> None:
    """Add a new sort option."""
    PlayerSortingManager.add_sort_option(key, display_name, field, description, category) 