import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Alert,
  ActivityIndicator,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Player, SimilarPlayersResponse } from '../types';
import { ApiService, handleApiError } from '../services/api';
import { theme, getPositionColor, getCompetitionColor } from '../theme';
import PlayerCard from '../components/PlayerCard';

interface PlayerDetailScreenProps {
  navigation: any;
  route: {
    params: {
      playerId: number;
    };
  };
}

export const PlayerDetailScreen: React.FC<PlayerDetailScreenProps> = ({ navigation, route }) => {
  const { playerId } = route.params;
  const [player, setPlayer] = useState<Player | null>(null);
  const [similarPlayers, setSimilarPlayers] = useState<Player[]>([]);
  const [loading, setLoading] = useState(true);
  const [loadingSimilar, setLoadingSimilar] = useState(false);

  useEffect(() => {
    loadPlayerData();
  }, [playerId]);

  const loadPlayerData = async () => {
    try {
      setLoading(true);
      const playerData = await ApiService.getPlayer(playerId);
      setPlayer(playerData);
    } catch (error) {
      Alert.alert('Error', handleApiError(error));
    } finally {
      setLoading(false);
    }
  };

  const loadSimilarPlayers = async () => {
    try {
      setLoadingSimilar(true);
      const response = await ApiService.getSimilarPlayers(playerId, 'hybrid', 5);
      setSimilarPlayers(response.similar_players);
    } catch (error) {
      Alert.alert('Error', handleApiError(error));
    } finally {
      setLoadingSimilar(false);
    }
  };

  const handleSimilarPlayerPress = (similarPlayer: Player) => {
    navigation.push('PlayerDetail', { playerId: similarPlayer.id });
  };

  const formatStat = (value: number | undefined, decimals: number = 1): string => {
    if (value === undefined || value === null) return '-';
    return value.toFixed(decimals);
  };

  const renderHeader = () => {
    if (!player) return null;

    return (
      <View style={styles.header}>
        <View style={styles.nameContainer}>
          <Text style={styles.name}>{player.name}</Text>
          <Text style={styles.age}>{player.age} years old</Text>
        </View>
        
        <View style={styles.badgesContainer}>
          <View
            style={[
              styles.positionBadge,
              { backgroundColor: getPositionColor(player.position) },
            ]}
          >
            <Text style={styles.positionText}>{player.position}</Text>
          </View>
          
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

        <Text style={styles.team}>{player.squad}</Text>
        <Text style={styles.nation}>{player.nation}</Text>
      </View>
    );
  };

  const renderStatsSection = (title: string, stats: { label: string; value: string | number }[]) => (
    <View style={styles.statsSection}>
      <Text style={styles.sectionTitle}>{title}</Text>
      <View style={styles.statsGrid}>
        {stats.map((stat, index) => (
          <View key={index} style={styles.statItem}>
            <Text style={styles.statValue}>{stat.value}</Text>
            <Text style={styles.statLabel}>{stat.label}</Text>
          </View>
        ))}
      </View>
    </View>
  );

  const renderPlayerStats = () => {
    if (!player) return null;

    const basicStats = [
      { label: 'Goals', value: player.goals },
      { label: 'Assists', value: player.assists },
      { label: 'G+A', value: player.goals_assists },
      { label: 'Apps', value: player.matches_played },
    ];

    const per90Stats = [
      { label: 'G/90', value: formatStat(player.goals_per_90) },
      { label: 'A/90', value: formatStat(player.assists_per_90) },
      { label: 'G+A/90', value: formatStat(player.goal_contribution_per_90) },
      { label: 'Min/App', value: formatStat(player.minutes_per_game) },
    ];

    const advancedStats = [
      { label: 'xG', value: formatStat(player.expected_goals) },
      { label: 'xA', value: formatStat(player.expected_assists) },
      { label: 'Shot Acc%', value: formatStat(player.shots_on_target_percentage) },
      { label: 'Pass Acc%', value: formatStat(player.pass_completion_percentage) },
    ];

    const defensiveStats = [
      { label: 'Tackles', value: player.tackles || '-' },
      { label: 'Interceptions', value: player.interceptions || '-' },
      { label: 'Blocks', value: player.blocks || '-' },
      { label: 'Dribble%', value: formatStat(player.dribble_success_percentage) },
    ];

    return (
      <View style={styles.statsContainer}>
        {renderStatsSection('Basic Stats', basicStats)}
        {renderStatsSection('Per 90 Stats', per90Stats)}
        {renderStatsSection('Advanced Stats', advancedStats)}
        {renderStatsSection('Defensive Stats', defensiveStats)}
      </View>
    );
  };

  const renderSimilarPlayers = () => (
    <View style={styles.similarSection}>
      <View style={styles.similarHeader}>
        <Text style={styles.sectionTitle}>Similar Players</Text>
        <TouchableOpacity
          style={styles.loadSimilarButton}
          onPress={loadSimilarPlayers}
          disabled={loadingSimilar}
        >
          {loadingSimilar ? (
            <ActivityIndicator size="small" color={theme.colors.surface} />
          ) : (
            <Text style={styles.loadSimilarText}>Load Similar</Text>
          )}
        </TouchableOpacity>
      </View>
      
      {similarPlayers.length > 0 ? (
        similarPlayers.map((similarPlayer) => (
          <PlayerCard
            key={similarPlayer.id}
            player={similarPlayer}
            onPress={handleSimilarPlayerPress}
            showStats={false}
          />
        ))
      ) : (
        <Text style={styles.noSimilarText}>
          Tap "Load Similar" to find players with similar playing styles
        </Text>
      )}
    </View>
  );

  if (loading) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color={theme.colors.primary} />
          <Text style={styles.loadingText}>Loading player details...</Text>
        </View>
      </SafeAreaView>
    );
  }

  if (!player) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.errorContainer}>
          <Text style={styles.errorText}>Player not found</Text>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView style={styles.scrollView}>
        {renderHeader()}
        {renderPlayerStats()}
        {renderSimilarPlayers()}
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: theme.colors.background,
  },
  scrollView: {
    flex: 1,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    fontSize: 16,
    color: theme.colors.textSecondary,
    marginTop: theme.spacing.md,
  },
  errorContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  errorText: {
    fontSize: 16,
    color: theme.colors.error,
  },
  header: {
    padding: theme.spacing.lg,
    backgroundColor: theme.colors.surface,
    alignItems: 'center',
  },
  nameContainer: {
    alignItems: 'center',
    marginBottom: theme.spacing.md,
  },
  name: {
    fontSize: 24,
    fontWeight: 'bold',
    color: theme.colors.text,
    marginBottom: theme.spacing.xs,
  },
  age: {
    fontSize: 16,
    color: theme.colors.textSecondary,
  },
  badgesContainer: {
    flexDirection: 'row',
    marginBottom: theme.spacing.md,
  },
  positionBadge: {
    paddingHorizontal: theme.spacing.md,
    paddingVertical: theme.spacing.sm,
    borderRadius: theme.borderRadius.md,
    marginRight: theme.spacing.sm,
  },
  positionText: {
    color: theme.colors.surface,
    fontSize: 14,
    fontWeight: 'bold',
  },
  competitionBadge: {
    paddingHorizontal: theme.spacing.md,
    paddingVertical: theme.spacing.sm,
    borderRadius: theme.borderRadius.md,
  },
  competitionText: {
    color: theme.colors.surface,
    fontSize: 14,
    fontWeight: 'bold',
  },
  team: {
    fontSize: 18,
    fontWeight: '600',
    color: theme.colors.text,
    marginBottom: theme.spacing.xs,
  },
  nation: {
    fontSize: 14,
    color: theme.colors.textSecondary,
  },
  statsContainer: {
    padding: theme.spacing.lg,
  },
  statsSection: {
    marginBottom: theme.spacing.xl,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: theme.colors.text,
    marginBottom: theme.spacing.md,
  },
  statsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  statItem: {
    backgroundColor: theme.colors.surface,
    padding: theme.spacing.md,
    borderRadius: theme.borderRadius.md,
    alignItems: 'center',
    flex: 0.48,
    marginBottom: theme.spacing.sm,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 1,
    },
    shadowOpacity: 0.1,
    shadowRadius: 2,
    elevation: 2,
  },
  statValue: {
    fontSize: 20,
    fontWeight: 'bold',
    color: theme.colors.primary,
    marginBottom: theme.spacing.xs,
  },
  statLabel: {
    fontSize: 12,
    color: theme.colors.textSecondary,
    textAlign: 'center',
  },
  similarSection: {
    padding: theme.spacing.lg,
  },
  similarHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: theme.spacing.md,
  },
  loadSimilarButton: {
    backgroundColor: theme.colors.secondary,
    paddingHorizontal: theme.spacing.md,
    paddingVertical: theme.spacing.sm,
    borderRadius: theme.borderRadius.md,
  },
  loadSimilarText: {
    color: theme.colors.surface,
    fontSize: 14,
    fontWeight: 'bold',
  },
  noSimilarText: {
    fontSize: 14,
    color: theme.colors.textSecondary,
    textAlign: 'center',
    fontStyle: 'italic',
  },
});

export default PlayerDetailScreen; 