import React, { useState, useEffect } from 'react';
import {
    View,
    ScrollView,
    StyleSheet,
    RefreshControl,
    Alert,
    Text,
    ActivityIndicator,
} from 'react-native';
import { Button, FAB, Card, Title, Paragraph } from 'react-native-paper';
import { workoutApi } from '../services/api';
import WorkoutCard from '../components/WorkoutCard';
import WorkoutFormModal from '../components/WorkoutFormModal';
import ErrorMessage from '../components/ErrorMessage';

export default function WorkoutTrackerScreen() {
    const [workouts, setWorkouts] = useState([]);
    const [weeklyStats, setWeeklyStats] = useState(null);
    const [loading, setLoading] = useState(true);
    const [refreshing, setRefreshing] = useState(false);
    const [error, setError] = useState(null);
    const [modalVisible, setModalVisible] = useState(false);
    const [editingWorkout, setEditingWorkout] = useState(null);

    const fetchWorkouts = async () => {
        try {
            setError(null);
            const [workoutsResponse, dashboardResponse] = await Promise.all([
                workoutApi.getAllWorkouts(),
                workoutApi.getWeeklyStats(), // Returns dashboard data
            ]);

            console.log('📦 Workouts Response:', workoutsResponse.data);
            console.log('📦 Dashboard Response:', dashboardResponse.data);

            setWorkouts(workoutsResponse.data);

            // Dashboard returns both workout and smoking data
            if (dashboardResponse.data.workout) {
                setWeeklyStats(dashboardResponse.data.workout);
            }
        } catch (err) {
            setError(err.message || 'Failed to load workouts');
            console.error('Workout fetch error:', err);
        } finally {
            setLoading(false);
            setRefreshing(false);
        }
    };

    useEffect(() => {
        fetchWorkouts();
    }, []);

    const onRefresh = () => {
        setRefreshing(true);
        fetchWorkouts();
    };

    const handleAddWorkout = () => {
        setEditingWorkout(null);
        setModalVisible(true);
    };

    const handleEditWorkout = (workout) => {
        setEditingWorkout(workout);
        setModalVisible(true);
    };

    const handleDeleteWorkout = (workoutDate) => {
        Alert.alert(
            'Delete Workout',
            'Are you sure you want to delete this workout?',
            [
                { text: 'Cancel', style: 'cancel' },
                {
                    text: 'Delete',
                    style: 'destructive',
                    onPress: async () => {
                        try {
                            await workoutApi.deleteWorkout(workoutDate);
                            fetchWorkouts();
                        } catch (err) {
                            Alert.alert('Error', 'Failed to delete workout');
                        }
                    },
                },
            ]
        );
    };

    const handleSaveWorkout = async (workoutData) => {
        try {
            console.log('💾 Saving workout:', workoutData);
            await workoutApi.upsertWorkout(workoutData);
            setModalVisible(false);
            setEditingWorkout(null);
            fetchWorkouts();
        } catch (err) {
            console.error('Save workout error:', err);
            Alert.alert('Error', err.response?.data?.detail || 'Failed to save workout');
        }
    };

    if (loading) {
        return (
            <View style={styles.centerContainer}>
                <ActivityIndicator size="large" color="#4A90E2" />
                <Text style={styles.loadingText}>Loading workouts...</Text>
            </View>
        );
    }

    if (error) {
        return <ErrorMessage message={error} onRetry={fetchWorkouts} />;
    }

    return (
        <View style={styles.container}>
            <ScrollView
                refreshControl={
                    <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
                }
            >
                {/* Weekly Stats Card */}
                {weeklyStats && (
                    <Card style={styles.statsCard}>
                        <Card.Content>
                            <Title style={styles.cardTitle}>💪 Workout Progress</Title>
                            <View style={styles.statsRow}>
                                <View style={styles.statItem}>
                                    <Title style={styles.statValue}>
                                        {weeklyStats.current_streak || 0}
                                    </Title>
                                    <Paragraph style={styles.statLabel}>Current Streak</Paragraph>
                                </View>
                                <View style={styles.statItem}>
                                    <Title style={styles.statValue}>
                                        {weeklyStats.total_workout_days || 0}
                                    </Title>
                                    <Paragraph style={styles.statLabel}>Total Workouts</Paragraph>
                                </View>
                                <View style={styles.statItem}>
                                    <Title style={styles.statValue}>
                                        {weeklyStats.average_duration ? Math.round(weeklyStats.average_duration) : 0}
                                    </Title>
                                    <Paragraph style={styles.statLabel}>Avg Duration (min)</Paragraph>
                                </View>
                            </View>
                            <View style={styles.additionalStats}>
                                <View style={styles.additionalStatItem}>
                                    <Text style={styles.additionalStatLabel}>Success Rate: </Text>
                                    <Text style={styles.additionalStatValue}>
                                        {weeklyStats.workout_percentage || 0}%
                                    </Text>
                                </View>
                                <View style={styles.additionalStatItem}>
                                    <Text style={styles.additionalStatLabel}>Most Common: </Text>
                                    <Text style={styles.additionalStatValue}>
                                        {weeklyStats.most_common_type || 'N/A'}
                                    </Text>
                                </View>
                            </View>
                        </Card.Content>
                    </Card>
                )}

                {/* Workouts List */}
                <View style={styles.listContainer}>
                    <Title style={styles.listTitle}>
                        Recent Workouts ({workouts.length})
                    </Title>
                    {workouts.length === 0 ? (
                        <Card style={styles.emptyCard}>
                            <Card.Content>
                                <Paragraph style={styles.emptyText}>
                                    💪 No workouts logged yet!{'\n'}
                                    Start tracking your fitness journey!
                                </Paragraph>
                            </Card.Content>
                        </Card>
                    ) : (
                        workouts
                            .sort((a, b) => new Date(b.date) - new Date(a.date)) // Sort by date descending
                            .map((workout) => (
                                <WorkoutCard
                                    key={workout.date}
                                    workout={workout}
                                    onEdit={() => handleEditWorkout(workout)}
                                    onDelete={() => handleDeleteWorkout(workout.date)}
                                />
                            ))
                    )}
                </View>
            </ScrollView>

            {/* Floating Action Button */}
            <FAB
                style={styles.fab}
                icon="plus"
                label="Log Workout"
                onPress={handleAddWorkout}
                color="#fff"
            />

            {/* Workout Form Modal */}
            <WorkoutFormModal
                visible={modalVisible}
                entry={editingWorkout}
                onClose={() => setModalVisible(false)}
                onSave={handleSaveWorkout}
            />
        </View>
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
    statsCard: {
        margin: 15,
        elevation: 4,
        backgroundColor: '#4A90E2',
        borderRadius: 12,
    },
    cardTitle: {
        color: '#FFFFFF',
        fontSize: 20,
        fontWeight: 'bold',
    },
    statsRow: {
        flexDirection: 'row',
        justifyContent: 'space-around',
        marginTop: 15,
        marginBottom: 10,
    },
    statItem: {
        alignItems: 'center',
    },
    statValue: {
        fontSize: 32,
        fontWeight: 'bold',
        color: '#FFFFFF',
    },
    statLabel: {
        fontSize: 12,
        color: '#FFFFFF',
        marginTop: 5,
        textAlign: 'center',
    },
    additionalStats: {
        marginTop: 15,
        paddingTop: 15,
        borderTopWidth: 1,
        borderTopColor: 'rgba(255, 255, 255, 0.3)',
    },
    additionalStatItem: {
        flexDirection: 'row',
        justifyContent: 'center',
        marginBottom: 8,
    },
    additionalStatLabel: {
        fontSize: 14,
        color: '#FFFFFF',
    },
    additionalStatValue: {
        fontSize: 14,
        fontWeight: 'bold',
        color: '#FFFFFF',
    },
    listContainer: {
        padding: 15,
    },
    listTitle: {
        fontSize: 20,
        fontWeight: 'bold',
        marginBottom: 15,
        color: '#212529',
    },
    emptyCard: {
        marginTop: 20,
        backgroundColor: '#FFFFFF',
        elevation: 2,
        borderRadius: 8,
    },
    emptyText: {
        textAlign: 'center',
        color: '#6C757D',
        fontSize: 16,
        lineHeight: 24,
    },
    fab: {
        position: 'absolute',
        right: 20,
        bottom: 20,
        backgroundColor: '#4A90E2',
    },
});
