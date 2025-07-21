import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  RefreshControl,
  TouchableOpacity,
  Alert,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Player, LeaderboardResponse } from '../types';
import { ApiService, handleApiError, checkApiConnectivity } from '../services/api';
import { theme } from '../theme';
import PlayerCard from '../components/PlayerCard';

interface HomeScreenProps {
  navigation: any;
}

export const HomeScreen: React.FC<HomeScreenProps> = ({ navigation }) => {
  const [topScorers, setTopScorers] = useState<Player[]>([]);
  const [topAssists, setTopAssists] = useState<Player[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const loadData = async () => {
    try {
      setLoading(true);
      
      // Check API connectivity first
      const isConnected = await checkApiConnectivity();
      if (!isConnected) {
        Alert.alert(
          'Network Error',
          'Cannot connect to the SoccerLens API. Please check:\n\n' +
          '1. Django server is running on port 8000\n' +
          '2. Your device and computer are on the same WiFi network\n' +
          '3. Firewall is not blocking the connection\n\n' +
          'Try restarting the Django server: python manage.py runserver 0.0.0.0:8000'
        );
        return;
      }
      
      // Load top scorers
      const scorersResponse = await ApiService.getLeaderboard('goals', 5);
      setTopScorers(scorersResponse.players);
      
      // Load top assists
      const assistsResponse = await ApiService.getLeaderboard('assists', 5);
      setTopAssists(assistsResponse.players);
      
    } catch (error) {
      Alert.alert('Error', handleApiError(error));
    } finally {
      setLoading(false);
    }
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await loadData();
    setRefreshing(false);
  };

  useEffect(() => {
    loadData();
  }, []);

  const handlePlayerPress = (player: Player) => {
    navigation.navigate('PlayerDetail', { playerId: player.id });
  };

  const handleQuickAction = (action: string) => {
    switch (action) {
      case 'search':
        navigation.navigate('Search');
        break;
    }
  };

  if (loading) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.loadingContainer}>
          <Text style={styles.loadingText}>Loading SoccerLens...</Text>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView
        style={styles.scrollView}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
      >
        {/* Header */}
        <View style={styles.header}>
          <Text style={styles.title}>SoccerLens</Text>
          <Text style={styles.subtitle}>Your Ultimate Player Search</Text>
        </View>



        {/* Quick Actions */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Quick Actions</Text>
          <View style={styles.quickActions}>
            <TouchableOpacity
              style={styles.actionButton}
              onPress={() => handleQuickAction('search')}
            >
              <Text style={styles.actionButtonText}>🔍 Search</Text>
            </TouchableOpacity>

          </View>
        </View>



        {/* Top Scorers */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Top Goal Scorers</Text>
          {topScorers.map((player, index) => (
            <PlayerCard
              key={player.id}
              player={player}
              onPress={handlePlayerPress}
              rank={index + 1}
            />
          ))}
        </View>

        {/* Top Assists */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Top Assist Providers</Text>
          {topAssists.map((player, index) => (
            <PlayerCard
              key={player.id}
              player={player}
              onPress={handlePlayerPress}
              rank={index + 1}
            />
          ))}
        </View>
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
    fontSize: 18,
    color: theme.colors.textSecondary,
  },
  header: {
    padding: theme.spacing.lg,
    alignItems: 'center',
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: theme.colors.primary,
    marginBottom: theme.spacing.xs,
  },
  subtitle: {
    fontSize: 16,
    color: theme.colors.textSecondary,
  },
  section: {
    padding: theme.spacing.lg,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: theme.colors.text,
    marginBottom: theme.spacing.md,
  },
  quickActions: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  actionButton: {
    backgroundColor: theme.colors.primary,
    padding: theme.spacing.md,
    borderRadius: theme.borderRadius.md,
    flex: 0.48,
    alignItems: 'center',
  },
  actionButtonText: {
    color: theme.colors.surface,
    fontSize: 16,
    fontWeight: 'bold',
  },

});

export default HomeScreen; 