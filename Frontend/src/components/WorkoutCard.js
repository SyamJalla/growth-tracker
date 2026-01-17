import React from 'react';
import { View, StyleSheet } from 'react-native';
import { Card, Title, Paragraph, IconButton, Chip } from 'react-native-paper';

export default function WorkoutCard({ workout, onEdit, onDelete }) {
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

    const getIntensityColor = (intensity) => {
        const colors = {
            Low: '#51CF66',
            Moderate: '#FFC107',
            High: '#F44336',
        };
        return colors[intensity] || '#9E9E9E';
    };

    const getWorkoutIcon = (type) => {
        const icons = {
            Push: '💪',
            Pull: '🔙',
            Legs: '🦵',
            Upper: '💪',
            Lower: '🦵',
            Cardio: '🏃',
            Others: '🏋️',
        };
        return icons[type] || '🏋️';
    };

    return (
        <Card style={styles.card}>
            <Card.Content>
                <View style={styles.header}>
                    <View style={styles.headerLeft}>
                        <Title style={styles.date}>
                            {formatDate(workout.date)}
                        </Title>
                        <Paragraph style={styles.workoutType}>
                            {getWorkoutIcon(workout.workout_type)} {workout.workout_type}
                        </Paragraph>
                    </View>
                    <View style={styles.actions}>
                        <IconButton
                            icon="pencil"
                            size={20}
                            onPress={onEdit}
                            iconColor="#4A90E2"
                        />
                        <IconButton
                            icon="delete"
                            size={20}
                            onPress={onDelete}
                            iconColor="#F44336"
                        />
                    </View>
                </View>

                <View style={styles.details}>
                    <View style={styles.detailItem}>
                        <Paragraph style={styles.detailLabel}>Duration</Paragraph>
                        <Title style={styles.detailValue}>
                            ⏱️ {workout.duration_minutes} min
                        </Title>
                    </View>

                    {workout.intensity && (
                        <View style={styles.intensityContainer}>
                            <Chip
                                style={[
                                    styles.intensityChip,
                                    { backgroundColor: getIntensityColor(workout.intensity) },
                                ]}
                                textStyle={styles.intensityText}
                            >
                                {workout.intensity}
                            </Chip>
                        </View>
                    )}
                </View>

                {workout.notes && (
                    <View style={styles.notesContainer}>
                        <Paragraph style={styles.notesLabel}>📝 Notes:</Paragraph>
                        <Paragraph style={styles.notes}>{workout.notes}</Paragraph>
                    </View>
                )}

                {!workout.workout_done && (
                    <View style={styles.skippedContainer}>
                        <Paragraph style={styles.skippedText}>
                            ⚠️ Rest Day / Skipped
                        </Paragraph>
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
    workoutType: {
        fontSize: 14,
        color: '#6C757D',
        fontWeight: '500',
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
        minWidth: 120,
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
        color: '#4A90E2',
    },
    intensityContainer: {
        marginLeft: 15,
        marginBottom: 8,
    },
    intensityChip: {
        backgroundColor: '#51CF66',
    },
    intensityText: {
        color: '#fff',
        fontWeight: 'bold',
        fontSize: 13,
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
    skippedContainer: {
        marginTop: 12,
        padding: 10,
        backgroundColor: '#FFF3CD',
        borderRadius: 6,
        borderLeftWidth: 4,
        borderLeftColor: '#FFC107',
    },
    skippedText: {
        color: '#856404',
        fontWeight: '600',
        fontSize: 13,
    },
});
