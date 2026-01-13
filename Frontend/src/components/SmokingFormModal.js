import React, { useState, useEffect } from 'react';
import {
    View,
    Modal,
    ScrollView,
    StyleSheet,
} from 'react-native';
import {
    TextInput,
    Button,
    Title,
    HelperText,
    Portal,
    Dialog,
    Chip,
} from 'react-native-paper';
import DateTimePicker from '@react-native-community/datetimepicker';

const MOOD_OPTIONS = ['Happy', 'Neutral', 'Stressed', 'Anxious'];
const TRIGGER_OPTIONS = ['Stress', 'Social', 'Boredom', 'Habit', 'Alcohol', 'Other'];

export default function SmokingFormModal({ visible, entry, onClose, onSave }) {
    const [formData, setFormData] = useState({
        entry_date: new Date(),
        cigarettes_smoked: '',
        mood: '',
        triggers: [],
        notes: '',
    });
    const [showDatePicker, setShowDatePicker] = useState(false);
    const [showTimePicker, setShowTimePicker] = useState(false);
    const [errors, setErrors] = useState({});

    useEffect(() => {
        if (entry) {
            setFormData({
                entry_date: new Date(entry.entry_date),
                cigarettes_smoked: entry.cigarettes_smoked?.toString() || '',
                mood: entry.mood || '',
                triggers: entry.triggers || [],
                notes: entry.notes || '',
            });
        } else {
            setFormData({
                entry_date: new Date(),
                cigarettes_smoked: '',
                mood: '',
                triggers: [],
                notes: '',
            });
        }
        setErrors({});
    }, [entry, visible]);

    const validateForm = () => {
        const newErrors = {};

        if (!formData.cigarettes_smoked || parseInt(formData.cigarettes_smoked) < 0) {
            newErrors.cigarettes_smoked = 'Please enter a valid number';
        }

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleSave = () => {
        if (validateForm()) {
            const dataToSave = {
                entry_date: formData.entry_date.toISOString(),
                cigarettes_smoked: parseInt(formData.cigarettes_smoked),
                mood: formData.mood || null,
                triggers: formData.triggers.length > 0 ? formData.triggers : null,
                notes: formData.notes || null,
            };
            onSave(dataToSave);
        }
    };

    const toggleTrigger = (trigger) => {
        if (formData.triggers.includes(trigger)) {
            setFormData({
                ...formData,
                triggers: formData.triggers.filter((t) => t !== trigger),
            });
        } else {
            setFormData({
                ...formData,
                triggers: [...formData.triggers, trigger],
            });
        }
    };

    const onDateChange = (event, selectedDate) => {
        setShowDatePicker(false);
        if (selectedDate) {
            setFormData({ ...formData, entry_date: selectedDate });
        }
    };

    const onTimeChange = (event, selectedTime) => {
        setShowTimePicker(false);
        if (selectedTime) {
            const newDate = new Date(formData.entry_date);
            newDate.setHours(selectedTime.getHours());
            newDate.setMinutes(selectedTime.getMinutes());
            setFormData({ ...formData, entry_date: newDate });
        }
    };

    return (
        <Portal>
            <Dialog visible={visible} onDismiss={onClose} style={styles.dialog}>
                <Dialog.Title>{entry ? 'Edit Entry' : 'Log Smoking Entry'}</Dialog.Title>
                <Dialog.ScrollArea>
                    <ScrollView contentContainerStyle={styles.scrollContent}>
                        <Button
                            mode="outlined"
                            onPress={() => setShowDatePicker(true)}
                            style={styles.input}
                        >
                            Date: {formData.entry_date.toLocaleDateString()}
                        </Button>

                        <Button
                            mode="outlined"
                            onPress={() => setShowTimePicker(true)}
                            style={styles.input}
                        >
                            Time: {formData.entry_date.toLocaleTimeString()}
                        </Button>

                        {showDatePicker && (
                            <DateTimePicker
                                value={formData.entry_date}
                                mode="date"
                                display="default"
                                onChange={onDateChange}
                            />
                        )}

                        {showTimePicker && (
                            <DateTimePicker
                                value={formData.entry_date}
                                mode="time"
                                display="default"
                                onChange={onTimeChange}
                            />
                        )}

                        <TextInput
                            label="Cigarettes Smoked *"
                            value={formData.cigarettes_smoked}
                            onChangeText={(text) => setFormData({ ...formData, cigarettes_smoked: text })}
                            mode="outlined"
                            keyboardType="numeric"
                            style={styles.input}
                            error={!!errors.cigarettes_smoked}
                        />
                        <HelperText type="error" visible={!!errors.cigarettes_smoked}>
                            {errors.cigarettes_smoked}
                        </HelperText>

                        <Title style={styles.sectionTitle}>Mood</Title>
                        <View style={styles.chipContainer}>
                            {MOOD_OPTIONS.map((mood) => (
                                <Chip
                                    key={mood}
                                    selected={formData.mood === mood}
                                    onPress={() => setFormData({ ...formData, mood: mood })}
                                    style={styles.chip}
                                >
                                    {mood}
                                </Chip>
                            ))}
                        </View>

                        <Title style={styles.sectionTitle}>Triggers</Title>
                        <View style={styles.chipContainer}>
                            {TRIGGER_OPTIONS.map((trigger) => (
                                <Chip
                                    key={trigger}
                                    selected={formData.triggers.includes(trigger)}
                                    onPress={() => toggleTrigger(trigger)}
                                    style={styles.chip}
                                >
                                    {trigger}
                                </Chip>
                            ))}
                        </View>

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
    sectionTitle: {
        fontSize: 16,
        marginTop: 10,
        marginBottom: 5,
    },
    chipContainer: {
        flexDirection: 'row',
        flexWrap: 'wrap',
        marginBottom: 15,
    },
    chip: {
        marginRight: 8,
        marginBottom: 8,
    },
});
