import React, { useState, useEffect } from 'react';
import {
    View,
    Modal,
    ScrollView,
    StyleSheet,
    Alert,
    Platform,
} from 'react-native';
import {
    TextInput,
    Button,
    Title,
    HelperText,
    Portal,
    Dialog,
    Chip,
    Paragraph,
    Banner,
} from 'react-native-paper';
import DateTimePicker from '@react-native-community/datetimepicker';

const MOOD_OPTIONS = ['Happy', 'Neutral', 'Stressed', 'Anxious'];
const TRIGGER_OPTIONS = ['Stress', 'Social', 'Boredom', 'Habit', 'Alcohol', 'Other'];

export default function SmokingFormModal({ visible, entry, onClose, onSave, currentStreak }) {
    const [formData, setFormData] = useState({
        entry_date: new Date(),
        cigarette_count: '',
        location: '',
        remarks: '',
    });
    const [showDatePicker, setShowDatePicker] = useState(false);
    const [errors, setErrors] = useState({});
    const [showWarning, setShowWarning] = useState(false);

    // Date constants for 2026
    const YEAR_START = new Date('2026-01-01T00:00:00');
    const YEAR_END = new Date('2026-12-31T23:59:59');
    const TODAY = new Date();
    TODAY.setHours(23, 59, 59, 999); // Set to end of today to allow all of today

    useEffect(() => {
        if (entry) {
            setFormData({
                entry_date: new Date(entry.date || entry.entry_date),
                cigarette_count: entry.cigarette_count?.toString() || '',
                location: entry.location || '',
                remarks: entry.remarks || '',
            });
            setShowWarning(false);
        } else {
            setFormData({
                entry_date: new Date(),
                cigarette_count: '',
                location: '',
                remarks: '',
            });
            checkStreakImpact(new Date());
        }
        setErrors({});
    }, [entry, visible]);

    const checkStreakImpact = (selectedDate) => {
        if (!entry && currentStreak > 0) {
            const dateStr = selectedDate.toISOString().split('T')[0];
            const todayStr = new Date().toISOString().split('T')[0];

            // Show warning if adding historical entry during active streak
            if (dateStr <= todayStr) {
                setShowWarning(true);
            } else {
                setShowWarning(false);
            }
        }
    };

    const validateForm = () => {
        const newErrors = {};

        if (!formData.cigarette_count || parseInt(formData.cigarette_count) < 1) {
            newErrors.cigarette_count = 'Must be at least 1';
        }

        // Date validation
        const selectedDate = new Date(formData.entry_date);
        selectedDate.setHours(0, 0, 0, 0);

        if (selectedDate < YEAR_START || selectedDate > YEAR_END) {
            newErrors.entry_date = 'Date must be within 2026';
        } else if (selectedDate > TODAY) {
            newErrors.entry_date = 'Cannot add future smoking entries';
        }

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleSave = () => {
        if (validateForm()) {
            // Format date as YYYY-MM-DD for backend
            const dateStr = formData.entry_date.toISOString().split('T')[0];
            const dataToSave = {
                date: dateStr,
                cigarette_count: parseInt(formData.cigarette_count),
                location: formData.location || null,
                remarks: formData.remarks || null,
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
        if (selectedDate && event.type !== 'dismissed') {
            // Set to midnight to avoid timezone issues
            const normalizedDate = new Date(selectedDate);
            normalizedDate.setHours(0, 0, 0, 0);
            setFormData({ ...formData, entry_date: normalizedDate });
            checkStreakImpact(normalizedDate);
        }
    };

    return (
        <Portal>
            <Dialog visible={visible} onDismiss={onClose} style={styles.dialog}>
                <Dialog.Title>{entry ? 'Edit Entry' : 'Log Smoking Entry'}</Dialog.Title>
                <Dialog.ScrollArea>
                    <ScrollView contentContainerStyle={styles.scrollContent}>
                        {showWarning && (
                            <Banner
                                visible={showWarning}
                                icon="alert"
                                style={styles.warningBanner}
                            >
                                ⚠️ Adding this entry may affect your clean streak of {currentStreak} days.
                            </Banner>
                        )}

                        <Button
                            mode="outlined"
                            onPress={() => setShowDatePicker(true)}
                            style={styles.input}
                        >
                            Date: {formData.entry_date.toLocaleDateString()}
                        </Button>
                        <HelperText type="error" visible={!!errors.entry_date}>
                            {errors.entry_date}
                        </HelperText>

                        {showDatePicker && Platform.OS === 'web' ? (
                            <input
                                type="date"
                                value={formData.entry_date.toISOString().split('T')[0]}
                                onChange={(e) => {
                                    if (e.target.value) {
                                        const selected = new Date(e.target.value + 'T00:00:00');
                                        setFormData({ ...formData, entry_date: selected });
                                        checkStreakImpact(selected);
                                    }
                                }}
                                onBlur={() => setShowDatePicker(false)}
                                max={TODAY.toISOString().split('T')[0]}
                                min={YEAR_START.toISOString().split('T')[0]}
                                style={{
                                    padding: 12,
                                    fontSize: 16,
                                    border: '1px solid #ccc',
                                    borderRadius: 4,
                                    width: '100%',
                                    marginBottom: 8
                                }}
                            />
                        ) : showDatePicker ? (
                            <DateTimePicker
                                value={formData.entry_date}
                                mode="date"
                                display="default"
                                onChange={onDateChange}
                                maximumDate={TODAY}
                                minimumDate={YEAR_START}
                            />
                        ) : null}

                        <TextInput
                            label="Cigarettes Smoked *"
                            value={formData.cigarette_count}
                            onChangeText={(text) => setFormData({ ...formData, cigarette_count: text })}
                            mode="outlined"
                            keyboardType="numeric"
                            style={styles.input}
                            error={!!errors.cigarette_count}
                        />
                        <HelperText type="error" visible={!!errors.cigarette_count}>
                            {errors.cigarette_count}
                        </HelperText>

                        <TextInput
                            label="Location (e.g., Home, Work, Social, Other)"
                            value={formData.location}
                            onChangeText={(text) => setFormData({ ...formData, location: text })}
                            mode="outlined"
                            style={styles.input}
                        />

                        <TextInput
                            label="Remarks"
                            value={formData.remarks}
                            onChangeText={(text) => setFormData({ ...formData, remarks: text })}
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
    warningBanner: {
        marginBottom: 16,
        backgroundColor: '#fff3cd',
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
