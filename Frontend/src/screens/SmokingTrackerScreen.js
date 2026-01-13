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
import { smokingApi } from '../services/api';
import SmokingCard from '../components/SmokingCard';
import SmokingFormModal from '../components/SmokingFormModal';
import ErrorMessage from '../components/ErrorMessage';

export default function SmokingTrackerScreen() {
    const [entries, setEntries] = useState([]);
    const [streakInfo, setStreakInfo] = useState(null);
    const [weeklyStats, setWeeklyStats] = useState(null);
    const [loading, setLoading] = useState(true);
    const [refreshing, setRefreshing] = useState(false);
    const [error, setError] = useState(null);
    const [modalVisible, setModalVisible] = useState(false);
    const [editingEntry, setEditingEntry] = useState(null);

    const fetchSmokingData = async () => {
        try {
            setError(null);
            const [entriesResponse, streakResponse, statsResponse] = await Promise.all([
                smokingApi.getAllEntries(),
                smokingApi.getStreakInfo(),
                smokingApi.getWeeklyStats(),
            ]);

            setEntries(entriesResponse.data);
            setStreakInfo(streakResponse.data);
            setWeeklyStats(statsResponse.data);
        } catch (err) {
            setError(err.message || 'Failed to load smoking data');
            console.error('Smoking fetch error:', err);
        } finally {
            setLoading(false);
            setRefreshing(false);
        }
    };

    useEffect(() => {
        fetchSmokingData();
    }, []);

    const onRefresh = () => {
        setRefreshing(true);
        fetchSmokingData();
    };

    const handleAddEntry = () => {
        setEditingEntry(null);
        setModalVisible(true);
    };

    const handleEditEntry = (entry) => {
        setEditingEntry(entry);
        setModalVisible(true);
    };

    const handleDeleteEntry = (entryId) => {
        Alert.alert(
            'Delete Entry',
            'Are you sure you want to delete this entry?',
            [
                { text: 'Cancel', style: 'cancel' },
                {
                    text: 'Delete',
                    style: 'destructive',
                    onPress: async () => {
                        try {
                            await smokingApi.deleteEntry(entryId);
                            fetchSmokingData();
                        } catch (err) {
                            Alert.alert('Error', 'Failed to delete entry');
                        }
                    },
                },
            ]
        );
    };

    const handleSaveEntry = async (entryData) => {
        try {
            if (editingEntry) {
                await smokingApi.updateEntry(editingEntry.id, entryData);
            } else {
                await smokingApi.logEntry(entryData);
            }
            setModalVisible(false);
            fetchSmokingData();
        } catch (err) {
            Alert.alert('Error', 'Failed to save entry');
        }
    };

    if (loading) {
        return (
            <View style={styles.centerContainer}>
                <ActivityIndicator size="large" color="#2196F3" />
                <Text style={styles.loadingText}>Loading smoking data...</Text>
            </View>
        );
    }

    if (error) {
        return <ErrorMessage message={error} onRetry={fetchSmokingData} />;
    }

    return (
        <View style={styles.container}>
            <ScrollView
                refreshControl={
                    <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
                }
            >
                {/* Streak Info Card */}
                {streakInfo && (
                    <Card style={styles.streakCard}>
                        <Card.Content>
                            <Title>🎯 Smoke-Free Journey</Title>
                            <View style={styles.streakRow}>
                                <View style={styles.streakItem}>
                                    <Title style={styles.streakValue}>{streakInfo.current_streak || 0}</Title>
                                    <Paragraph style={styles.streakLabel}>Current Streak (days)</Paragraph>
                                </View>
                                <View style={styles.streakItem}>
                                    <Title style={styles.streakValue}>{streakInfo.longest_streak || 0}</Title>
                                    <Paragraph style={styles.streakLabel}>Longest Streak</Paragraph>
                                </View>
                            </View>
                        </Card.Content>
                    </Card>
                )}

                {/* Weekly Stats Card */}
                {weeklyStats && (
                    <Card style={styles.statsCard}>
                        <Card.Content>
                            <Title>This Week's Summary</Title>
                            <View style={styles.statsRow}>
                                <View style={styles.statItem}>
                                    <Paragraph style={styles.statLabel}>Total Smoked</Paragraph>
                                    <Title>{weeklyStats.total_smoked || 0}</Title>
                                </View>
                                <View style={styles.statItem}>
                                    <Paragraph style={styles.statLabel}>Daily Average</Paragraph>
                                    <Title>{weeklyStats.daily_average || 0}</Title>
                                </View>
                                <View style={styles.statItem}>
                                    <Paragraph style={styles.statLabel}>Entries</Paragraph>
                                    <Title>{weeklyStats.total_entries || 0}</Title>
                                </View>
                            </View>
                        </Card.Content>
                    </Card>
                )}

                {/* Entries List */}
                <View style={styles.listContainer}>
                    <Title style={styles.listTitle}>Recent Entries</Title>
                    {entries.length === 0 ? (
                        <Card style={styles.emptyCard}>
                            <Card.Content>
                                <Paragraph style={styles.emptyText}>
                                    No entries yet. Start tracking your smoke-free journey!
                                </Paragraph>
                            </Card.Content>
                        </Card>
                    ) : (
                        entries.map((entry) => (
                            <SmokingCard
                                key={entry.id}
                                entry={entry}
                                onEdit={() => handleEditEntry(entry)}
                                onDelete={() => handleDeleteEntry(entry.id)}
                            />
                        ))
                    )}
                </View>
            </ScrollView>

            {/* Floating Action Button */}
            <FAB
                style={styles.fab}
                icon="plus"
                onPress={handleAddEntry}
                color="#fff"
            />

            {/* Smoking Form Modal */}
            <SmokingFormModal
                visible={modalVisible}
                entry={editingEntry}
                onClose={() => setModalVisible(false)}
                onSave={handleSaveEntry}
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
    streakCard: {
        margin: 15,
        elevation: 3,
        backgroundColor: '#4CAF50',
    },
    streakRow: {
        flexDirection: 'row',
        justifyContent: 'space-around',
        marginTop: 15,
    },
    streakItem: {
        alignItems: 'center',
    },
    streakValue: {
        fontSize: 32,
        fontWeight: 'bold',
        color: '#fff',
    },
    streakLabel: {
        fontSize: 12,
        color: '#fff',
        marginTop: 5,
    },
    statsCard: {
        marginHorizontal: 15,
        marginBottom: 15,
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
