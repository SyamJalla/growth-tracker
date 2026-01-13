import React from 'react';
import { View, StyleSheet } from 'react-native';
import { Button, Paragraph } from 'react-native-paper';
import { MaterialCommunityIcons } from '@expo/vector-icons';

export default function ErrorMessage({ message, onRetry }) {
    return (
        <View style={styles.container}>
            <MaterialCommunityIcons name="alert-circle" size={60} color="#F44336" />
            <Paragraph style={styles.message}>{message}</Paragraph>
            {onRetry && (
                <Button mode="contained" onPress={onRetry} style={styles.button}>
                    Retry
                </Button>
            )}
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        padding: 20,
        backgroundColor: '#f5f5f5',
    },
    message: {
        fontSize: 16,
        color: '#666',
        textAlign: 'center',
        marginTop: 15,
        marginBottom: 20,
    },
    button: {
        backgroundColor: '#2196F3',
    },
});
