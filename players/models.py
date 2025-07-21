from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
import numpy as np


class Player(models.Model):
    """
    Player model representing soccer players from top European leagues.
    Based on 2024-2025 season data.
    """
    
    # Basic Information
    rank = models.IntegerField(null=True, blank=True, help_text="Player ranking")
    name = models.CharField(max_length=100, db_index=True, help_text="Player name")
    last_name = models.CharField(max_length=50, db_index=True, null=True, blank=True, help_text="Player last name for sorting")
    nation = models.CharField(max_length=50, db_index=True, help_text="Player nationality")
    position = models.CharField(max_length=20, db_index=True, help_text="Player position (e.g., FW, MF, DF, GK)")
    squad = models.CharField(max_length=50, db_index=True, help_text="Current club/team")
    competition = models.CharField(max_length=50, db_index=True, help_text="League competition")
    age = models.FloatField(validators=[MinValueValidator(15.0), MaxValueValidator(45.0)], db_index=True, help_text="Player age")
    born_year = models.IntegerField(validators=[MinValueValidator(1960), MaxValueValidator(2010)], help_text="Birth year")
    
    # Playing Time Statistics
    matches_played = models.IntegerField(default=0, help_text="Matches played")
    starts = models.IntegerField(default=0, help_text="Matches started")
    minutes = models.IntegerField(default=0, help_text="Total minutes played")
    minutes_per_90 = models.FloatField(default=0.0, help_text="90-minute periods played")
    
    # Goal and Assist Statistics
    goals = models.IntegerField(default=0, db_index=True, help_text="Goals scored")
    assists = models.IntegerField(default=0, db_index=True, help_text="Assists")
    goals_assists = models.IntegerField(default=0, help_text="Goals + Assists")
    goals_minus_penalties = models.IntegerField(default=0, help_text="Goals excluding penalties")
    penalties_scored = models.IntegerField(default=0, help_text="Penalty goals")
    penalties_attempted = models.IntegerField(default=0, help_text="Penalty attempts")
    
    # Card Statistics
    yellow_cards = models.IntegerField(default=0, help_text="Yellow cards")
    red_cards = models.IntegerField(default=0, help_text="Red cards")
    
    # Advanced Statistics
    expected_goals = models.FloatField(default=0.0, help_text="Expected goals (xG)")
    expected_goals_non_penalty = models.FloatField(default=0.0, help_text="Non-penalty expected goals")
    expected_assists = models.FloatField(default=0.0, help_text="Expected assists (xAG)")
    
    # Shooting Statistics
    shots = models.IntegerField(default=0, help_text="Total shots")
    shots_on_target = models.IntegerField(default=0, help_text="Shots on target")
    shots_on_target_percentage = models.FloatField(default=0.0, help_text="Shot accuracy %")
    shots_per_90 = models.FloatField(default=0.0, help_text="Shots per 90 minutes")
    shots_on_target_per_90 = models.FloatField(default=0.0, help_text="Shots on target per 90")
    
    # Passing Statistics
    passes_completed = models.IntegerField(default=0, help_text="Passes completed")
    passes_attempted = models.IntegerField(default=0, help_text="Passes attempted")
    pass_completion_percentage = models.FloatField(default=0.0, help_text="Pass completion %")
    key_passes = models.IntegerField(default=0, help_text="Key passes")
    
    # Defensive Statistics
    tackles = models.IntegerField(default=0, help_text="Tackles")
    tackles_won = models.IntegerField(default=0, help_text="Tackles won")
    interceptions = models.IntegerField(default=0, help_text="Interceptions")
    blocks = models.IntegerField(default=0, help_text="Blocks")
    clearances = models.IntegerField(default=0, help_text="Clearances")
    
    # Possession Statistics
    touches = models.IntegerField(default=0, help_text="Total touches")
    dribbles_attempted = models.IntegerField(default=0, help_text="Dribbles attempted")
    dribbles_successful = models.IntegerField(default=0, help_text="Successful dribbles")
    dribble_success_percentage = models.FloatField(default=0.0, help_text="Dribble success %")
    
    # Goalkeeper Statistics (only relevant for GKs)
    goals_against = models.FloatField(null=True, blank=True, help_text="Goals against (GK)")
    goals_against_per_90 = models.FloatField(null=True, blank=True, help_text="Goals against per 90 (GK)")
    shots_faced = models.IntegerField(null=True, blank=True, help_text="Shots faced (GK)")
    saves = models.IntegerField(null=True, blank=True, help_text="Saves made (GK)")
    save_percentage = models.FloatField(null=True, blank=True, help_text="Save percentage (GK)")
    clean_sheets = models.IntegerField(null=True, blank=True, help_text="Clean sheets (GK)")
    
    # Performance Metrics
    progressive_carries = models.IntegerField(default=0, help_text="Progressive carries")
    progressive_passes = models.IntegerField(default=0, help_text="Progressive passes")
    progressive_receptions = models.IntegerField(default=0, help_text="Progressive pass receptions")
    
    # Phase 2: Vector Search Fields
    style_embedding = models.JSONField(null=True, blank=True, help_text="Player style embedding vector")
    style_description = models.TextField(blank=True, help_text="Generated player style description")
    similarity_score = models.FloatField(null=True, blank=True, help_text="Similarity score for search results")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'players'
        ordering = ['-goals', '-assists', 'name']
        indexes = [
            models.Index(fields=['position', 'competition']),
            models.Index(fields=['squad', 'competition']),
            models.Index(fields=['goals', 'assists']),
            models.Index(fields=['age', 'position']),
            models.Index(fields=['nation', 'position']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.squad}) - {self.position}"
    
    @property
    def goals_per_90(self):
        """Calculate goals per 90 minutes"""
        if self.minutes_per_90 > 0:
            return round(self.goals / self.minutes_per_90, 2)
        return 0.0
    
    @property
    def assists_per_90(self):
        """Calculate assists per 90 minutes"""
        if self.minutes_per_90 > 0:
            return round(self.assists / self.minutes_per_90, 2)
        return 0.0
    
    @property
    def goal_contribution_per_90(self):
        """Calculate goals + assists per 90 minutes"""
        if self.minutes_per_90 > 0:
            return round(self.goals_assists / self.minutes_per_90, 2)
        return 0.0
    
    @property
    def minutes_per_game(self):
        """Calculate average minutes per game"""
        if self.matches_played > 0:
            return round(self.minutes / self.matches_played, 1)
        return 0.0
    
    def generate_style_description(self):
        """
        Generate a text description of the player's style based on their statistics.
        This will be used for NLP-based similarity search.
        """
        description_parts = []
        
        # Position-based description
        if 'FW' in self.position:
            description_parts.append("attacking player")
            if self.goals > 10:
                description_parts.append("prolific goalscorer")
            if self.assists > 5:
                description_parts.append("creative playmaker")
        elif 'MF' in self.position:
            description_parts.append("midfielder")
            if self.assists > 5:
                description_parts.append("creative midfielder")
            if self.tackles > 20:
                description_parts.append("defensive midfielder")
        elif 'DF' in self.position:
            description_parts.append("defender")
            if self.tackles > 30:
                description_parts.append("strong tackler")
            if self.pass_completion_percentage > 85:
                description_parts.append("ball-playing defender")
        elif 'GK' in self.position:
            description_parts.append("goalkeeper")
            if self.save_percentage and self.save_percentage > 75:
                description_parts.append("reliable shot-stopper")
        
        # Performance characteristics
        if self.dribble_success_percentage > 60:
            description_parts.append("skilled dribbler")
        if self.pass_completion_percentage > 85:
            description_parts.append("accurate passer")
        if self.shots_on_target_percentage > 50:
            description_parts.append("clinical finisher")
        
        # Playing style
        if self.progressive_passes > 50:
            description_parts.append("progressive passer")
        if self.progressive_carries > 30:
            description_parts.append("ball carrier")
        
        # Age and experience
        if self.age < 23:
            description_parts.append("young talent")
        elif self.age > 30:
            description_parts.append("experienced player")
        
        return " ".join(description_parts) if description_parts else "versatile player"
    
    def get_statistics_vector(self):
        """
        Create a numerical vector representation of player statistics for similarity search.
        """
        # Normalize statistics to 0-1 range for better similarity comparison
        stats = {
            'goals_per_90': min(self.goals_per_90 / 1.0, 1.0) if self.goals_per_90 > 0 else 0,
            'assists_per_90': min(self.assists_per_90 / 0.5, 1.0) if self.assists_per_90 > 0 else 0,
            'shot_accuracy': self.shots_on_target_percentage / 100.0 if self.shots_on_target_percentage > 0 else 0,
            'pass_accuracy': self.pass_completion_percentage / 100.0 if self.pass_completion_percentage > 0 else 0,
            'dribble_success': self.dribble_success_percentage / 100.0 if self.dribble_success_percentage > 0 else 0,
            'tackles_per_90': min((self.tackles / self.minutes_per_90) / 5.0, 1.0) if self.minutes_per_90 > 0 else 0,
            'interceptions_per_90': min((self.interceptions / self.minutes_per_90) / 3.0, 1.0) if self.minutes_per_90 > 0 else 0,
            'progressive_passes_per_90': min((self.progressive_passes / self.minutes_per_90) / 10.0, 1.0) if self.minutes_per_90 > 0 else 0,
            'progressive_carries_per_90': min((self.progressive_carries / self.minutes_per_90) / 5.0, 1.0) if self.minutes_per_90 > 0 else 0,
            'age_normalized': min(self.age / 40.0, 1.0),
        }
        
        return list(stats.values())
