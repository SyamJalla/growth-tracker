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
            const [workoutsResponse, statsResponse] = await Promise.all([
                workoutApi.getAllWorkouts(),
                workoutApi.getWeeklyStats(),
            ]);

            setWorkouts(workoutsResponse.data);
            setWeeklyStats(statsResponse.data);
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

    const handleDeleteWorkout = (workoutId) => {
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
                            await workoutApi.deleteWorkout(workoutId);
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
            if (editingWorkout) {
                await workoutApi.updateWorkout(editingWorkout.id, workoutData);
            } else {
                await workoutApi.logWorkout(workoutData);
            }
            setModalVisible(false);
            fetchWorkouts();
        } catch (err) {
            Alert.alert('Error', 'Failed to save workout');
        }
    };

    if (loading) {
        return (
            <View style={styles.centerContainer}>
                <ActivityIndicator size="large" color="#2196F3" />
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
                            <Title>This Week's Stats</Title>
                            <View style={styles.statsRow}>
                                <View style={styles.statItem}>
                                    <Paragraph style={styles.statLabel}>Workouts</Paragraph>
                                    <Title>{weeklyStats.total_workouts || 0}</Title>
                                </View>
                                <View style={styles.statItem}>
                                    <Paragraph style={styles.statLabel}>Total Time</Paragraph>
                                    <Title>{weeklyStats.total_duration || 0} min</Title>
                                </View>
                                <View style={styles.statItem}>
                                    <Paragraph style={styles.statLabel}>Avg Duration</Paragraph>
                                    <Title>{weeklyStats.avg_duration || 0} min</Title>
                                </View>
                            </View>
                        </Card.Content>
                    </Card>
                )}

                {/* Workouts List */}
                <View style={styles.listContainer}>
                    <Title style={styles.listTitle}>Recent Workouts</Title>
                    {workouts.length === 0 ? (
                        <Card style={styles.emptyCard}>
                            <Card.Content>
                                <Paragraph style={styles.emptyText}>
                                    No workouts logged yet. Start tracking your fitness journey!
                                </Paragraph>
                            </Card.Content>
                        </Card>
                    ) : (
                        workouts.map((workout) => (
                            <WorkoutCard
                                key={workout.id}
                                workout={workout}
                                onEdit={() => handleEditWorkout(workout)}
                                onDelete={() => handleDeleteWorkout(workout.id)}
                            />
                        ))
                    )}
                </View>
            </ScrollView>

            {/* Floating Action Button */}
            <FAB
                style={styles.fab}
                icon="plus"
                onPress={handleAddWorkout}
                color="#fff"
            />

            {/* Workout Form Modal */}
            <WorkoutFormModal
                visible={modalVisible}
                workout={editingWorkout}
                onClose={() => setModalVisible(false)}
                onSave={handleSaveWorkout}
            />
        </View>
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
    statsCard: {
        margin: 15,
        elevation: 3,
    },
    statsRow: {
        flexDirection: 'row',
        justifyContent: 'space-around',
        marginTop: 10,
    },
    statItem: {
        alignItems: 'center',
    },
    statLabel: {
        fontSize: 12,
        color: '#666',
    },
    listContainer: {
        padding: 15,
    },
    listTitle: {
        fontSize: 20,
        fontWeight: 'bold',
        marginBottom: 10,
    },
    emptyCard: {
        marginTop: 20,
    },
    emptyText: {
        textAlign: 'center',
        color: '#666',
    },
    fab: {
        position: 'absolute',
        right: 20,
        bottom: 20,
        backgroundColor: '#2196F3',
    },
});
