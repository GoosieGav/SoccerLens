# ⚽ SoccerLens Mobile App

A beautiful React Native mobile app for discovering and analyzing soccer players from top European leagues.

## 🚀 Features

### ✅ Phase 3 - React Native Frontend (In Progress)

- **🏠 Home Screen** - Featured players and quick actions
- **🔍 Search Screen** - Advanced player search with filtering
- **📊 Player Cards** - Beautiful player statistics display
- **🎨 Modern UI/UX** - Clean, intuitive interface
- **📱 Responsive Design** - Works on all screen sizes
- **⚡ Real-time Search** - Instant search results
- **🔄 Pull to Refresh** - Easy data updates

### 🎯 Coming Soon

- **🏆 Leaderboards Screen** - Player rankings by various stats
- **👤 Player Detail Screen** - Comprehensive player profiles
- **🔗 Similar Players** - AI-powered player recommendations
- **⚙️ Advanced Filters** - Detailed filtering options
- **💾 Offline Support** - Cached data for offline use
- **🔔 Push Notifications** - Player news and updates

## 🛠 Tech Stack

- **React Native** with Expo
- **TypeScript** for type safety
- **React Navigation** for app navigation
- **Axios** for API communication
- **Expo Vector Icons** for beautiful icons
- **Custom Theme System** for consistent styling

## 📱 Getting Started

### Prerequisites

- Node.js (v16 or higher)
- Expo CLI
- iOS Simulator or Android Emulator (or physical device)

### Installation

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Start the development server:**
   ```bash
   npm start
   ```

3. **Run on your device:**
   - Scan the QR code with Expo Go app (iOS/Android)
   - Press `i` for iOS Simulator
   - Press `a` for Android Emulator

## 🔗 Backend Integration

This app connects to the SoccerLens Django backend API:

- **API Base URL**: `http://127.0.0.1:8000/api`
- **Features**: Player search, filtering, sorting, leaderboards
- **Data**: 2,854+ players from top European leagues

## 📊 API Endpoints Used

- `GET /api/players/` - List players with filtering & sorting
- `GET /api/players/search/` - Search players
- `GET /api/players/leaderboard/` - Get player rankings
- `GET /api/players/sort_options/` - Get sorting options
- `GET /api/players/{id}/` - Get player details
- `GET /api/players/{id}/similar/` - Get similar players

## 🎨 Design System

### Colors
- **Primary**: Deep Blue (#1E3A8A)
- **Secondary**: Bright Blue (#3B82F6)
- **Background**: Light Gray (#F8FAFC)
- **Surface**: White (#FFFFFF)

### Position Colors
- **Forwards**: Red (#EF4444)
- **Midfielders**: Blue (#3B82F6)
- **Defenders**: Green (#10B981)
- **Goalkeepers**: Purple (#8B5CF6)

## 📱 Screenshots

*Screenshots will be added as the app develops*

## 🚧 Development Status

### ✅ Completed
- [x] Project setup with Expo
- [x] Navigation structure
- [x] Theme system
- [x] API service layer
- [x] Player card component
- [x] Home screen
- [x] Search screen (basic)

### 🔄 In Progress
- [ ] Player detail screen
- [ ] Leaderboards screen
- [ ] Advanced filtering
- [ ] Similar players feature

### 📋 Planned
- [ ] Offline caching
- [ ] Push notifications
- [ ] User profiles
- [ ] Social features
- [ ] Performance optimization

## 🐛 Known Issues

- Backend connection requires local Django server running
- Some screens are placeholders (Leaderboards, Profile)
- Advanced filtering UI not yet implemented

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is part of the SoccerLens application suite.

---

**SoccerLens Mobile** - Your Ultimate Player Search Experience! ⚽📱 