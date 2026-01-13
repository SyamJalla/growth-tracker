import React from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { MaterialCommunityIcons } from '@expo/vector-icons';

// Import screens
import DashboardScreen from '../screens/DashboardScreen';
import WorkoutTrackerScreen from '../screens/WorkoutTrackerScreen';
import SmokingTrackerScreen from '../screens/SmokingTrackerScreen';
import HealthScreen from '../screens/HealthScreen';

const Tab = createBottomTabNavigator();

export default function AppNavigator() {
    return (
        <Tab.Navigator
            screenOptions={({ route }) => ({
                tabBarIcon: ({ focused, color, size }) => {
                    let iconName;

                    if (route.name === 'Dashboard') {
                        iconName = focused ? 'view-dashboard' : 'view-dashboard-outline';
                    } else if (route.name === 'Workouts') {
                        iconName = focused ? 'dumbbell' : 'dumbbell';
                    } else if (route.name === 'Smoking') {
                        iconName = focused ? 'smoking-off' : 'smoking';
                    } else if (route.name === 'Health') {
                        iconName = focused ? 'heart-pulse' : 'heart-outline';
                    }

                    return <MaterialCommunityIcons name={iconName} size={size} color={color} />;
                },
                tabBarActiveTintColor: '#2196F3',
                tabBarInactiveTintColor: 'gray',
                headerStyle: {
                    backgroundColor: '#2196F3',
                },
                headerTintColor: '#fff',
                headerTitleStyle: {
                    fontWeight: 'bold',
                },
            })}
        >
            <Tab.Screen
                name="Dashboard"
                component={DashboardScreen}
                options={{ title: 'Growth Tracker' }}
            />
            <Tab.Screen
                name="Workouts"
                component={WorkoutTrackerScreen}
                options={{ title: 'Workout Tracker' }}
            />
            <Tab.Screen
                name="Smoking"
                component={SmokingTrackerScreen}
                options={{ title: 'Smoking Tracker' }}
            />
            <Tab.Screen
                name="Health"
                component={HealthScreen}
                options={{ title: 'Health Status' }}
            />
        </Tab.Navigator>
    );
}
