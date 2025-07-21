import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  TextInput,
  Alert,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { PlayerFilters } from '../types';
import { ApiService, handleApiError } from '../services/api';
import { theme } from '../theme';

interface FilterScreenProps {
  navigation: any;
  route: {
    params: {
      filters: PlayerFilters;
      onApply: (filters: PlayerFilters) => void;
    };
  };
}

export const FilterScreen: React.FC<FilterScreenProps> = ({ navigation, route }) => {
  const { filters: initialFilters, onApply } = route.params;
  const [filters, setFilters] = useState<PlayerFilters>(initialFilters);
  const [positions, setPositions] = useState<string[]>([]);
  const [competitions, setCompetitions] = useState<string[]>([]);
  const [teams, setTeams] = useState<string[]>([]);
  const [nations, setNations] = useState<string[]>([]);

  useEffect(() => {
    loadFilterOptions();
  }, []);

  const loadFilterOptions = async () => {
    try {
      const [posData, compData, teamsData, nationsData] = await Promise.all([
        ApiService.getPositions(),
        ApiService.getCompetitions(),
        ApiService.getTeams(),
        ApiService.getNations(),
      ]);
      
      setPositions(posData);
      setCompetitions(compData);
      setTeams(teamsData);
      setNations(nationsData);
    } catch (error) {
      Alert.alert('Error', handleApiError(error));
    }
  };

  const handleApply = () => {
    onApply(filters);
    navigation.goBack();
  };

  const handleReset = () => {
    setFilters({});
  };

  const updateFilter = (key: keyof PlayerFilters, value: any) => {
    setFilters(prev => ({
      ...prev,
      [key]: value,
    }));
  };

  const renderPositionFilter = () => (
    <View style={styles.filterSection}>
      <Text style={styles.sectionTitle}>Position</Text>
      <View style={styles.chipContainer}>
        {positions.map((position) => (
          <TouchableOpacity
            key={position}
            style={[
              styles.chip,
              filters.position === position && styles.chipSelected,
            ]}
            onPress={() => updateFilter('position', filters.position === position ? undefined : position)}
          >
            <Text style={[
              styles.chipText,
              filters.position === position && styles.chipTextSelected,
            ]}>
              {position}
            </Text>
          </TouchableOpacity>
        ))}
      </View>
    </View>
  );

  const renderCompetitionFilter = () => (
    <View style={styles.filterSection}>
      <Text style={styles.sectionTitle}>Competition</Text>
      <View style={styles.chipContainer}>
        {competitions.slice(0, 10).map((competition) => (
          <TouchableOpacity
            key={competition}
            style={[
              styles.chip,
              filters.competition === competition && styles.chipSelected,
            ]}
            onPress={() => updateFilter('competition', filters.competition === competition ? undefined : competition)}
          >
            <Text style={[
              styles.chipText,
              filters.competition === competition && styles.chipTextSelected,
            ]}>
              {competition.replace('es ', '').replace('it ', '').replace('de ', '').replace('fr ', '').replace('eng ', '')}
            </Text>
          </TouchableOpacity>
        ))}
      </View>
    </View>
  );

  const renderAgeFilter = () => (
    <View style={styles.filterSection}>
      <Text style={styles.sectionTitle}>Age Range</Text>
      <View style={styles.rangeContainer}>
        <View style={styles.rangeInput}>
          <Text style={styles.rangeLabel}>Min Age</Text>
          <TextInput
            style={styles.input}
            placeholder="18"
            value={filters.age_min?.toString() || ''}
            onChangeText={(text) => updateFilter('age_min', text ? parseInt(text) : undefined)}
            keyboardType="numeric"
          />
        </View>
        <View style={styles.rangeInput}>
          <Text style={styles.rangeLabel}>Max Age</Text>
          <TextInput
            style={styles.input}
            placeholder="35"
            value={filters.age_max?.toString() || ''}
            onChangeText={(text) => updateFilter('age_max', text ? parseInt(text) : undefined)}
            keyboardType="numeric"
          />
        </View>
      </View>
    </View>
  );

  const renderStatsFilter = () => (
    <View style={styles.filterSection}>
      <Text style={styles.sectionTitle}>Performance Stats</Text>
      <View style={styles.statsContainer}>
        <View style={styles.statInput}>
          <Text style={styles.statLabel}>Min Goals</Text>
          <TextInput
            style={styles.input}
            placeholder="0"
            value={filters.goals_min?.toString() || ''}
            onChangeText={(text) => updateFilter('goals_min', text ? parseInt(text) : undefined)}
            keyboardType="numeric"
          />
        </View>
        <View style={styles.statInput}>
          <Text style={styles.statLabel}>Min Assists</Text>
          <TextInput
            style={styles.input}
            placeholder="0"
            value={filters.assists_min?.toString() || ''}
            onChangeText={(text) => updateFilter('assists_min', text ? parseInt(text) : undefined)}
            keyboardType="numeric"
          />
        </View>
        <View style={styles.statInput}>
          <Text style={styles.statLabel}>Min Apps</Text>
          <TextInput
            style={styles.input}
            placeholder="0"
            value={filters.matches_played_min?.toString() || ''}
            onChangeText={(text) => updateFilter('matches_played_min', text ? parseInt(text) : undefined)}
            keyboardType="numeric"
          />
        </View>
      </View>
    </View>
  );

  const renderQuickFilters = () => (
    <View style={styles.filterSection}>
      <Text style={styles.sectionTitle}>Quick Filters</Text>
      <View style={styles.quickFilterContainer}>
        <TouchableOpacity
          style={[
            styles.quickFilterButton,
            filters.top_performers && styles.quickFilterButtonSelected,
          ]}
          onPress={() => updateFilter('top_performers', !filters.top_performers)}
        >
          <Text style={[
            styles.quickFilterText,
            filters.top_performers && styles.quickFilterTextSelected,
          ]}>
            Top Performers
          </Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[
            styles.quickFilterButton,
            filters.regular_players && styles.quickFilterButtonSelected,
          ]}
          onPress={() => updateFilter('regular_players', !filters.regular_players)}
        >
          <Text style={[
            styles.quickFilterText,
            filters.regular_players && styles.quickFilterTextSelected,
          ]}>
            Regular Players
          </Text>
        </TouchableOpacity>
      </View>
    </View>
  );

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.goBack()}>
          <Text style={styles.cancelButton}>Cancel</Text>
        </TouchableOpacity>
        <Text style={styles.title}>Filters</Text>
        <TouchableOpacity onPress={handleReset}>
          <Text style={styles.resetButton}>Reset</Text>
        </TouchableOpacity>
      </View>

      <ScrollView style={styles.content}>
        {renderPositionFilter()}
        {renderCompetitionFilter()}
        {renderAgeFilter()}
        {renderStatsFilter()}
        {renderQuickFilters()}
      </ScrollView>

      <View style={styles.footer}>
        <TouchableOpacity style={styles.applyButton} onPress={handleApply}>
          <Text style={styles.applyButtonText}>Apply Filters</Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: theme.colors.background,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: theme.spacing.lg,
    backgroundColor: theme.colors.surface,
    borderBottomWidth: 1,
    borderBottomColor: theme.colors.border,
  },
  title: {
    fontSize: 18,
    fontWeight: 'bold',
    color: theme.colors.text,
  },
  cancelButton: {
    fontSize: 16,
    color: theme.colors.textSecondary,
  },
  resetButton: {
    fontSize: 16,
    color: theme.colors.primary,
  },
  content: {
    flex: 1,
  },
  filterSection: {
    padding: theme.spacing.lg,
    borderBottomWidth: 1,
    borderBottomColor: theme.colors.border,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: theme.colors.text,
    marginBottom: theme.spacing.md,
  },
  chipContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
  },
  chip: {
    backgroundColor: theme.colors.background,
    paddingHorizontal: theme.spacing.md,
    paddingVertical: theme.spacing.sm,
    borderRadius: theme.borderRadius.md,
    marginRight: theme.spacing.sm,
    marginBottom: theme.spacing.sm,
    borderWidth: 1,
    borderColor: theme.colors.border,
  },
  chipSelected: {
    backgroundColor: theme.colors.primary,
    borderColor: theme.colors.primary,
  },
  chipText: {
    fontSize: 14,
    color: theme.colors.text,
  },
  chipTextSelected: {
    color: theme.colors.surface,
    fontWeight: 'bold',
  },
  rangeContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  rangeInput: {
    flex: 0.48,
  },
  rangeLabel: {
    fontSize: 14,
    color: theme.colors.textSecondary,
    marginBottom: theme.spacing.xs,
  },
  input: {
    backgroundColor: theme.colors.surface,
    padding: theme.spacing.md,
    borderRadius: theme.borderRadius.md,
    borderWidth: 1,
    borderColor: theme.colors.border,
    fontSize: 16,
    color: theme.colors.text,
  },
  statsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  statInput: {
    flex: 0.31,
  },
  statLabel: {
    fontSize: 14,
    color: theme.colors.textSecondary,
    marginBottom: theme.spacing.xs,
  },
  quickFilterContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  quickFilterButton: {
    flex: 0.48,
    backgroundColor: theme.colors.background,
    padding: theme.spacing.md,
    borderRadius: theme.borderRadius.md,
    borderWidth: 1,
    borderColor: theme.colors.border,
    alignItems: 'center',
  },
  quickFilterButtonSelected: {
    backgroundColor: theme.colors.primary,
    borderColor: theme.colors.primary,
  },
  quickFilterText: {
    fontSize: 14,
    color: theme.colors.text,
  },
  quickFilterTextSelected: {
    color: theme.colors.surface,
    fontWeight: 'bold',
  },
  footer: {
    padding: theme.spacing.lg,
    backgroundColor: theme.colors.surface,
    borderTopWidth: 1,
    borderTopColor: theme.colors.border,
  },
  applyButton: {
    backgroundColor: theme.colors.primary,
    padding: theme.spacing.md,
    borderRadius: theme.borderRadius.md,
    alignItems: 'center',
  },
  applyButtonText: {
    color: theme.colors.surface,
    fontSize: 16,
    fontWeight: 'bold',
  },
});

export default FilterScreen; 