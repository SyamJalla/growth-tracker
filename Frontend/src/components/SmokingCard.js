import React from 'react';
import { View, StyleSheet } from 'react-native';
import { Card, Title, Paragraph, IconButton, Chip } from 'react-native-paper';

export default function SmokingCard({ entry, onEdit, onDelete }) {
    const formatDate = (dateString) => {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            month: 'short',
            day: 'numeric',
            year: 'numeric',
        });
    };

    const formatTime = (dateString) => {
        const date = new Date(dateString);
        return date.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
        });
    };

    const getMoodColor = (mood) => {
        const colors = {
            happy: '#4CAF50',
            neutral: '#FFC107',
            stressed: '#FF9800',
            anxious: '#F44336',
        };
        return colors[mood?.toLowerCase()] || '#9E9E9E';
    };

    return (
        <Card style={styles.card}>
            <Card.Content>
                <View style={styles.header}>
                    <View style={styles.headerLeft}>
                        <Title style={styles.date}>
                            {formatDate(entry.entry_date)}
                        </Title>
                        <Paragraph style={styles.time}>
                            {formatTime(entry.entry_date)}
                        </Paragraph>
                    </View>
                    <View style={styles.actions}>
                        <IconButton icon="pencil" size={20} onPress={onEdit} />
                        <IconButton icon="delete" size={20} onPress={onDelete} />
                    </View>
                </View>

                <View style={styles.details}>
                    <View style={styles.detailItem}>
                        <Paragraph style={styles.detailLabel}>Cigarettes</Paragraph>
                        <Title style={styles.detailValue}>{entry.cigarettes_smoked || 0}</Title>
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
                </View>

                {entry.notes && (
                    <View style={styles.notesContainer}>
                        <Paragraph style={styles.notes}>{entry.notes}</Paragraph>
                    </View>
                )}

                {entry.triggers && entry.triggers.length > 0 && (
                    <View style={styles.triggersContainer}>
                        <Paragraph style={styles.triggersLabel}>Triggers:</Paragraph>
                        <View style={styles.triggersList}>
                            {entry.triggers.map((trigger, index) => (
                                <Chip key={index} style={styles.triggerChip} textStyle={styles.triggerText}>
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
        marginBottom: 10,
        elevation: 2,
    },
    header: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'flex-start',
        marginBottom: 10,
    },
    headerLeft: {
        flex: 1,
    },
    date: {
        fontSize: 18,
        fontWeight: 'bold',
        marginBottom: 2,
    },
    time: {
        fontSize: 12,
        color: '#666',
    },
    actions: {
        flexDirection: 'row',
    },
    details: {
        flexDirection: 'row',
        alignItems: 'center',
        paddingVertical: 10,
        borderTopWidth: 1,
        borderTopColor: '#e0e0e0',
    },
    detailItem: {
        alignItems: 'center',
        flex: 1,
    },
    detailLabel: {
        fontSize: 12,
        color: '#666',
    },
    detailValue: {
        fontSize: 24,
        fontWeight: 'bold',
        marginTop: 2,
    },
    moodContainer: {
        flex: 1,
        alignItems: 'center',
    },
    moodChip: {
        backgroundColor: '#4CAF50',
    },
    moodText: {
        color: '#fff',
        fontWeight: 'bold',
    },
    notesContainer: {
        marginTop: 10,
        paddingTop: 10,
        borderTopWidth: 1,
        borderTopColor: '#e0e0e0',
    },
    notes: {
        fontSize: 14,
        fontStyle: 'italic',
        color: '#666',
    },
    triggersContainer: {
        marginTop: 10,
        paddingTop: 10,
        borderTopWidth: 1,
        borderTopColor: '#e0e0e0',
    },
    triggersLabel: {
        fontSize: 12,
        color: '#666',
        marginBottom: 5,
    },
    triggersList: {
        flexDirection: 'row',
        flexWrap: 'wrap',
    },
    triggerChip: {
        marginRight: 5,
        marginBottom: 5,
        backgroundColor: '#FFC107',
    },
    triggerText: {
        fontSize: 12,
    },
});
