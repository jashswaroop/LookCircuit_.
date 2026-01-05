import React from 'react';
import {
    View,
    Text,
    StyleSheet,
    TouchableOpacity,
    SafeAreaView,
    Image
} from 'react-native';

const HomeScreen = ({ navigation }: any) => {
    return (
        <SafeAreaView style={styles.container}>
            <View style={styles.header}>
                <Text style={styles.title}>LookCircuit</Text>
                <Text style={styles.subtitle}>AI-Powered Fashion Consultant</Text>
            </View>

            <View style={styles.heroSection}>
                <View style={styles.iconCircle}>
                    <Text style={styles.iconEmoji}>👔</Text>
                </View>
                <Text style={styles.heroText}>
                    Discover your perfect style based on your unique features
                </Text>
            </View>

            <View style={styles.features}>
                <View style={styles.featureItem}>
                    <Text style={styles.featureEmoji}>🎨</Text>
                    <Text style={styles.featureText}>Color Analysis</Text>
                </View>
                <View style={styles.featureItem}>
                    <Text style={styles.featureEmoji}>👤</Text>
                    <Text style={styles.featureText}>Face Shape</Text>
                </View>
                <View style={styles.featureItem}>
                    <Text style={styles.featureEmoji}>✨</Text>
                    <Text style={styles.featureText}>Style Tips</Text>
                </View>
            </View>

            <TouchableOpacity
                style={styles.ctaButton}
                onPress={() => navigation.navigate('Camera')}
            >
                <Text style={styles.ctaText}>📸 Analyze My Style</Text>
            </TouchableOpacity>

            <TouchableOpacity
                style={styles.secondaryButton}
                onPress={() => navigation.navigate('Recommendations')}
            >
                <Text style={styles.secondaryText}>View Sample Results</Text>
            </TouchableOpacity>
        </SafeAreaView>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#0f0f23',
        paddingHorizontal: 20,
    },
    header: {
        alignItems: 'center',
        marginTop: 40,
    },
    title: {
        fontSize: 36,
        fontWeight: 'bold',
        color: '#fff',
        letterSpacing: 2,
    },
    subtitle: {
        fontSize: 14,
        color: '#8b8b9a',
        marginTop: 8,
    },
    heroSection: {
        alignItems: 'center',
        marginTop: 50,
    },
    iconCircle: {
        width: 120,
        height: 120,
        borderRadius: 60,
        backgroundColor: '#1a1a2e',
        justifyContent: 'center',
        alignItems: 'center',
        borderWidth: 2,
        borderColor: '#4a4a6a',
    },
    iconEmoji: {
        fontSize: 50,
    },
    heroText: {
        fontSize: 18,
        color: '#c4c4d4',
        textAlign: 'center',
        marginTop: 20,
        paddingHorizontal: 30,
        lineHeight: 26,
    },
    features: {
        flexDirection: 'row',
        justifyContent: 'space-around',
        marginTop: 50,
        paddingHorizontal: 10,
    },
    featureItem: {
        alignItems: 'center',
        flex: 1,
    },
    featureEmoji: {
        fontSize: 32,
        marginBottom: 8,
    },
    featureText: {
        fontSize: 12,
        color: '#8b8b9a',
        textAlign: 'center',
    },
    ctaButton: {
        backgroundColor: '#6366f1',
        paddingVertical: 18,
        borderRadius: 12,
        marginTop: 60,
        alignItems: 'center',
    },
    ctaText: {
        color: '#fff',
        fontSize: 18,
        fontWeight: '600',
    },
    secondaryButton: {
        paddingVertical: 16,
        marginTop: 16,
        alignItems: 'center',
    },
    secondaryText: {
        color: '#6366f1',
        fontSize: 16,
    },
});

export default HomeScreen;
