# Growth Tracker - Frontend

React Native mobile application for tracking workouts, smoking habits, and health metrics.

## Features

- **Dashboard**: View key performance indicators (KPIs) and weekly progress charts
- **Workout Tracker**: Log and track workout sessions with duration, intensity, and notes
- **Smoking Tracker**: Monitor smoking habits with streak tracking and triggers
- **Health Status**: Check API and database health

## Tech Stack

- **React Native** with Expo
- **React Navigation** (Bottom Tabs + Stack Navigation)
- **React Native Paper** for Material Design UI components
- **Axios** for API communication
- **React Native Chart Kit** for data visualization
- **AsyncStorage** for local storage

## Prerequisites

- Node.js (v14 or higher)
- npm or yarn
- Expo CLI: `npm install -g expo-cli`
- iOS Simulator (Mac) or Android Emulator

## Installation

1. Navigate to the Frontend directory:
   ```bash
   cd Frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Configure the backend API URL:
   - Edit `src/services/config.js`
   - Update the API URL based on your environment:
     - Local: `http://localhost:8000/api`
     - Docker: `http://host.docker.internal:8000/api`
     - Production: Your production URL

## Running the App

### Start Expo Dev Server
```bash
npm start
```

### Run on iOS Simulator (Mac only)
```bash
npm run ios
```

### Run on Android Emulator
```bash
npm run android
```

### Run on Web Browser
```bash
npm run web
```

## Project Structure

```
Frontend/
├── App.js                      # Root component
├── package.json                # Dependencies
├── src/
│   ├── navigation/
│   │   └── AppNavigator.js     # Bottom tab navigation
│   ├── screens/
│   │   ├── DashboardScreen.js       # KPI dashboard
│   │   ├── WorkoutTrackerScreen.js  # Workout logging
│   │   ├── SmokingTrackerScreen.js  # Smoking tracking
│   │   └── HealthScreen.js          # System health
│   ├── components/
│   │   ├── KPICard.js               # KPI display card
│   │   ├── WorkoutCard.js           # Workout list item
│   │   ├── SmokingCard.js           # Smoking entry item
│   │   ├── WorkoutFormModal.js      # Add/edit workout form
│   │   ├── SmokingFormModal.js      # Add/edit smoking form
│   │   └── ErrorMessage.js          # Error display
│   └── services/
│       ├── api.js                   # API client with endpoints
│       └── config.js                # API configuration
```

## API Integration

The app connects to the Growth Tracker Backend API. Ensure the backend is running before using the app.

### API Endpoints Used:
- `/api/health` - Health check
- `/api/dashboard/kpis` - Dashboard KPIs
- `/api/workouts` - Workout CRUD operations
- `/api/smoking` - Smoking tracker operations

## Configuration

### Backend URL
Update in `src/services/config.js`:
```javascript
export const API_CONFIG = {
  LOCAL: 'http://localhost:8000/api',
  PRODUCTION: 'https://your-api.com/api',
};
```

### Color Theme
Primary color: `#2196F3` (Material Blue)
Can be customized in individual component style sheets.

## Features by Screen

### Dashboard
- Current workout streak
- Smoke-free days count
- Total workouts
- Average workout duration
- Weekly workout progress chart
- Monthly trends

### Workout Tracker
- Log workout sessions
- Track type, duration, intensity, calories
- View weekly statistics
- Edit/delete workouts
- Add personal notes

### Smoking Tracker
- Log smoking entries
- Track cigarettes smoked
- Monitor mood and triggers
- View current/longest streak
- Weekly statistics
- Streak achievements

### Health Status
- API health status
- Database connectivity
- System information
- Refresh functionality

## Development

### Adding New Features
1. Create screen in `src/screens/`
2. Create components in `src/components/`
3. Add API endpoints in `src/services/api.js`
4. Register screen in `src/navigation/AppNavigator.js`

### Debugging
- Use React Native Debugger
- Check Expo DevTools console
- View network requests in Chrome DevTools

## Building for Production

### Android APK
```bash
expo build:android
```

### iOS IPA
```bash
expo build:ios
```

### Web Deployment
```bash
expo build:web
```

## Troubleshooting

### Connection Issues
- Verify backend is running
- Check API URL in config.js
- Ensure device/emulator can reach backend
- For Android emulator, use `10.0.2.2:8000` instead of `localhost:8000`

### Module Not Found
```bash
npm install
expo r -c  # Clear cache and restart
```

### Build Errors
```bash
rm -rf node_modules
npm install
```

## Dependencies

See [package.json](package.json) for full list.

Key dependencies:
- expo: ~50.0.0
- react: 18.2.0
- react-native: 0.73.0
- @react-navigation/native: ^6.1.9
- react-native-paper: ^5.11.6
- axios: ^1.6.5

## License

Part of Growth Tracker project.

## Support

For issues, check:
1. Backend API is running
2. Correct API URL in config
3. All dependencies installed
4. Expo CLI is up to date
