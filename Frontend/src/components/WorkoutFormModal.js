import React, { useState, useEffect } from 'react';
import { View, StyleSheet, ScrollView, Platform, TextInput as RNTextInput } from 'react-native';
import {
    Modal,
    Portal,
    Button,
    TextInput,
    Title,
    HelperText,
    Chip,
} from 'react-native-paper';
import DateTimePicker from '@react-native-community/datetimepicker';

// Match backend WorkoutType enum exactly
const WORKOUT_TYPES = ['Push', 'Pull', 'Legs', 'Upper', 'Lower', 'Cardio', 'Others'];

// Match backend IntensityLevel enum exactly
const INTENSITY_LEVELS = ['Low', 'Moderate', 'High'];

export default function WorkoutFormModal({ visible, entry, onClose, onSave }) {
    const [date, setDate] = useState(new Date());
    const [dateString, setDateString] = useState(''); // For web input
    const [showDatePicker, setShowDatePicker] = useState(false);
    const [workoutType, setWorkoutType] = useState('');
    const [duration, setDuration] = useState('');
    const [intensity, setIntensity] = useState('');
    const [notes, setNotes] = useState('');
    const [errors, setErrors] = useState({});

    useEffect(() => {
        if (entry) {
            // Editing existing entry
            const entryDate = new Date(entry.date + 'T00:00:00');
            setDate(entryDate);
            setDateString(entry.date); // YYYY-MM-DD format
            setWorkoutType(entry.workout_type || '');
            setDuration(entry.duration_minutes?.toString() || '');
            setIntensity(entry.intensity || '');
            setNotes(entry.notes || '');
        } else {
            // New entry - default to today
            const today = new Date();
            setDate(today);
            setDateString(formatDateForBackend(today));
            setWorkoutType('');
            setDuration('');
            setIntensity('');
            setNotes('');
        }
        setErrors({});
    }, [entry, visible]);

    const formatDateForDisplay = (date) => {
        return date.toLocaleDateString('en-US', {
            weekday: 'short',
            month: 'short',
            day: 'numeric',
            year: 'numeric',
        });
    };

    const formatDateForBackend = (date) => {
        // Format as YYYY-MM-DD for backend
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    };

    const handleDateChange = (event, selectedDate) => {
        console.log('📅 Date change event:', event.type, 'Selected:', selectedDate);

        // On Android, picker auto-closes after selection
        if (Platform.OS === 'android') {
            setShowDatePicker(false);
        }

        // Update date if user confirmed (not cancelled)
        if (event.type === 'set' && selectedDate) {
            console.log('✅ Setting new date:', selectedDate);
            setDate(selectedDate);
            setDateString(formatDateForBackend(selectedDate));
        } else if (event.type === 'dismissed') {
            console.log('❌ Date picker dismissed');
            // On iOS, we need to hide the picker when dismissed
            if (Platform.OS === 'ios') {
                setShowDatePicker(false);
            }
        }
    };

    // Handle web date input change
    const handleWebDateChange = (text) => {
        setDateString(text);
        // Parse YYYY-MM-DD format
        const newDate = new Date(text + 'T00:00:00');
        if (!isNaN(newDate.getTime())) {
            setDate(newDate);
        }
    };

    const validateForm = () => {
        const newErrors = {};

        if (!workoutType) {
            newErrors.workoutType = 'Please select a workout type';
        }

        if (!duration || parseInt(duration) <= 0) {
            newErrors.duration = 'Duration must be greater than 0';
        }

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleSubmit = () => {
        if (!validateForm()) return;

        const workoutData = {
            date: Platform.OS === 'web' ? dateString : formatDateForBackend(date),
            workout_done: true,
            workout_type: workoutType,
            duration_minutes: parseInt(duration),
            intensity: intensity || null,
            notes: notes || null,
        };

        console.log('📤 Submitting workout data:', workoutData);
        onSave(workoutData);
    };

    return (
        <Portal>
            <Modal
                visible={visible}
                onDismiss={onClose}
                contentContainerStyle={styles.modal}
            >
                <ScrollView>
                    <Title style={styles.title}>
                        {entry ? 'Edit Workout' : 'Log Workout'}
                    </Title>

                    {/* Date Picker - Web vs Mobile */}
                    {Platform.OS === 'web' ? (
                        // Web: Use native HTML5 date input
                        <View style={styles.webDateContainer}>
                            <Title style={styles.webDateLabel}>Date *</Title>
                            <RNTextInput
                                style={styles.webDateInput}
                                type="date"
                                value={dateString}
                                onChange={(e) => handleWebDateChange(e.target.value)}
                                max={formatDateForBackend(new Date())} // Today
                                min="2026-01-01" // Year start
                            />
                        </View>
                    ) : (
                        // Mobile: Use native date picker
                        <>
                            <Button
                                mode="outlined"
                                onPress={() => setShowDatePicker(true)}
                                style={styles.dateButton}
                                icon="calendar"
                            >
                                Date: {formatDateForDisplay(date)}
                            </Button>

                            {showDatePicker && (
                                <DateTimePicker
                                    value={date}
                                    mode="date"
                                    display={Platform.OS === 'ios' ? 'spinner' : 'default'}
                                    onChange={handleDateChange}
                                    testID="dateTimePicker"
                                />
                            )}
                        </>
                    )}

                    {/* Workout Type */}
                    <View style={styles.section}>
                        <Title style={styles.sectionTitle}>Workout Type *</Title>
                        <View style={styles.chipContainer}>
                            {WORKOUT_TYPES.map((type) => (
                                <Chip
                                    key={type}
                                    selected={workoutType === type}
                                    onPress={() => setWorkoutType(type)}
                                    style={styles.chip}
                                    selectedColor="#4A90E2"
                                >
                                    {type}
                                </Chip>
                            ))}
                        </View>
                        {errors.workoutType && (
                            <HelperText type="error">{errors.workoutType}</HelperText>
                        )}
                    </View>

                    {/* Duration */}
                    <TextInput
                        label="Duration (minutes) *"
                        value={duration}
                        onChangeText={setDuration}
                        keyboardType="numeric"
                        mode="outlined"
                        style={styles.input}
                        error={!!errors.duration}
                    />
                    {errors.duration && (
                        <HelperText type="error">{errors.duration}</HelperText>
                    )}

                    {/* Intensity */}
                    <View style={styles.section}>
                        <Title style={styles.sectionTitle}>Intensity (Optional)</Title>
                        <View style={styles.chipContainer}>
                            {INTENSITY_LEVELS.map((level) => (
                                <Chip
                                    key={level}
                                    selected={intensity === level}
                                    onPress={() => setIntensity(level)}
                                    style={styles.chip}
                                    selectedColor="#4A90E2"
                                >
                                    {level}
                                </Chip>
                            ))}
                        </View>
                    </View>

                    {/* Notes */}
                    <TextInput
                        label="Notes (Optional)"
                        value={notes}
                        onChangeText={setNotes}
                        multiline
                        numberOfLines={4}
                        mode="outlined"
                        style={styles.input}
                    />

                    {/* Action Buttons */}
                    <View style={styles.buttonContainer}>
                        <Button
                            mode="outlined"
                            onPress={onClose}
                            style={styles.button}
                        >
                            Cancel
                        </Button>
                        <Button
                            mode="contained"
                            onPress={handleSubmit}
                            style={styles.button}
                            buttonColor="#4A90E2"
                        >
                            {entry ? 'Update' : 'Save'}
                        </Button>
                    </View>
                </ScrollView>
            </Modal>
        </Portal>
    );
}

const styles = StyleSheet.create({
    modal: {
        backgroundColor: 'white',
        padding: 20,
        margin: 20,
        borderRadius: 8,
        maxHeight: '90%',
    },
    title: {
        fontSize: 24,
        fontWeight: 'bold',
        marginBottom: 20,
        color: '#212529',
    },
    dateButton: {
        marginBottom: 20,
    },
    webDateContainer: {
        marginBottom: 20,
    },
    webDateLabel: {
        fontSize: 16,
        marginBottom: 8,
        color: '#495057',
    },
    webDateInput: {
        padding: 12,
        borderWidth: 1,
        borderColor: '#CED4DA',
        borderRadius: 4,
        fontSize: 16,
        backgroundColor: '#FFFFFF',
    },
    section: {
        marginBottom: 20,
    },
    sectionTitle: {
        fontSize: 16,
        marginBottom: 10,
        color: '#495057',
    },
    chipContainer: {
        flexDirection: 'row',
        flexWrap: 'wrap',
        gap: 8,
    },
    chip: {
        marginRight: 8,
        marginBottom: 8,
    },
    input: {
        marginBottom: 15,
    },
    buttonContainer: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        marginTop: 20,
    },
    button: {
        flex: 1,
        marginHorizontal: 5,
    },
});
