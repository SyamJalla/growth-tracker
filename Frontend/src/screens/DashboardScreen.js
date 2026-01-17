import React, { useState } from 'react';
import { useFocusEffect } from '@react-navigation/native';
import {
    View,
    ScrollView,
    StyleSheet,
    RefreshControl,
    Text,
    ActivityIndicator,
} from 'react-native';
import { Card, Title, Paragraph } from 'react-native-paper';
import { dashboardApi } from '../services/api';
import KPICard from '../components/KPICard';
import ErrorMessage from '../components/ErrorMessage';

export default function DashboardScreen() {
    const [dashboardData, setDashboardData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [refreshing, setRefreshing] = useState(false);
    const [error, setError] = useState(null);

    const fetchDashboardData = async () => {
        try {
            setError(null);
            const response = await dashboardApi.getDashboard();
            setDashboardData(response.data);
        } catch (err) {
            console.error('Dashboard Error:', err);
            setError(err.message || 'Failed to load dashboard data');
        } finally {
            setLoading(false);
            setRefreshing(false);
        }
    };

    useFocusEffect(
        React.useCallback(() => {
            fetchDashboardData();
        }, [])
    );

    const onRefresh = () => {
        setRefreshing(true);
        fetchDashboardData();
    };

    if (loading) {
        return (
            <View style={styles.centerContainer}>
                <ActivityIndicator size="large" color="#4A90E2" />
                <Text style={styles.loadingText}>Loading dashboard...</Text>
            </View>
        );
    }

    if (error) {
        return (
            <ErrorMessage
                message={error}
                onRetry={fetchDashboardData}
            />
        );
    }

    const workout = dashboardData?.workout || {};
    const smoking = dashboardData?.smoking || {};

    return (
        <ScrollView
            style={styles.container}
            refreshControl={
                <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
            }
        >
            {/* KPIs Section */}
            <View style={styles.section}>
                <Title style={styles.sectionTitle}>Key Performance Indicators</Title>
                <View style={styles.kpiGrid}>
                    <KPICard
                        title="Workout Streak"
                        value={`${workout.current_streak || 0} days`}
                        icon="fire"
                        color="#FF6B6B"
                    />
                    <KPICard
                        title="Smoke-Free Days"
                        value={`${smoking.current_clean_streak || 0} days`}
                        icon="smoking-off"
                        color="#51CF66"
                    />
                    <KPICard
                        title="Total Workouts"
                        value={workout.total_workout_days || 0}
                        icon="dumbbell"
                        color="#4A90E2"
                    />
                    <KPICard
                        title="Avg Workout Time"
                        value={workout.average_duration ? `${Math.round(workout.average_duration)} min` : 'N/A'}
                        icon="timer"
                        color="#9775FA"
                    />
                </View>
            </View>

            {/* Workout Statistics */}
            <View style={styles.section}>
                <Card style={styles.workoutCard}>
                    <Card.Content>
                        <Title style={styles.cardTitle}>Workout Statistics</Title>
                        <View style={styles.statRow}>
                            <View style={styles.statItem}>
                                <Text style={styles.statEmoji}>🔥</Text>
                                <Text style={styles.statLabel}>Current Streak</Text>
                                <Text style={styles.statValue}>{workout.current_streak || 0} days</Text>
                            </View>
                            <View style={styles.statItem}>
                                <Text style={styles.statEmoji}>🏆</Text>
                                <Text style={styles.statLabel}>Longest Streak</Text>
                                <Text style={styles.statValue}>{workout.longest_streak || 0} days</Text>
                            </View>
                        </View>
                        <View style={styles.statRow}>
                            <View style={styles.statItem}>
                                <Text style={styles.statEmoji}>📅</Text>
                                <Text style={styles.statLabel}>Days Tracked</Text>
                                <Text style={styles.statValue}>{workout.total_days || 0}</Text>
                            </View>
                            <View style={styles.statItem}>
                                <Text style={styles.statEmoji}>✅</Text>
                                <Text style={styles.statLabel}>Success Rate</Text>
                                <Text style={styles.statValue}>{workout.workout_percentage || 0}%</Text>
                            </View>
                        </View>
                        <View style={styles.singleStatRow}>
                            <Text style={styles.statEmoji}>💪</Text>
                            <Text style={styles.statLabel}>Most Common Type: </Text>
                            <Text style={styles.statValueInline}>{workout.most_common_type || 'N/A'}</Text>
                        </View>
                    </Card.Content>
                </Card>
            </View>

            {/* Smoking Statistics */}
            <View style={styles.section}>
                <Card style={styles.smokingCard}>
                    <Card.Content>
                        <Title style={styles.cardTitle}>Smoking Statistics</Title>
                        <View style={styles.statRow}>
                            <View style={styles.statItem}>
                                <Text style={styles.statEmoji}>✨</Text>
                                <Text style={styles.statLabel}>Clean Streak</Text>
                                <Text style={styles.statValue}>{smoking.current_clean_streak || 0} days</Text>
                            </View>
                            <View style={styles.statItem}>
                                <Text style={styles.statEmoji}>🏆</Text>
                                <Text style={styles.statLabel}>Best Streak</Text>
                                <Text style={styles.statValue}>{smoking.longest_clean_streak || 0} days</Text>
                            </View>
                        </View>
                        <View style={styles.statRow}>
                            <View style={styles.statItem}>
                                <Text style={styles.statEmoji}>⚠️</Text>
                                <Text style={styles.statLabel}>Total Relapses</Text>
                                <Text style={styles.statValue}>{smoking.total_relapses || 0}</Text>
                            </View>
                            <View style={styles.statItem}>
                                <Text style={styles.statEmoji}>🚬</Text>
                                <Text style={styles.statLabel}>Cigarettes</Text>
                                <Text style={styles.statValue}>{smoking.total_cigarettes || 0}</Text>
                            </View>
                        </View>
                        <View style={styles.singleStatRow}>
                            <Text style={styles.statEmoji}>📍</Text>
                            <Text style={styles.statLabel}>Common Location: </Text>
                            <Text style={styles.statValueInline}>{smoking.most_common_location || 'N/A'}</Text>
                        </View>
                    </Card.Content>
                </Card>
            </View>

            {/* Monthly Trends */}
            <View style={styles.section}>
                <Card style={styles.trendsCard}>
                    <Card.Content>
                        <Title style={styles.cardTitle}>Monthly Trends</Title>
                        <View style={styles.trendItem}>
                            <Text style={styles.comingSoon}>📊 Detailed trends coming soon!</Text>
                            <Text style={styles.trendFeature}>• Workout consistency over time</Text>
                            <Text style={styles.trendFeature}>• Smoking reduction progress</Text>
                            <Text style={styles.trendFeature}>• Weekly performance charts</Text>
                        </View>
                    </Card.Content>
                </Card>
            </View>

            {/* Last Updated */}
            <View style={styles.section}>
                <Text style={styles.lastUpdated}>
                    Last updated: {dashboardData?.last_updated || 'N/A'}
                </Text>
            </View>
        </ScrollView>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#F8F9FA',
    },
    centerContainer: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: '#F8F9FA',
    },
    loadingText: {
        marginTop: 10,
        fontSize: 16,
        color: '#6C757D',
    },
    section: {
        padding: 15,
    },
    sectionTitle: {
        fontSize: 22,
        fontWeight: 'bold',
        marginBottom: 15,
        color: '#212529',
    },
    kpiGrid: {
        flexDirection: 'row',
        flexWrap: 'wrap',
        justifyContent: 'space-between',
    },
    workoutCard: {
        marginBottom: 15,
        elevation: 4,
        backgroundColor: '#FFFFFF',
        borderLeftWidth: 4,
        borderLeftColor: '#4A90E2',
        borderRadius: 12,
    },
    smokingCard: {
        marginBottom: 15,
        elevation: 4,
        backgroundColor: '#FFFFFF',
        borderLeftWidth: 4,
        borderLeftColor: '#51CF66',
        borderRadius: 12,
    },
    trendsCard: {
        marginBottom: 15,
        elevation: 4,
        backgroundColor: '#FFFFFF',
        borderLeftWidth: 4,
        borderLeftColor: '#9775FA',
        borderRadius: 12,
    },
    cardTitle: {
        fontSize: 18,
        fontWeight: 'bold',
        color: '#212529',
        marginBottom: 15,
    },
    statRow: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        marginBottom: 15,
    },
    statItem: {
        flex: 1,
        alignItems: 'center',
        padding: 10,
        backgroundColor: '#F8F9FA',
        borderRadius: 8,
        marginHorizontal: 5,
    },
    statEmoji: {
        fontSize: 24,
        marginBottom: 5,
    },
    statLabel: {
        fontSize: 12,
        color: '#6C757D',
        marginBottom: 5,
        textAlign: 'center',
    },
    statValue: {
        fontSize: 18,
        fontWeight: 'bold',
        color: '#212529',
    },
    singleStatRow: {
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'center',
        padding: 10,
        backgroundColor: '#F8F9FA',
        borderRadius: 8,
    },
    statValueInline: {
        fontSize: 14,
        fontWeight: 'bold',
        color: '#4A90E2',
    },
    trendItem: {
        marginTop: 10,
    },
    comingSoon: {
        fontWeight: 'bold',
        marginBottom: 15,
        color: '#4A90E2',
        fontSize: 16,
        textAlign: 'center',
    },
    trendFeature: {
        fontSize: 14,
        color: '#6C757D',
        marginBottom: 8,
        paddingLeft: 10,
    },
    lastUpdated: {
        textAlign: 'center',
        color: '#999',
        fontSize: 12,
        marginBottom: 20,
    },
});
