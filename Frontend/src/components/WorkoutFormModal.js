import React, { useState, useEffect } from 'react';
import {
    View,
    Modal,
    ScrollView,
    StyleSheet,
    Platform,
} from 'react-native';
import {
    TextInput,
    Button,
    Title,
    HelperText,
    Portal,
    Dialog,
    Paragraph,
} from 'react-native-paper';
import DateTimePicker from '@react-native-community/datetimepicker';

export default function WorkoutFormModal({ visible, workout, onClose, onSave }) {
    const [formData, setFormData] = useState({
        workout_type: '',
        workout_date: new Date(),
        duration_minutes: '',
        intensity: '',
        calories_burned: '',
        notes: '',
    });
    const [showDatePicker, setShowDatePicker] = useState(false);
    const [showTimePicker, setShowTimePicker] = useState(false);
    const [errors, setErrors] = useState({});

    useEffect(() => {
        if (workout) {
            setFormData({
                workout_type: workout.workout_type || '',
                workout_date: new Date(workout.workout_date),
                duration_minutes: workout.duration_minutes?.toString() || '',
                intensity: workout.intensity || '',
                calories_burned: workout.calories_burned?.toString() || '',
                notes: workout.notes || '',
            });
        } else {
            setFormData({
                workout_type: '',
                workout_date: new Date(),
                duration_minutes: '',
                intensity: '',
                calories_burned: '',
                notes: '',
            });
        }
        setErrors({});
    }, [workout, visible]);

    const validateForm = () => {
        const newErrors = {};

        if (!formData.workout_type.trim()) {
            newErrors.workout_type = 'Workout type is required';
        }

        if (!formData.duration_minutes || parseInt(formData.duration_minutes) <= 0) {
            newErrors.duration_minutes = 'Duration must be greater than 0';
        }

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleSave = () => {
        if (validateForm()) {
            const dataToSave = {
                workout_type: formData.workout_type,
                workout_date: formData.workout_date.toISOString(),
                duration_minutes: parseInt(formData.duration_minutes),
                intensity: formData.intensity || null,
                calories_burned: formData.calories_burned ? parseInt(formData.calories_burned) : null,
                notes: formData.notes || null,
            };
            onSave(dataToSave);
        }
    };

    const onDateChange = (event, selectedDate) => {
        setShowDatePicker(false);
        if (selectedDate) {
            setFormData({ ...formData, workout_date: selectedDate });
        }
    };

    const onTimeChange = (event, selectedTime) => {
        setShowTimePicker(false);
        if (selectedTime) {
            const newDate = new Date(formData.workout_date);
            newDate.setHours(selectedTime.getHours());
            newDate.setMinutes(selectedTime.getMinutes());
            setFormData({ ...formData, workout_date: newDate });
        }
    };

    return (
        <Portal>
            <Dialog visible={visible} onDismiss={onClose} style={styles.dialog}>
                <Dialog.Title>{workout ? 'Edit Workout' : 'Log Workout'}</Dialog.Title>
                <Dialog.ScrollArea>
                    <ScrollView contentContainerStyle={styles.scrollContent}>
                        <TextInput
                            label="Workout Type *"
                            value={formData.workout_type}
                            onChangeText={(text) => setFormData({ ...formData, workout_type: text })}
                            mode="outlined"
                            style={styles.input}
                            error={!!errors.workout_type}
                        />
                        <HelperText type="error" visible={!!errors.workout_type}>
                            {errors.workout_type}
                        </HelperText>

                        <Button
                            mode="outlined"
                            onPress={() => setShowDatePicker(true)}
                            style={styles.input}
                        >
                            Date: {formData.workout_date.toLocaleDateString()}
                        </Button>

                        <Button
                            mode="outlined"
                            onPress={() => setShowTimePicker(true)}
                            style={styles.input}
                        >
                            Time: {formData.workout_date.toLocaleTimeString()}
                        </Button>

                        {showDatePicker && (
                            <DateTimePicker
                                value={formData.workout_date}
                                mode="date"
                                display="default"
                                onChange={onDateChange}
                            />
                        )}

                        {showTimePicker && (
                            <DateTimePicker
                                value={formData.workout_date}
                                mode="time"
                                display="default"
                                onChange={onTimeChange}
                            />
                        )}

                        <TextInput
                            label="Duration (minutes) *"
                            value={formData.duration_minutes}
                            onChangeText={(text) => setFormData({ ...formData, duration_minutes: text })}
                            mode="outlined"
                            keyboardType="numeric"
                            style={styles.input}
                            error={!!errors.duration_minutes}
                        />
                        <HelperText type="error" visible={!!errors.duration_minutes}>
                            {errors.duration_minutes}
                        </HelperText>

                        <TextInput
                            label="Intensity (e.g., Low, Medium, High)"
                            value={formData.intensity}
                            onChangeText={(text) => setFormData({ ...formData, intensity: text })}
                            mode="outlined"
                            style={styles.input}
                        />

                        <TextInput
                            label="Calories Burned"
                            value={formData.calories_burned}
                            onChangeText={(text) => setFormData({ ...formData, calories_burned: text })}
                            mode="outlined"
                            keyboardType="numeric"
                            style={styles.input}
                        />

                        <TextInput
                            label="Notes"
                            value={formData.notes}
                            onChangeText={(text) => setFormData({ ...formData, notes: text })}
                            mode="outlined"
                            multiline
                            numberOfLines={3}
                            style={styles.input}
                        />
                    </ScrollView>
                </Dialog.ScrollArea>
                <Dialog.Actions>
                    <Button onPress={onClose}>Cancel</Button>
                    <Button onPress={handleSave} mode="contained">
                        Save
                    </Button>
                </Dialog.Actions>
            </Dialog>
        </Portal>
    );
}

const styles = StyleSheet.create({
    dialog: {
        maxHeight: '80%',
    },
    scrollContent: {
        paddingHorizontal: 24,
    },
    input: {
        marginBottom: 8,
    },
});
