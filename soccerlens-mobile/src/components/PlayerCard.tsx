import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { Player } from '../types';
import { theme, getPositionColor, getCompetitionColor } from '../theme';

interface PlayerCardProps {
  player: Player;
  onPress?: (player: Player) => void;
  showStats?: boolean;
  rank?: number;
  currentSort?: string;
}

export const PlayerCard: React.FC<PlayerCardProps> = ({
  player,
  onPress,
  showStats = true,
  rank,
  currentSort,
}) => {
  const handlePress = () => {
    if (onPress) {
      onPress(player);
    }
  };

  const formatStat = (value: number | undefined, decimals: number = 1): string => {
    if (value === undefined || value === null) return '-';
    return value.toFixed(decimals);
  };

  return (
    <TouchableOpacity
      style={[styles.container, showStats && styles.containerWithStats]}
      onPress={handlePress}
      activeOpacity={0.7}
    >
      <View style={styles.header}>
        {rank && (
          <View style={styles.rankContainer}>
            <Text style={styles.rankText}>#{rank}</Text>
          </View>
        )}
        
        <View style={styles.nameContainer}>
          <Text style={styles.name} numberOfLines={1}>
            {player.name}
          </Text>
          <Text style={styles.age}>{player.age} years</Text>
        </View>

        <View style={styles.positionContainer}>
          <View
            style={[
              styles.positionBadge,
              { backgroundColor: getPositionColor(player.position) },
            ]}
          >
            <Text style={styles.positionText}>{player.position}</Text>
          </View>
        </View>
      </View>

      <View style={styles.teamContainer}>
        <Text style={styles.team} numberOfLines={1}>
          {player.squad}
        </Text>
        <View
          style={[
            styles.competitionBadge,
            { backgroundColor: getCompetitionColor(player.competition) },
          ]}
        >
          <Text style={styles.competitionText}>
            {player.competition.replace('es ', '').replace('it ', '').replace('de ', '').replace('fr ', '').replace('eng ', '')}
          </Text>
        </View>
      </View>

      {showStats && (
        <View style={styles.statsContainer}>
          {currentSort && (
            <View style={styles.currentSortContainer}>
              <Text style={styles.currentSortValue}>
                {currentSort === 'name' 
                  ? player.name 
                  : formatStat(player[currentSort as keyof Player] as number)
                }
              </Text>
              <Text style={styles.currentSortLabel}>
                {currentSort === 'name' 
                  ? 'Name' 
                  : currentSort.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
                }
              </Text>
            </View>
          )}
          <View style={styles.statRow}>
            <View style={styles.statItem}>
              <Text style={styles.statValue}>{player.goals}</Text>
              <Text style={styles.statLabel}>Goals</Text>
            </View>
            <View style={styles.statItem}>
              <Text style={styles.statValue}>{player.assists}</Text>
              <Text style={styles.statLabel}>Assists</Text>
            </View>
            <View style={styles.statItem}>
              <Text style={styles.statValue}>{player.goals_assists}</Text>
              <Text style={styles.statLabel}>G+A</Text>
            </View>
            <View style={styles.statItem}>
              <Text style={styles.statValue}>{player.matches_played}</Text>
              <Text style={styles.statLabel}>Apps</Text>
            </View>
          </View>

          <View style={styles.statRow}>
            <View style={styles.statItem}>
              <Text style={styles.statValue}>{formatStat(player.goals_per_90)}</Text>
              <Text style={styles.statLabel}>G/90</Text>
            </View>
            <View style={styles.statItem}>
              <Text style={styles.statValue}>{formatStat(player.assists_per_90)}</Text>
              <Text style={styles.statLabel}>A/90</Text>
            </View>
            <View style={styles.statItem}>
              <Text style={styles.statValue}>{formatStat(player.goal_contribution_per_90)}</Text>
              <Text style={styles.statLabel}>G+A/90</Text>
            </View>
            <View style={styles.statItem}>
              <Text style={styles.statValue}>{formatStat(player.minutes_per_game)}</Text>
              <Text style={styles.statLabel}>Min/App</Text>
            </View>
          </View>
        </View>
      )}

      {player.similarity_score !== undefined && (
        <View style={styles.similarityContainer}>
          <Text style={styles.similarityText}>
            Similarity: {(player.similarity_score * 100).toFixed(1)}%
          </Text>
        </View>
      )}
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: theme.colors.surface,
    borderRadius: theme.borderRadius.lg,
    padding: theme.spacing.md,
    marginBottom: theme.spacing.sm,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 3.84,
    elevation: 5,
  },
  containerWithStats: {
    paddingBottom: theme.spacing.lg,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: theme.spacing.sm,
  },
  rankContainer: {
    backgroundColor: theme.colors.primary,
    borderRadius: theme.borderRadius.sm,
    paddingHorizontal: theme.spacing.sm,
    paddingVertical: theme.spacing.xs,
    marginRight: theme.spacing.sm,
  },
  rankText: {
    color: theme.colors.surface,
    fontSize: 12,
    fontWeight: 'bold',
  },
  nameContainer: {
    flex: 1,
  },
  name: {
    fontSize: 16,
    fontWeight: 'bold',
    color: theme.colors.text,
    marginBottom: 2,
  },
  age: {
    fontSize: 12,
    color: theme.colors.textSecondary,
  },
  positionContainer: {
    marginLeft: theme.spacing.sm,
  },
  positionBadge: {
    paddingHorizontal: theme.spacing.sm,
    paddingVertical: theme.spacing.xs,
    borderRadius: theme.borderRadius.sm,
  },
  positionText: {
    color: theme.colors.surface,
    fontSize: 10,
    fontWeight: 'bold',
  },
  teamContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: theme.spacing.md,
  },
  team: {
    fontSize: 14,
    color: theme.colors.text,
    fontWeight: '500',
    flex: 1,
  },
  competitionBadge: {
    paddingHorizontal: theme.spacing.sm,
    paddingVertical: theme.spacing.xs,
    borderRadius: theme.borderRadius.sm,
    marginLeft: theme.spacing.sm,
  },
  competitionText: {
    color: theme.colors.surface,
    fontSize: 10,
    fontWeight: 'bold',
  },
  statsContainer: {
    borderTopWidth: 1,
    borderTopColor: theme.colors.border,
    paddingTop: theme.spacing.md,
  },
  currentSortContainer: {
    alignItems: 'center',
    marginBottom: theme.spacing.md,
    paddingVertical: theme.spacing.sm,
    backgroundColor: theme.colors.primary + '10',
    borderRadius: theme.borderRadius.sm,
  },
  currentSortValue: {
    fontSize: 24,
    fontWeight: 'bold',
    color: theme.colors.primary,
    marginBottom: 2,
  },
  currentSortLabel: {
    fontSize: 12,
    color: theme.colors.textSecondary,
    textAlign: 'center',
    fontWeight: '500',
  },
  statRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: theme.spacing.sm,
  },
  statItem: {
    alignItems: 'center',
    flex: 1,
  },
  statValue: {
    fontSize: 16,
    fontWeight: 'bold',
    color: theme.colors.primary,
    marginBottom: 2,
  },
  statLabel: {
    fontSize: 10,
    color: theme.colors.textSecondary,
    textAlign: 'center',
  },
  similarityContainer: {
    marginTop: theme.spacing.sm,
    paddingTop: theme.spacing.sm,
    borderTopWidth: 1,
    borderTopColor: theme.colors.border,
  },
  similarityText: {
    fontSize: 12,
    color: theme.colors.secondary,
    textAlign: 'center',
    fontWeight: '500',
  },
});

export default PlayerCard; 