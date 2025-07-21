import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TextInput,
  FlatList,
  TouchableOpacity,
  Alert,
  ActivityIndicator,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Player, PlayerFilters, SortOption } from '../types';
import { ApiService, handleApiError } from '../services/api';
import { theme } from '../theme';
import PlayerCard from '../components/PlayerCard';

interface SearchScreenProps {
  navigation: any;
}

export const SearchScreen: React.FC<SearchScreenProps> = ({ navigation }) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [players, setPlayers] = useState<Player[]>([]);
  const [loading, setLoading] = useState(false);
  const [sortOptions, setSortOptions] = useState<SortOption[]>([]);
  const [selectedSort, setSelectedSort] = useState<string>('goals');
  const [showFilters, setShowFilters] = useState(false);
  const [filters, setFilters] = useState<PlayerFilters>({});

  useEffect(() => {
    loadSortOptions();
  }, []);

  useEffect(() => {
    if (searchQuery.length > 2) {
      performSearch();
    } else if (searchQuery.length === 0) {
      loadDefaultPlayers();
    }
  }, [searchQuery, filters]);

  // Separate effect for sorting changes
  useEffect(() => {
    console.log('🔄 Sort changed to:', selectedSort);
    if (searchQuery.length === 0) {
      loadDefaultPlayers();
    } else if (searchQuery.length > 2) {
      // For search results, we'll use the main players endpoint with search filters
      // This allows us to use the sorting functionality
      performSortedSearch();
    }
  }, [selectedSort, searchQuery, filters]);

  const loadSortOptions = async () => {
    try {
      const response = await ApiService.getSortOptions();
      
      // Handle the nested structure from the API
      let options: SortOption[] = [];
      if (response.all_options) {
        // Transform the all_options object to include the key field
        options = Object.entries(response.all_options).map(([key, value]: [string, any]) => ({
          key: key,
          display_name: value.display_name,
          description: value.description,
          category: value.category
        }));
      } else if (response.categories) {
        // If categories exist, flatten them and add keys
        options = Object.entries(response.categories).flatMap(([category, categoryOptions]: [string, any]) =>
          categoryOptions.map((option: any) => ({
            key: option.key || option.field,
            display_name: option.display_name,
            description: option.description,
            category: category
          }))
        );
      } else {
        console.error('Unexpected sort options format:', response);
        return;
      }
      
      setSortOptions(options);
    } catch (error: any) {
      console.error('Error loading sort options:', error);
    }
  };

  const loadDefaultPlayers = async () => {
    try {
      setLoading(true);
      const sortOrder = selectedSort === 'name' ? 'asc' : 'desc';
      const response = await ApiService.getPlayers(filters, selectedSort, sortOrder, 1, 20);
      setPlayers(response.results);
    } catch (error) {
      Alert.alert('Error', handleApiError(error));
    } finally {
      setLoading(false);
    }
  };

  const performSearch = async () => {
    try {
      setLoading(true);
      // Use the main players endpoint with search and current sorting
      const sortOrder = selectedSort === 'name' ? 'asc' : 'desc';
      const response = await ApiService.getPlayers(filters, selectedSort, sortOrder, 1, 20, searchQuery);
      setPlayers(response.results);
    } catch (error) {
      Alert.alert('Error', handleApiError(error));
    } finally {
      setLoading(false);
    }
  };

  const performSortedSearch = async () => {
    try {
      setLoading(true);
      // Use the main players endpoint with search and sorting
      const sortOrder = selectedSort === 'name' ? 'asc' : 'desc';
      const response = await ApiService.getPlayers(filters, selectedSort, sortOrder, 1, 20, searchQuery);
      setPlayers(response.results);
    } catch (error) {
      Alert.alert('Error', handleApiError(error));
    } finally {
      setLoading(false);
    }
  };

  const handlePlayerPress = (player: Player) => {
    navigation.navigate('PlayerDetail', { playerId: player.id });
  };

  const handleSortChange = (sortKey: string) => {
    setSelectedSort(sortKey);
  };

  const handleFilterChange = (newFilters: PlayerFilters) => {
    setFilters(newFilters);
    setShowFilters(false);
  };

  const renderSortOption = ({ item }: { item: SortOption }) => {
    const sortKey = item.key || item.display_name?.toLowerCase().replace(/\s+/g, '_');
    const isSelected = selectedSort === sortKey;
    
    return (
      <TouchableOpacity
        style={[
          styles.sortOption,
          isSelected && styles.sortOptionSelected,
        ]}
        onPress={() => handleSortChange(sortKey)}
      >
        <Text
          style={[
            styles.sortOptionText,
            isSelected && styles.sortOptionTextSelected,
          ]}
        >
          {item.display_name}
        </Text>
      </TouchableOpacity>
    );
  };

  const renderPlayer = ({ item }: { item: Player }) => {
    return (
      <PlayerCard
        player={item}
        onPress={handlePlayerPress}
        showStats={true}
        currentSort={selectedSort}
      />
    );
  };

  return (
    <SafeAreaView style={styles.container}>
      {/* Search Header */}
      <View style={styles.header}>
        <Text style={styles.title}>Search Players</Text>
        
        {/* Search Input */}
        <View style={styles.searchContainer}>
          <TextInput
            style={styles.searchInput}
            placeholder="Search by name, team, or nationality..."
            value={searchQuery}
            onChangeText={setSearchQuery}
            placeholderTextColor={theme.colors.textSecondary}
          />
        </View>

        {/* Sort Options */}
        <View style={styles.sortContainer}>
          <Text style={styles.sectionTitle}>Sort by:</Text>
          <FlatList
            data={sortOptions}
            renderItem={renderSortOption}
            keyExtractor={(item) => item.key || item.display_name}
            horizontal
            showsHorizontalScrollIndicator={false}
            style={styles.sortList}
            extraData={selectedSort}
          />
        </View>

        {/* Filter Button */}
        <TouchableOpacity
          style={styles.filterButton}
          onPress={() => setShowFilters(!showFilters)}
        >
          <Text style={styles.filterButtonText}>
            {showFilters ? 'Hide Filters' : 'Show Filters'}
          </Text>
        </TouchableOpacity>
      </View>

      {/* Filters Modal */}
      {showFilters && (
        <View style={styles.filtersContainer}>
          <Text style={styles.sectionTitle}>Filters</Text>
          <TouchableOpacity
            style={styles.filterOption}
            onPress={() => navigation.navigate('FilterScreen', { filters, onApply: handleFilterChange })}
          >
            <Text style={styles.filterOptionText}>Advanced Filters</Text>
          </TouchableOpacity>
        </View>
      )}

      {/* Results */}
      <View style={styles.resultsContainer}>
        {loading ? (
          <View style={styles.loadingContainer}>
            <ActivityIndicator size="large" color={theme.colors.primary} />
            <Text style={styles.loadingText}>Searching...</Text>
          </View>
        ) : (
          <FlatList
            data={players}
            renderItem={renderPlayer}
            keyExtractor={(item) => item.id.toString()}
            showsVerticalScrollIndicator={false}
            contentContainerStyle={styles.playerList}
            extraData={selectedSort}
            key={selectedSort}
            ListEmptyComponent={
              <View style={styles.emptyContainer}>
                <Text style={styles.emptyText}>
                  {searchQuery.length > 0
                    ? 'No players found matching your search.'
                    : 'Start typing to search for players.'}
                </Text>
              </View>
            }
          />
        )}
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
    padding: theme.spacing.lg,
    backgroundColor: theme.colors.surface,
    borderBottomWidth: 1,
    borderBottomColor: theme.colors.border,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: theme.colors.text,
    marginBottom: theme.spacing.md,
  },
  searchContainer: {
    marginBottom: theme.spacing.md,
  },
  searchInput: {
    backgroundColor: theme.colors.background,
    padding: theme.spacing.md,
    borderRadius: theme.borderRadius.md,
    fontSize: 16,
    color: theme.colors.text,
    borderWidth: 1,
    borderColor: theme.colors.border,
  },
  sortContainer: {
    marginBottom: theme.spacing.md,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: theme.colors.text,
    marginBottom: theme.spacing.sm,
  },
  sortList: {
    flexGrow: 0,
  },
  sortOption: {
    backgroundColor: theme.colors.background,
    paddingHorizontal: theme.spacing.md,
    paddingVertical: theme.spacing.sm,
    borderRadius: theme.borderRadius.md,
    marginRight: theme.spacing.sm,
    borderWidth: 1,
    borderColor: theme.colors.border,
  },
  sortOptionSelected: {
    backgroundColor: theme.colors.primary,
    borderColor: theme.colors.primary,
  },
  sortOptionText: {
    fontSize: 14,
    color: theme.colors.text,
  },
  sortOptionTextSelected: {
    color: theme.colors.surface,
    fontWeight: 'bold',
  },
  filterButton: {
    backgroundColor: theme.colors.secondary,
    padding: theme.spacing.sm,
    borderRadius: theme.borderRadius.md,
    alignItems: 'center',
  },
  filterButtonText: {
    color: theme.colors.surface,
    fontSize: 14,
    fontWeight: 'bold',
  },
  filtersContainer: {
    padding: theme.spacing.lg,
    backgroundColor: theme.colors.surface,
    borderBottomWidth: 1,
    borderBottomColor: theme.colors.border,
  },
  filterOption: {
    backgroundColor: theme.colors.background,
    padding: theme.spacing.md,
    borderRadius: theme.borderRadius.md,
    borderWidth: 1,
    borderColor: theme.colors.border,
  },
  filterOptionText: {
    fontSize: 16,
    color: theme.colors.text,
    textAlign: 'center',
  },
  resultsContainer: {
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
  playerList: {
    padding: theme.spacing.lg,
  },
  emptyContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: theme.spacing.xl,
  },
  emptyText: {
    fontSize: 16,
    color: theme.colors.textSecondary,
    textAlign: 'center',
  },
});

export default SearchScreen; 