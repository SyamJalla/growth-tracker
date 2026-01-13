import React, { useState, useEffect } from 'react';
import {
    View,
    ScrollView,
    StyleSheet,
    RefreshControl,
    Text,
    ActivityIndicator,
} from 'react-native';
import { Card, Title, Paragraph, Button } from 'react-native-paper';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import { healthApi } from '../services/api';
import ErrorMessage from '../components/ErrorMessage';

export default function HealthScreen() {
    const [healthStatus, setHealthStatus] = useState(null);
    const [dbStatus, setDbStatus] = useState(null);
    const [loading, setLoading] = useState(true);
    const [refreshing, setRefreshing] = useState(false);
    const [error, setError] = useState(null);

    const fetchHealthStatus = async () => {
        try {
            setError(null);
            const [healthResponse, dbResponse] = await Promise.all([
                healthApi.checkHealth(),
                healthApi.checkDbHealth(),
            ]);

            setHealthStatus(healthResponse.data);
            setDbStatus(dbResponse.data);
        } catch (err) {
            setError(err.message || 'Failed to load health status');
            console.error('Health check error:', err);
        } finally {
            setLoading(false);
            setRefreshing(false);
        }
    };

    useEffect(() => {
        fetchHealthStatus();
    }, []);

    const onRefresh = () => {
        setRefreshing(true);
        fetchHealthStatus();
    };

    const getStatusColor = (status) => {
        return status === 'healthy' || status === 'ok' ? '#4CAF50' : '#F44336';
    };

    const getStatusIcon = (status) => {
        return status === 'healthy' || status === 'ok' ? 'check-circle' : 'alert-circle';
    };

    if (loading) {
        return (
            <View style={styles.centerContainer}>
                <ActivityIndicator size="large" color="#2196F3" />
                <Text style={styles.loadingText}>Checking system health...</Text>
            </View>
        );
    }

    if (error) {
        return <ErrorMessage message={error} onRetry={fetchHealthStatus} />;
    }

    return (
        <ScrollView
            style={styles.container}
            refreshControl={
                <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
            }
        >
            {/* API Health Status */}
            {healthStatus && (
                <Card style={styles.card}>
                    <Card.Content>
                        <View style={styles.headerRow}>
                            <MaterialCommunityIcons
                                name={getStatusIcon(healthStatus.status)}
                                size={40}
                                color={getStatusColor(healthStatus.status)}
                            />
                            <View style={styles.headerText}>
                                <Title>API Health</Title>
                                <Paragraph style={[
                                    styles.statusText,
                                    { color: getStatusColor(healthStatus.status) }
                                ]}>
                                    {healthStatus.status?.toUpperCase()}
                                </Paragraph>
                            </View>
                        </View>
                        {healthStatus.timestamp && (
                            <Paragraph style={styles.timestamp}>
                                Last checked: {new Date(healthStatus.timestamp).toLocaleString()}
                            </Paragraph>
                        )}
                    </Card.Content>
                </Card>
            )}

            {/* Database Health Status */}
            {dbStatus && (
                <Card style={styles.card}>
                    <Card.Content>
                        <View style={styles.headerRow}>
                            <MaterialCommunityIcons
                                name={getStatusIcon(dbStatus.status)}
                                size={40}
                                color={getStatusColor(dbStatus.status)}
                            />
                            <View style={styles.headerText}>
                                <Title>Database Health</Title>
                                <Paragraph style={[
                                    styles.statusText,
                                    { color: getStatusColor(dbStatus.status) }
                                ]}>
                                    {dbStatus.status?.toUpperCase()}
                                </Paragraph>
                            </View>
                        </View>
                        {dbStatus.message && (
                            <Paragraph style={styles.message}>{dbStatus.message}</Paragraph>
                        )}
                    </Card.Content>
                </Card>
            )}

            {/* System Information */}
            <Card style={styles.card}>
                <Card.Content>
                    <Title>System Information</Title>
                    <View style={styles.infoRow}>
                        <MaterialCommunityIcons name="api" size={24} color="#2196F3" />
                        <View style={styles.infoText}>
                            <Paragraph style={styles.infoLabel}>API Version</Paragraph>
                            <Paragraph>1.0.0</Paragraph>
                        </View>
                    </View>
                    <View style={styles.infoRow}>
                        <MaterialCommunityIcons name="database" size={24} color="#2196F3" />
                        <View style={styles.infoText}>
                            <Paragraph style={styles.infoLabel}>Database</Paragraph>
                            <Paragraph>SQLite</Paragraph>
                        </View>
                    </View>
                    <View style={styles.infoRow}>
                        <MaterialCommunityIcons name="server" size={24} color="#2196F3" />
                        <View style={styles.infoText}>
                            <Paragraph style={styles.infoLabel}>Server</Paragraph>
                            <Paragraph>FastAPI</Paragraph>
                        </View>
                    </View>
                </Card.Content>
            </Card>

            {/* Refresh Button */}
            <View style={styles.buttonContainer}>
                <Button
                    mode="contained"
                    onPress={fetchHealthStatus}
                    icon="refresh"
                    style={styles.button}
                >
                    Refresh Health Status
                </Button>
            </View>
        </ScrollView>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#f5f5f5',
        padding: 15,
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
    card: {
        marginBottom: 15,
        elevation: 3,
    },
    headerRow: {
        flexDirection: 'row',
        alignItems: 'center',
        marginBottom: 10,
    },
    headerText: {
        marginLeft: 15,
        flex: 1,
    },
    statusText: {
        fontSize: 16,
        fontWeight: 'bold',
    },
    timestamp: {
        fontSize: 12,
        color: '#666',
        marginTop: 5,
    },
    message: {
        marginTop: 10,
        color: '#666',
    },
    infoRow: {
        flexDirection: 'row',
        alignItems: 'center',
        marginTop: 15,
    },
    infoText: {
        marginLeft: 15,
        flex: 1,
    },
    infoLabel: {
        fontSize: 12,
        color: '#666',
    },
    buttonContainer: {
        marginVertical: 20,
    },
    button: {
        backgroundColor: '#2196F3',
    },
});
