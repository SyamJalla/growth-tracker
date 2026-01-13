import React from 'react';
import { View, StyleSheet } from 'react-native';
import { Card, Title, Paragraph, IconButton } from 'react-native-paper';

export default function WorkoutCard({ workout, onEdit, onDelete }) {
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

    return (
        <Card style={styles.card}>
            <Card.Content>
                <View style={styles.header}>
                    <View style={styles.headerLeft}>
                        <Title style={styles.type}>{workout.workout_type || 'Workout'}</Title>
                        <Paragraph style={styles.date}>
                            {formatDate(workout.workout_date)} at {formatTime(workout.workout_date)}
                        </Paragraph>
                    </View>
                    <View style={styles.actions}>
                        <IconButton icon="pencil" size={20} onPress={onEdit} />
                        <IconButton icon="delete" size={20} onPress={onDelete} />
                    </View>
                </View>

                <View style={styles.details}>
                    <View style={styles.detailItem}>
                        <Paragraph style={styles.detailLabel}>Duration</Paragraph>
                        <Paragraph style={styles.detailValue}>{workout.duration_minutes} min</Paragraph>
                    </View>
                    <View style={styles.detailItem}>
                        <Paragraph style={styles.detailLabel}>Intensity</Paragraph>
                        <Paragraph style={styles.detailValue}>{workout.intensity || 'N/A'}</Paragraph>
                    </View>
                    <View style={styles.detailItem}>
                        <Paragraph style={styles.detailLabel}>Calories</Paragraph>
                        <Paragraph style={styles.detailValue}>
                            {workout.calories_burned || 'N/A'}
                        </Paragraph>
                    </View>
                </View>

                {workout.notes && (
                    <View style={styles.notesContainer}>
                        <Paragraph style={styles.notes}>{workout.notes}</Paragraph>
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
    type: {
        fontSize: 18,
        fontWeight: 'bold',
        marginBottom: 2,
    },
    date: {
        fontSize: 12,
        color: '#666',
    },
    actions: {
        flexDirection: 'row',
    },
    details: {
        flexDirection: 'row',
        justifyContent: 'space-around',
        paddingVertical: 10,
        borderTopWidth: 1,
        borderTopColor: '#e0e0e0',
    },
    detailItem: {
        alignItems: 'center',
    },
    detailLabel: {
        fontSize: 12,
        color: '#666',
    },
    detailValue: {
        fontSize: 16,
        fontWeight: 'bold',
        marginTop: 2,
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
});
