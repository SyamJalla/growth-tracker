import React from 'react';
import { View, StyleSheet } from 'react-native';
import { Card, Title, Paragraph } from 'react-native-paper';
import { MaterialCommunityIcons } from '@expo/vector-icons';

export default function KPICard({ title, value, icon, color = '#2196F3' }) {
    return (
        <Card style={[styles.card, { borderLeftColor: color }]}>
            <Card.Content style={styles.content}>
                <View style={styles.iconContainer}>
                    <MaterialCommunityIcons name={icon} size={32} color={color} />
                </View>
                <View style={styles.textContainer}>
                    <Paragraph style={styles.title}>{title}</Paragraph>
                    <Title style={styles.value}>{value}</Title>
                </View>
            </Card.Content>
        </Card>
    );
}

const styles = StyleSheet.create({
    card: {
        width: '48%',
        marginBottom: 10,
        elevation: 3,
        borderLeftWidth: 4,
    },
    content: {
        flexDirection: 'row',
        alignItems: 'center',
    },
    iconContainer: {
        marginRight: 10,
    },
    textContainer: {
        flex: 1,
    },
    title: {
        fontSize: 12,
        color: '#666',
    },
    value: {
        fontSize: 18,
        fontWeight: 'bold',
    },
});
