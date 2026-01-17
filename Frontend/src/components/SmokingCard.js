import React from 'react';
import { View, StyleSheet } from 'react-native';
import { Card, Title, Paragraph, IconButton, Chip } from 'react-native-paper';

export default function SmokingCard({ entry, onEdit, onDelete }) {
    const formatDate = (dateString) => {
        try {
            // Backend returns date as "YYYY-MM-DD" string
            const date = new Date(dateString + 'T00:00:00');
            return date.toLocaleDateString('en-US', {
                weekday: 'short',
                month: 'short',
                day: 'numeric',
                year: 'numeric',
            });
        } catch (error) {
            console.error('Date formatting error:', error, dateString);
            return dateString;
        }
    };

    const formatTime = (timeString) => {
        try {
            if (!timeString) return 'N/A';
            // Parse HH:MM:SS format
            const [hours, minutes] = timeString.split(':');
            const date = new Date();
            date.setHours(parseInt(hours), parseInt(minutes));
            return date.toLocaleTimeString('en-US', {
                hour: '2-digit',
                minute: '2-digit',
            });
        } catch (error) {
            console.error('Time formatting error:', error, timeString);
            return timeString;
        }
    };

    const getMoodColor = (mood) => {
        const colors = {
            Happy: '#51CF66',
            Neutral: '#FFC107',
            Stressed: '#FF9800',
            Anxious: '#F44336',
        };
        return colors[mood] || '#9E9E9E';
    };

    const getLocationIcon = (location) => {
        const icons = {
            Home: '🏠',
            Work: '💼',
            Social: '🎉',
            Outside: '🌳',
            Car: '🚗',
            Other: '📍',
        };
        return icons[location] || '📍';
    };

    return (
        <Card style={styles.card}>
            <Card.Content>
                <View style={styles.header}>
                    <View style={styles.headerLeft}>
                        <Title style={styles.date}>
                            {formatDate(entry.date)}
                        </Title>
                        {entry.time && (
                            <Paragraph style={styles.time}>
                                🕐 {formatTime(entry.time)}
                            </Paragraph>
                        )}
                    </View>
                    <View style={styles.actions}>
                        <IconButton icon="pencil" size={20} onPress={onEdit} iconColor="#4A90E2" />
                        <IconButton icon="delete" size={20} onPress={onDelete} iconColor="#F44336" />
                    </View>
                </View>

                <View style={styles.details}>
                    <View style={styles.detailItem}>
                        <Paragraph style={styles.detailLabel}>Cigarettes</Paragraph>
                        <Title style={styles.detailValue}>🚬 {entry.cigarette_count || 0}</Title>
                    </View>

                    {entry.mood && (
                        <View style={styles.moodContainer}>
                            <Chip
                                style={[styles.moodChip, { backgroundColor: getMoodColor(entry.mood) }]}
                                textStyle={styles.moodText}
                            >
                                {entry.mood}
                            </Chip>
                        </View>
                    )}

                    {entry.location && (
                        <View style={styles.locationContainer}>
                            <Paragraph style={styles.locationText}>
                                {getLocationIcon(entry.location)} {entry.location}
                            </Paragraph>
                        </View>
                    )}
                </View>

                {entry.notes && (
                    <View style={styles.notesContainer}>
                        <Paragraph style={styles.notesLabel}>📝 Notes:</Paragraph>
                        <Paragraph style={styles.notes}>{entry.notes}</Paragraph>
                    </View>
                )}

                {entry.triggers && entry.triggers.length > 0 && (
                    <View style={styles.triggersContainer}>
                        <Paragraph style={styles.triggersLabel}>⚡ Triggers:</Paragraph>
                        <View style={styles.triggersList}>
                            {entry.triggers.map((trigger, index) => (
                                <Chip
                                    key={index}
                                    style={styles.triggerChip}
                                    textStyle={styles.triggerText}
                                    mode="outlined"
                                >
                                    {trigger}
                                </Chip>
                            ))}
                        </View>
                    </View>
                )}
            </Card.Content>
        </Card>
    );
}

const styles = StyleSheet.create({
    card: {
        marginBottom: 12,
        elevation: 3,
        backgroundColor: '#FFFFFF',
        borderRadius: 8,
    },
    header: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'flex-start',
        marginBottom: 12,
    },
    headerLeft: {
        flex: 1,
    },
    date: {
        fontSize: 16,
        fontWeight: 'bold',
        marginBottom: 4,
        color: '#212529',
    },
    time: {
        fontSize: 12,
        color: '#6C757D',
    },
    actions: {
        flexDirection: 'row',
        marginTop: -8,
        marginRight: -8,
    },
    details: {
        flexDirection: 'row',
        alignItems: 'center',
        paddingVertical: 12,
        borderTopWidth: 1,
        borderTopColor: '#E9ECEF',
        flexWrap: 'wrap',
    },
    detailItem: {
        alignItems: 'center',
        minWidth: 100,
        marginBottom: 8,
    },
    detailLabel: {
        fontSize: 12,
        color: '#6C757D',
    },
    detailValue: {
        fontSize: 22,
        fontWeight: 'bold',
        marginTop: 4,
        color: '#F44336',
    },
    moodContainer: {
        marginLeft: 15,
        marginBottom: 8,
    },
    moodChip: {
        backgroundColor: '#51CF66',
    },
    moodText: {
        color: '#fff',
        fontWeight: 'bold',
        fontSize: 13,
    },
    locationContainer: {
        marginLeft: 15,
        marginBottom: 8,
    },
    locationText: {
        fontSize: 13,
        color: '#495057',
        fontWeight: '500',
    },
    notesContainer: {
        marginTop: 12,
        paddingTop: 12,
        borderTopWidth: 1,
        borderTopColor: '#E9ECEF',
    },
    notesLabel: {
        fontSize: 12,
        color: '#6C757D',
        marginBottom: 6,
        fontWeight: '600',
    },
    notes: {
        fontSize: 14,
        fontStyle: 'italic',
        color: '#495057',
        lineHeight: 20,
    },
    triggersContainer: {
        marginTop: 12,
        paddingTop: 12,
        borderTopWidth: 1,
        borderTopColor: '#E9ECEF',
    },
    triggersLabel: {
        fontSize: 12,
        color: '#6C757D',
        marginBottom: 8,
        fontWeight: '600',
    },
    triggersList: {
        flexDirection: 'row',
        flexWrap: 'wrap',
    },
    triggerChip: {
        marginRight: 8,
        marginBottom: 8,
        backgroundColor: '#FFF3CD',
        borderColor: '#FFC107',
    },
    triggerText: {
        fontSize: 12,
        color: '#856404',
    },
});
