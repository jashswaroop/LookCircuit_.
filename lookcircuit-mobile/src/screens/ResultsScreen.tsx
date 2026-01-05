import React, { useEffect } from 'react';
import {
    View,
    Text,
    StyleSheet,
    ScrollView,
    SafeAreaView,
    TouchableOpacity,
    Image,
    Dimensions,
} from 'react-native';
import Animated, { FadeInDown, FadeInUp } from 'react-native-reanimated';
import { Palette, Share2, ArrowRight, User, Sliders } from 'lucide-react-native';
import { BlurView } from 'expo-blur';
import { colors, typography, layout } from '../theme';

const { width } = Dimensions.get('window');
const GAP = 12;
const PADDING = 20;

const ResultsScreen = ({ route, navigation }: any) => {
    const { imageUri, analysisResults } = route.params || {};

    const results = analysisResults || {
        skinTone: { type: 3, undertone: 'warm', hex: '#D4A574' },
        faceShape: { shape: 'oval', confidence: 0.92 },
        hairCoverage: { level: 'full', percentage: 95 },
        colorSeason: 'spring'
    };

    const fitzpatrickLabels: { [key: number]: string } = {
        1: 'Type I',
        2: 'Type II',
        3: 'Type III',
        4: 'Type IV',
        5: 'Type V',
        6: 'Type VI',
    };

    const seasonColors: { [key: string]: string[] } = {
        spring: ['#FFDAB9', '#FFD700', '#FF6347', '#98FB98'],
        summer: ['#E6E6FA', '#B0C4DE', '#DDA0DD', '#FFC0CB'],
        autumn: ['#8B4513', '#D2691E', '#556B2F', '#CD853F'],
        winter: ['#000080', '#800020', '#228B22', '#DC143C'],
    };

    const seasonPalette = seasonColors[results.colorSeason] || seasonColors.spring;

    return (
        <View style={styles.container}>
            <ScrollView showsVerticalScrollIndicator={false} contentContainerStyle={styles.scrollContent}>

                {/* Header Section */}
                <Animated.View entering={FadeInDown.duration(600)} style={styles.profileSection}>
                    <View style={styles.imageWrapper}>
                        <Image
                            source={imageUri ? { uri: imageUri } : { uri: 'https://via.placeholder.com/150' }}
                            style={styles.profileImage}
                        />
                        <View style={styles.badge}>
                            <Text style={styles.badgeText}>98% Match</Text>
                        </View>
                    </View>
                    <Text style={styles.greeting}>Analysis Complete</Text>
                    <Text style={styles.subGreeting}>Here is your style DNA</Text>
                </Animated.View>

                {/* Bento Grid */}
                <View style={styles.grid}>
                    {/* Skin Tone Card */}
                    <Animated.View entering={FadeInUp.delay(200)} style={[styles.card, styles.cardLarge]}>
                        <View style={styles.cardHeader}>
                            <View style={[styles.iconBox, { backgroundColor: 'rgba(255,100,100,0.1)' }]}>
                                <User size={20} color="#FF6F61" />
                            </View>
                            <Text style={styles.cardLabel}>SKIN TONE</Text>
                        </View>
                        <View style={styles.skinToneDisplay}>
                            <View style={[styles.skinSwatch, { backgroundColor: results.skinTone.hex }]} />
                            <View>
                                <Text style={styles.primaryValue}>{fitzpatrickLabels[results.skinTone.type]}</Text>
                                <Text style={styles.secondaryValue}>
                                    {results.skinTone.undertone.toUpperCase()} UNDERTONE
                                </Text>
                            </View>
                        </View>
                    </Animated.View>

                    {/* Face Shape Card */}
                    <Animated.View entering={FadeInUp.delay(300)} style={[styles.card, styles.cardMedium]}>
                        <View style={styles.cardHeader}>
                            <View style={[styles.iconBox, { backgroundColor: 'rgba(100,100,255,0.1)' }]}>
                                <Sliders size={20} color="#6366F1" />
                            </View>
                            <Text style={styles.cardLabel}>SHAPE</Text>
                        </View>
                        <Text style={styles.primaryValue}>
                            {results.faceShape.shape.charAt(0).toUpperCase() + results.faceShape.shape.slice(1)}
                        </Text>
                        <Text style={styles.confidenceText}>
                            {Math.round(results.faceShape.confidence * 100)}% Confidence
                        </Text>
                    </Animated.View>

                    {/* Color Season Card */}
                    <Animated.View entering={FadeInUp.delay(400)} style={[styles.card, styles.cardFull]}>
                        <View style={styles.cardHeader}>
                            <View style={[styles.iconBox, { backgroundColor: 'rgba(255,200,50,0.1)' }]}>
                                <Palette size={20} color="#F59E0B" />
                            </View>
                            <Text style={styles.cardLabel}>COLOR SEASON</Text>
                            <Text style={styles.seasonTitle}>
                                {results.colorSeason.toUpperCase()}
                            </Text>
                        </View>

                        <View style={styles.paletteRow}>
                            {seasonPalette.map((c, i) => (
                                <View key={i} style={[styles.paletteCircle, { backgroundColor: c }]} />
                            ))}
                            <View style={[styles.paletteCircle, { backgroundColor: '#333', justifyContent: 'center', alignItems: 'center' }]}>
                                <Text style={{ color: '#fff', fontSize: 10 }}>+12</Text>
                            </View>
                        </View>
                    </Animated.View>
                </View>

                {/* Actions */}
                <Animated.View entering={FadeInUp.delay(600)} style={styles.actionContainer}>
                    <TouchableOpacity
                        style={styles.primaryButton}
                        onPress={() => navigation.navigate('Recommendations', { analysisResults: results })}
                    >
                        <Text style={styles.primaryButtonText}>Discover Your Style</Text>
                        <ArrowRight size={20} color={colors.text.primary} />
                    </TouchableOpacity>

                    <TouchableOpacity style={styles.secondaryButton}>
                        <Share2 size={20} color={colors.text.secondary} />
                        <Text style={styles.secondaryButtonText}>Share Results</Text>
                    </TouchableOpacity>
                </Animated.View>

            </ScrollView>
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: colors.background.primary,
    },
    scrollContent: {
        paddingBottom: 40,
    },
    profileSection: {
        alignItems: 'center',
        paddingVertical: 30,
        backgroundColor: colors.background.surface,
        borderBottomLeftRadius: 32,
        borderBottomRightRadius: 32,
        marginBottom: 20,
    },
    imageWrapper: {
        marginBottom: 16,
        shadowColor: colors.accent.primary,
        shadowOffset: { width: 0, height: 8 },
        shadowOpacity: 0.3,
        shadowRadius: 16,
        elevation: 10,
    },
    profileImage: {
        width: 100,
        height: 100,
        borderRadius: 50,
        borderWidth: 3,
        borderColor: colors.accent.primary,
    },
    badge: {
        position: 'absolute',
        bottom: -5,
        alignSelf: 'center',
        backgroundColor: colors.accent.secondary,
        paddingHorizontal: 12,
        paddingVertical: 4,
        borderRadius: 12,
    },
    badgeText: {
        color: '#fff',
        fontSize: 10,
        fontFamily: typography.fonts.overline,
    },
    greeting: {
        fontFamily: typography.fonts.h2,
        fontSize: 24,
        color: colors.text.primary,
        marginBottom: 4,
    },
    subGreeting: {
        fontFamily: typography.fonts.body,
        fontSize: 14,
        color: colors.text.secondary,
    },

    // Grid
    grid: {
        flexDirection: 'row',
        flexWrap: 'wrap',
        paddingHorizontal: PADDING,
        gap: GAP,
    },
    card: {
        backgroundColor: colors.background.elevated,
        borderRadius: layout.borderRadius.large,
        padding: 16,
        borderWidth: 1,
        borderColor: 'rgba(255,255,255,0.05)',
    },
    cardLarge: {
        width: (width - (PADDING * 2) - GAP) * 0.6, // 60%
        height: 160,
        justifyContent: 'space-between',
    },
    cardMedium: {
        width: (width - (PADDING * 2) - GAP) * 0.4, // 40%
        height: 160,
        justifyContent: 'space-between',
    },
    cardFull: {
        width: '100%',
        height: 140,
        justifyContent: 'space-between',
    },

    // Card Internal
    cardHeader: {
        alignItems: 'flex-start',
    },
    iconBox: {
        width: 36,
        height: 36,
        borderRadius: 10,
        justifyContent: 'center',
        alignItems: 'center',
        marginBottom: 12,
    },
    cardLabel: {
        fontFamily: typography.fonts.overline,
        color: colors.text.muted,
        fontSize: 10,
        letterSpacing: 1,
        marginBottom: 4,
    },
    primaryValue: {
        fontFamily: typography.fonts.h3,
        color: colors.text.primary,
        fontSize: 18,
    },
    secondaryValue: {
        fontFamily: typography.fonts.caption,
        color: colors.text.secondary,
        fontSize: 12,
        marginTop: 2,
    },
    confidenceText: {
        fontFamily: typography.fonts.caption,
        color: colors.accent.success,
        fontSize: 12,
        marginTop: 4,
    },
    seasonTitle: {
        fontFamily: typography.fonts.h2,
        color: colors.text.primary,
        fontSize: 20,
    },

    skinToneDisplay: {
        marginTop: 10,
        flexDirection: 'row',
        alignItems: 'center',
        gap: 12,
    },
    skinSwatch: {
        width: 48,
        height: 48,
        borderRadius: 24,
        borderWidth: 2,
        borderColor: 'rgba(255,255,255,0.2)',
    },

    paletteRow: {
        flexDirection: 'row',
        gap: 12,
        marginTop: 12,
    },
    paletteCircle: {
        width: 40,
        height: 40,
        borderRadius: 20,
        borderWidth: 1,
        borderColor: 'rgba(255,255,255,0.1)',
    },

    // Actions
    actionContainer: {
        paddingHorizontal: PADDING,
        marginTop: 30,
        gap: 16,
    },
    primaryButton: {
        backgroundColor: colors.accent.primary,
        height: 56,
        borderRadius: layout.borderRadius.medium,
        flexDirection: 'row',
        justifyContent: 'center',
        alignItems: 'center',
        gap: 10,
        shadowColor: colors.accent.primary,
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.3,
        shadowRadius: 10,
        elevation: 6,
    },
    primaryButtonText: {
        fontFamily: typography.fonts.h3,
        color: '#fff',
        fontSize: 16,
    },
    secondaryButton: {
        height: 56,
        borderRadius: layout.borderRadius.medium,
        flexDirection: 'row',
        justifyContent: 'center',
        alignItems: 'center',
        gap: 10,
        backgroundColor: colors.background.element,
        borderWidth: 1,
        borderColor: 'rgba(255,255,255,0.1)',
    },
    secondaryButtonText: {
        fontFamily: typography.fonts.body,
        color: colors.text.secondary,
        fontSize: 16,
    },
});

export default ResultsScreen;
