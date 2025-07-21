// Player types
export interface Player {
  id: number;
  name: string;
  position: string;
  squad: string;
  competition: string;
  nation: string;
  age: number;
  goals: number;
  assists: number;
  goals_assists: number;
  matches_played: number;
  minutes: number;
  yellow_cards: number;
  red_cards: number;
  goals_per_90: number;
  assists_per_90: number;
  goal_contribution_per_90: number;
  minutes_per_game: number;
  expected_goals?: number;
  expected_assists?: number;
  shots_on_target_percentage?: number;
  pass_completion_percentage?: number;
  tackles?: number;
  interceptions?: number;
  blocks?: number;
  dribble_success_percentage?: number;
  progressive_carries?: number;
  progressive_passes?: number;
  save_percentage?: number;
  clean_sheets?: number;
  goals_against_per_90?: number;
  style_description?: string;
  similarity_score?: number;
}

// API Response types
export interface ApiResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface LeaderboardResponse {
  stat: string;
  stat_info: {
    display_name: string;
    field: string;
    description: string;
    category: string;
  };
  players: Player[];
  total_count: number;
}

export interface SimilarPlayersResponse {
  player: Player;
  similar_players: Player[];
  method: string;
  limit: number;
  total_found: number;
}

// Sorting types
export interface SortOption {
  key: string;
  display_name: string;
  description: string;
  category: string;
}

export interface SortOptionsResponse {
  categories: {
    [category: string]: SortOption[];
  };
  all_options: {
    [key: string]: SortOption;
  };
  available_categories: string[];
}

// Filter types
export interface PlayerFilters {
  position?: string;
  competition?: string;
  squad?: string;
  nation?: string;
  age_min?: number;
  age_max?: number;
  goals_min?: number;
  goals_max?: number;
  assists_min?: number;
  assists_max?: number;
  matches_played_min?: number;
  minutes_min?: number;
  regular_players?: boolean;
  top_performers?: boolean;
}

// Navigation types
export type RootStackParamList = {
  MainTabs: undefined;
  PlayerDetail: { playerId: number };
  FilterScreen: { filters: PlayerFilters; onApply: (filters: PlayerFilters) => void };
};

export type TabParamList = {
  Home: undefined;
  Search: undefined;
  Profile: undefined;
};

// Theme types
export interface Theme {
  colors: {
    primary: string;
    secondary: string;
    background: string;
    surface: string;
    text: string;
    textSecondary: string;
    border: string;
    success: string;
    warning: string;
    error: string;
  };
  spacing: {
    xs: number;
    sm: number;
    md: number;
    lg: number;
    xl: number;
  };
  borderRadius: {
    sm: number;
    md: number;
    lg: number;
  };
} 