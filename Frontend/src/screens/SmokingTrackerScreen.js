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
    const [loading, setLoading] = useState(true);
    const [refreshing, setRefreshing] = useState(false);
    const [error, setError] = useState(null);
    const [modalVisible, setModalVisible] = useState(false);
    const [editingEntry, setEditingEntry] = useState(null);

    const fetchSmokingData = async () => {
        try {
            setError(null);
            const [entriesResponse, dashboardResponse] = await Promise.all([
                smokingApi.getAllEntries(),
                smokingApi.getStreakInfo(), // Gets dashboard data with smoking stats
            ]);

            setEntries(entriesResponse.data);
            // Dashboard returns both workout and smoking data
            if (dashboardResponse.data.smoking) {
                setStreakInfo(dashboardResponse.data.smoking);
            }
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
            // Use upsert endpoint for both create and update
            await smokingApi.upsertEntry(entryData);
            setModalVisible(false);
            setEditingEntry(null);
            fetchSmokingData();
        } catch (err) {
            console.error('Save smoking entry error:', err);
            Alert.alert('Error', 'Failed to save smoking entry');
        }
    };

    if (loading) {
        return (
            <View style={styles.centerContainer}>
                <ActivityIndicator size="large" color="#51CF66" />
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
                            <Title style={styles.cardTitle}>🎯 Smoke-Free Journey</Title>
                            <View style={styles.streakRow}>
                                <View style={styles.streakItem}>
                                    <Title style={styles.streakValue}>
                                        {streakInfo.current_clean_streak || 0}
                                    </Title>
                                    <Paragraph style={styles.streakLabel}>Current Clean Streak</Paragraph>
                                </View>
                                <View style={styles.streakItem}>
                                    <Title style={styles.streakValue}>
                                        {streakInfo.longest_clean_streak || 0}
                                    </Title>
                                    <Paragraph style={styles.streakLabel}>Best Streak</Paragraph>
                                </View>
                            </View>
                            <View style={styles.additionalStats}>
                                <View style={styles.statBox}>
                                    <Text style={styles.statNumber}>{streakInfo.total_relapses || 0}</Text>
                                    <Text style={styles.statText}>Total Relapses</Text>
                                </View>
                                <View style={styles.statBox}>
                                    <Text style={styles.statNumber}>{streakInfo.total_cigarettes || 0}</Text>
                                    <Text style={styles.statText}>Total Cigarettes</Text>
                                </View>
                                {streakInfo.most_common_location && (
                                    <View style={styles.statBox}>
                                        <Text style={styles.statNumber}>📍</Text>
                                        <Text style={styles.statText}>{streakInfo.most_common_location}</Text>
                                    </View>
                                )}
                            </View>
                        </Card.Content>
                    </Card>
                )}

                {/* Entries List */}
                <View style={styles.listContainer}>
                    <Title style={styles.listTitle}>
                        Recent Entries ({entries.length})
                    </Title>
                    {entries.length === 0 ? (
                        <Card style={styles.emptyCard}>
                            <Card.Content>
                                <Paragraph style={styles.emptyText}>
                                    🎉 No smoking entries yet!{'\n'}
                                    Keep up the great work on your smoke-free journey!
                                </Paragraph>
                            </Card.Content>
                        </Card>
                    ) : (
                        entries.map((entry) => (
                            <SmokingCard
                                key={entry.date}
                                entry={entry}
                                onEdit={() => handleEditEntry(entry)}
                                onDelete={() => handleDeleteEntry(entry.date)}
                            />
                        ))
                    )}
                </View>
            </ScrollView>

            {/* Floating Action Button */}
            <FAB
                style={styles.fab}
                icon="plus"
                label="Log Relapse"
                onPress={handleAddEntry}
                color="#fff"
            />

            {/* Smoking Form Modal */}
            <SmokingFormModal
                visible={modalVisible}
                entry={editingEntry}
                onClose={() => setModalVisible(false)}
                onSave={handleSaveEntry}
                currentStreak={streakInfo?.current_clean_streak || 0}
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
    streakCard: {
        margin: 15,
        elevation: 4,
        backgroundColor: '#51CF66',
        borderRadius: 12,
    },
    cardTitle: {
        color: '#FFFFFF',
        fontSize: 20,
        fontWeight: 'bold',
    },
    streakRow: {
        flexDirection: 'row',
        justifyContent: 'space-around',
        marginTop: 15,
        marginBottom: 10,
    },
    streakItem: {
        alignItems: 'center',
    },
    streakValue: {
        fontSize: 36,
        fontWeight: 'bold',
        color: '#FFFFFF',
    },
    streakLabel: {
        fontSize: 13,
        color: '#FFFFFF',
        marginTop: 5,
        textAlign: 'center',
    },
    additionalStats: {
        flexDirection: 'row',
        justifyContent: 'space-around',
        marginTop: 15,
        paddingTop: 15,
        borderTopWidth: 1,
        borderTopColor: 'rgba(255, 255, 255, 0.3)',
    },
    statBox: {
        alignItems: 'center',
    },
    statNumber: {
        fontSize: 20,
        fontWeight: 'bold',
        color: '#FFFFFF',
    },
    statText: {
        fontSize: 11,
        color: '#FFFFFF',
        marginTop: 3,
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
        backgroundColor: '#51CF66',
    },
});
