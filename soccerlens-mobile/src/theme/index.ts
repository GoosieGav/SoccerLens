import { Theme } from '../types';

export const theme: Theme = {
  colors: {
    primary: '#1E3A8A', // Deep blue
    secondary: '#3B82F6', // Bright blue
    background: '#F8FAFC', // Light gray background
    surface: '#FFFFFF', // White surface
    text: '#1F2937', // Dark gray text
    textSecondary: '#6B7280', // Medium gray secondary text
    border: '#E5E7EB', // Light gray border
    success: '#10B981', // Green
    warning: '#F59E0B', // Amber
    error: '#EF4444', // Red
  },
  spacing: {
    xs: 4,
    sm: 8,
    md: 16,
    lg: 24,
    xl: 32,
  },
  borderRadius: {
    sm: 4,
    md: 8,
    lg: 12,
  },
};

// Position colors for player cards
export const positionColors = {
  FW: '#EF4444', // Red for forwards
  MF: '#3B82F6', // Blue for midfielders
  DF: '#10B981', // Green for defenders
  GK: '#8B5CF6', // Purple for goalkeepers
};

// Competition colors
export const competitionColors = {
  'Premier League': '#37003C',
  'es La Liga': '#FF6B35',
  'it Serie A': '#008FD7',
  'de Bundesliga': '#D20515',
  'fr Ligue 1': '#091C3E',
};

// Utility functions
export const getPositionColor = (position: string): string => {
  if (position.includes('FW')) return positionColors.FW;
  if (position.includes('MF')) return positionColors.MF;
  if (position.includes('DF')) return positionColors.DF;
  if (position.includes('GK')) return positionColors.GK;
  return theme.colors.textSecondary;
};

export const getCompetitionColor = (competition: string): string => {
  return competitionColors[competition as keyof typeof competitionColors] || theme.colors.primary;
};

export default theme; 