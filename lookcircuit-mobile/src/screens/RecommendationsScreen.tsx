import React, { useState } from 'react';
import {
    View,
    Text,
    StyleSheet,
    ScrollView,
    SafeAreaView,
    TouchableOpacity,
} from 'react-native';

const RecommendationsScreen = ({ route }: any) => {
    const { analysisResults } = route.params || {};
    const [activeTab, setActiveTab] = useState('colors');

    // Mock recommendations based on analysis
    const recommendations = {
        colors: {
            best: ['#FFDAB9', '#FFD700', '#FF6347', '#98FB98', '#87CEEB'],
            avoid: ['#000000', '#4A0000', '#2F4F4F'],
            metal: 'Gold',
        },
        style: {
            necklines: ['V-neck', 'Crew', 'Scoop', 'Boat'],
            patterns: ['Solid colors', 'Medium patterns', 'Subtle prints'],
            fits: ['Slim', 'Regular', 'Tailored'],
        },
        grooming: {
            hairstyles: ['Side part', 'Pompadour', 'Textured crop', 'Slick back'],
            beard: ['Stubble', 'Short beard', 'Full beard'],
        },
        occasions: [
            { name: 'Casual', outfit: 'Polo shirt + Chinos + Loafers' },
            { name: 'Formal', outfit: 'Dress shirt + Suit + Oxford shoes' },
            { name: 'Date Night', outfit: 'Fitted shirt + Dark jeans + Chelsea boots' },
        ],
    };

    const tabs = [
        { id: 'colors', label: '🎨 Colors' },
        { id: 'style', label: '👔 Style' },
        { id: 'grooming', label: '💇 Grooming' },
        { id: 'occasions', label: '📅 Occasions' },
    ];

    const renderColors = () => (
        <View style={styles.section}>
            <Text style={styles.sectionTitle}>Best Colors For You</Text>
            <View style={styles.colorGrid}>
                {recommendations.colors.best.map((color, index) => (
                    <View key={index} style={styles.colorItem}>
                        <View style={[styles.colorCircle, { backgroundColor: color }]} />
                    </View>
                ))}
            </View>

            <Text style={[styles.sectionTitle, { marginTop: 24 }]}>Colors To Avoid</Text>
            <View style={styles.colorGrid}>
                {recommendations.colors.avoid.map((color, index) => (
                    <View key={index} style={styles.colorItem}>
                        <View style={[styles.colorCircle, styles.avoidCircle, { backgroundColor: color }]} />
                    </View>
                ))}
            </View>

            <View style={styles.metalCard}>
                <Text style={styles.metalLabel}>Metal Preference</Text>
                <Text style={styles.metalValue}>✨ {recommendations.colors.metal}</Text>
            </View>
        </View>
    );

    const renderStyle = () => (
        <View style={styles.section}>
            <Text style={styles.sectionTitle}>Recommended Necklines</Text>
            <View style={styles.tagContainer}>
                {recommendations.style.necklines.map((item, index) => (
                    <View key={index} style={styles.tag}>
                        <Text style={styles.tagText}>{item}</Text>
                    </View>
                ))}
            </View>

            <Text style={[styles.sectionTitle, { marginTop: 24 }]}>Patterns</Text>
            <View style={styles.tagContainer}>
                {recommendations.style.patterns.map((item, index) => (
                    <View key={index} style={styles.tag}>
                        <Text style={styles.tagText}>{item}</Text>
                    </View>
                ))}
            </View>

            <Text style={[styles.sectionTitle, { marginTop: 24 }]}>Best Fits</Text>
            <View style={styles.tagContainer}>
                {recommendations.style.fits.map((item, index) => (
                    <View key={index} style={styles.tag}>
                        <Text style={styles.tagText}>{item}</Text>
                    </View>
                ))}
            </View>
        </View>
    );

    const renderGrooming = () => (
        <View style={styles.section}>
            <Text style={styles.sectionTitle}>Hairstyles</Text>
            {recommendations.grooming.hairstyles.map((item, index) => (
                <View key={index} style={styles.listItem}>
                    <Text style={styles.listBullet}>•</Text>
                    <Text style={styles.listText}>{item}</Text>
                </View>
            ))}

            <Text style={[styles.sectionTitle, { marginTop: 24 }]}>Beard Styles</Text>
            {recommendations.grooming.beard.map((item, index) => (
                <View key={index} style={styles.listItem}>
                    <Text style={styles.listBullet}>•</Text>
                    <Text style={styles.listText}>{item}</Text>
                </View>
            ))}
        </View>
    );

    const renderOccasions = () => (
        <View style={styles.section}>
            {recommendations.occasions.map((occasion, index) => (
                <View key={index} style={styles.occasionCard}>
                    <Text style={styles.occasionName}>{occasion.name}</Text>
                    <Text style={styles.occasionOutfit}>{occasion.outfit}</Text>
                </View>
            ))}
        </View>
    );

    return (
        <SafeAreaView style={styles.container}>
            {/* Tabs */}
            <View style={styles.tabBar}>
                {tabs.map((tab) => (
                    <TouchableOpacity
                        key={tab.id}
                        style={[styles.tab, activeTab === tab.id && styles.activeTab]}
                        onPress={() => setActiveTab(tab.id)}
                    >
                        <Text style={[styles.tabText, activeTab === tab.id && styles.activeTabText]}>
                            {tab.label}
                        </Text>
                    </TouchableOpacity>
                ))}
            </View>

            {/* Content */}
            <ScrollView showsVerticalScrollIndicator={false}>
                {activeTab === 'colors' && renderColors()}
                {activeTab === 'style' && renderStyle()}
                {activeTab === 'grooming' && renderGrooming()}
                {activeTab === 'occasions' && renderOccasions()}
            </ScrollView>
        </SafeAreaView>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#0f0f23',
    },
    tabBar: {
        flexDirection: 'row',
        backgroundColor: '#1a1a2e',
        paddingVertical: 4,
        paddingHorizontal: 8,
        marginHorizontal: 16,
        marginTop: 10,
        borderRadius: 12,
    },
    tab: {
        flex: 1,
        paddingVertical: 10,
        alignItems: 'center',
        borderRadius: 8,
    },
    activeTab: {
        backgroundColor: '#6366f1',
    },
    tabText: {
        fontSize: 12,
        color: '#8b8b9a',
    },
    activeTabText: {
        color: '#fff',
        fontWeight: '600',
    },
    section: {
        padding: 20,
    },
    sectionTitle: {
        fontSize: 14,
        color: '#8b8b9a',
        marginBottom: 16,
        textTransform: 'uppercase',
        letterSpacing: 1,
    },
    colorGrid: {
        flexDirection: 'row',
        flexWrap: 'wrap',
        gap: 16,
    },
    colorItem: {
        alignItems: 'center',
    },
    colorCircle: {
        width: 50,
        height: 50,
        borderRadius: 25,
        borderWidth: 2,
        borderColor: 'rgba(255,255,255,0.2)',
    },
    avoidCircle: {
        borderWidth: 2,
        borderColor: '#ff4444',
    },
    metalCard: {
        backgroundColor: '#1a1a2e',
        padding: 16,
        borderRadius: 12,
        marginTop: 24,
        alignItems: 'center',
    },
    metalLabel: {
        fontSize: 12,
        color: '#8b8b9a',
        marginBottom: 8,
    },
    metalValue: {
        fontSize: 20,
        color: '#FFD700',
        fontWeight: 'bold',
    },
    tagContainer: {
        flexDirection: 'row',
        flexWrap: 'wrap',
        gap: 10,
    },
    tag: {
        backgroundColor: '#1a1a2e',
        paddingHorizontal: 16,
        paddingVertical: 10,
        borderRadius: 20,
        borderWidth: 1,
        borderColor: '#6366f1',
    },
    tagText: {
        color: '#fff',
        fontSize: 14,
    },
    listItem: {
        flexDirection: 'row',
        alignItems: 'center',
        paddingVertical: 8,
    },
    listBullet: {
        color: '#6366f1',
        fontSize: 18,
        marginRight: 12,
    },
    listText: {
        color: '#fff',
        fontSize: 16,
    },
    occasionCard: {
        backgroundColor: '#1a1a2e',
        padding: 20,
        borderRadius: 12,
        marginBottom: 12,
    },
    occasionName: {
        fontSize: 18,
        color: '#fff',
        fontWeight: 'bold',
        marginBottom: 8,
    },
    occasionOutfit: {
        fontSize: 14,
        color: '#a0a0b0',
        lineHeight: 20,
    },
});

export default RecommendationsScreen;
