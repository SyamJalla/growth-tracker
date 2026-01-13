import React, { useState, useEffect } from 'react';
import {
    View,
    ScrollView,
    StyleSheet,
    RefreshControl,
    Dimensions,
    Text,
    ActivityIndicator,
} from 'react-native';
import { Card, Title, Paragraph } from 'react-native-paper';
import { LineChart } from 'react-native-chart-kit';
import { dashboardApi } from '../services/api';
import KPICard from '../components/KPICard';
import ErrorMessage from '../components/ErrorMessage';

const screenWidth = Dimensions.get('window').width;

export default function DashboardScreen() {
    const [kpis, setKpis] = useState(null);
    const [weeklyProgress, setWeeklyProgress] = useState(null);
    const [trends, setTrends] = useState(null);
    const [loading, setLoading] = useState(true);
    const [refreshing, setRefreshing] = useState(false);
    const [error, setError] = useState(null);

    const fetchDashboardData = async () => {
        try {
            setError(null);
            const [kpisResponse, weeklyResponse, trendsResponse] = await Promise.all([
                dashboardApi.getKPIs(),
                dashboardApi.getWeeklyProgress(),
                dashboardApi.getTrends(),
            ]);

            setKpis(kpisResponse.data);
            setWeeklyProgress(weeklyResponse.data);
            setTrends(trendsResponse.data);
        } catch (err) {
            setError(err.message || 'Failed to load dashboard data');
            console.error('Dashboard error:', err);
        } finally {
            setLoading(false);
            setRefreshing(false);
        }
    };

    useEffect(() => {
        fetchDashboardData();
    }, []);

    const onRefresh = () => {
        setRefreshing(true);
        fetchDashboardData();
    };

    if (loading) {
        return (
            <View style={styles.centerContainer}>
                <ActivityIndicator size="large" color="#2196F3" />
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
                    {kpis && (
                        <>
                            <KPICard
                                title="Workout Streak"
                                value={`${kpis.workout_streak} days`}
                                icon="fire"
                                color="#FF5722"
                            />
                            <KPICard
                                title="Smoke-Free Days"
                                value={`${kpis.smoke_free_days} days`}
                                icon="smoking-off"
                                color="#4CAF50"
                            />
                            <KPICard
                                title="Total Workouts"
                                value={kpis.total_workouts}
                                icon="dumbbell"
                                color="#2196F3"
                            />
                            <KPICard
                                title="Avg Workout Time"
                                value={`${kpis.avg_workout_duration} min`}
                                icon="timer"
                                color="#9C27B0"
                            />
                        </>
                    )}
                </View>
            </View>

            {/* Weekly Progress Section */}
            {weeklyProgress && weeklyProgress.labels && weeklyProgress.labels.length > 0 && (
                <View style={styles.section}>
                    <Card style={styles.card}>
                        <Card.Content>
                            <Title>Weekly Workout Progress</Title>
                            <LineChart
                                data={{
                                    labels: weeklyProgress.labels,
                                    datasets: [{
                                        data: weeklyProgress.workouts || [0],
                                    }],
                                }}
                                width={screenWidth - 60}
                                height={220}
                                chartConfig={{
                                    backgroundColor: '#ffffff',
                                    backgroundGradientFrom: '#ffffff',
                                    backgroundGradientTo: '#ffffff',
                                    decimalPlaces: 0,
                                    color: (opacity = 1) => `rgba(33, 150, 243, ${opacity})`,
                                    labelColor: (opacity = 1) => `rgba(0, 0, 0, ${opacity})`,
                                    style: {
                                        borderRadius: 16,
                                    },
                                    propsForDots: {
                                        r: '6',
                                        strokeWidth: '2',
                                        stroke: '#2196F3',
                                    },
                                }}
                                bezier
                                style={styles.chart}
                            />
                        </Card.Content>
                    </Card>
                </View>
            )}

            {/* Trends Section */}
            {trends && (
                <View style={styles.section}>
                    <Card style={styles.card}>
                        <Card.Content>
                            <Title>Monthly Trends</Title>
                            <View style={styles.trendItem}>
                                <Paragraph>Workout Trend: {trends.workout_trend}%</Paragraph>
                                <Paragraph>Smoking Reduction: {trends.smoking_reduction}%</Paragraph>
                                <Paragraph>Consistency Score: {trends.consistency_score}%</Paragraph>
                            </View>
                        </Card.Content>
                    </Card>
                </View>
            )}
        </ScrollView>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#f5f5f5',
    },
    centerContainer: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: '#f5f5f5',
    },
    loadingText: {
        marginTop: 10,
        fontSize: 16,
        color: '#666',
    },
    section: {
        padding: 15,
    },
    sectionTitle: {
        fontSize: 20,
        fontWeight: 'bold',
        marginBottom: 10,
    },
    kpiGrid: {
        flexDirection: 'row',
        flexWrap: 'wrap',
        justifyContent: 'space-between',
    },
    card: {
        marginBottom: 15,
        elevation: 3,
    },
    chart: {
        marginVertical: 8,
        borderRadius: 16,
    },
    trendItem: {
        marginTop: 10,
    },
});
