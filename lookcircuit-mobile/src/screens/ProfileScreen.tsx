import React from 'react';
import {
    View,
    Text,
    StyleSheet,
    ScrollView,
    SafeAreaView,
    TouchableOpacity,
    Image,
    Switch,
} from 'react-native';
import Animated, { FadeInDown } from 'react-native-reanimated';
import { User, Crown, Settings, LogOut, ChevronRight, Bell, Lock, Palette } from 'lucide-react-native';
import { colors, typography, layout } from '../theme';

const ProfileScreen = () => {
    const [notificationsEnabled, setNotificationsEnabled] = React.useState(true);

    const analysisData = {
        skinTone: 'Type III',
        faceShape: 'Oval',
        colorSeason: 'Spring',
        totalAnalyses: 12,
    };

    const MenuItem = ({ icon: Icon, title, subtitle, onPress, showChevron = true }: any) => (
        <TouchableOpacity style={styles.menuItem} onPress={onPress}>
            <View style={styles.menuIconContainer}>
                <Icon size={20} color={colors.accent.primary} />
            </View>
            <View style={styles.menuContent}>
                <Text style={styles.menuTitle}>{title}</Text>
                {subtitle && <Text style={styles.menuSubtitle}>{subtitle}</Text>}
            </View>
            {showChevron && <ChevronRight size={20} color={colors.text.muted} />}
        </TouchableOpacity>
    );

    return (
        <SafeAreaView style={styles.container}>
            <ScrollView showsVerticalScrollIndicator={false} contentContainerStyle={styles.scrollContent}>

                {/* Profile Header */}
                <Animated.View entering={FadeInDown.duration(600)} style={styles.profileHeader}>
                    <View style={styles.avatarContainer}>
                        <Image
                            source={{ uri: 'https://via.placeholder.com/100' }}
                            style={styles.avatar}
                        />
                        <TouchableOpacity style={styles.editAvatarButton}>
                            <User size={16} color={colors.text.primary} />
                        </TouchableOpacity>
                    </View>
                    <Text style={styles.userName}>John Doe</Text>
                    <Text style={styles.userEmail}>john.doe@example.com</Text>

                    <TouchableOpacity style={styles.premiumBadge}>
                        <Crown size={16} color="#F59E0B" />
                        <Text style={styles.premiumText}>Upgrade to Premium</Text>
                    </TouchableOpacity>
                </Animated.View>

                {/* Style DNA Summary */}
                <Animated.View entering={FadeInDown.delay(200)} style={styles.section}>
                    <Text style={styles.sectionTitle}>Your Style DNA</Text>
                    <View style={styles.dnaCard}>
                        <View style={styles.dnaRow}>
                            <View style={styles.dnaItem}>
                                <Text style={styles.dnaLabel}>Skin Tone</Text>
                                <Text style={styles.dnaValue}>{analysisData.skinTone}</Text>
                            </View>
                            <View style={styles.dnaItem}>
                                <Text style={styles.dnaLabel}>Face Shape</Text>
                                <Text style={styles.dnaValue}>{analysisData.faceShape}</Text>
                            </View>
                        </View>
                        <View style={styles.dnaRow}>
                            <View style={styles.dnaItem}>
                                <Text style={styles.dnaLabel}>Color Season</Text>
                                <Text style={styles.dnaValue}>{analysisData.colorSeason}</Text>
                            </View>
                            <View style={styles.dnaItem}>
                                <Text style={styles.dnaLabel}>Total Scans</Text>
                                <Text style={styles.dnaValue}>{analysisData.totalAnalyses}</Text>
                            </View>
                        </View>
                        <TouchableOpacity style={styles.updateButton}>
                            <Text style={styles.updateButtonText}>Update Analysis</Text>
                        </TouchableOpacity>
                    </View>
                </Animated.View>

                {/* Preferences */}
                <Animated.View entering={FadeInDown.delay(400)} style={styles.section}>
                    <Text style={styles.sectionTitle}>Preferences</Text>
                    <View style={styles.menuCard}>
                        <View style={styles.menuItem}>
                            <View style={styles.menuIconContainer}>
                                <Bell size={20} color={colors.accent.primary} />
                            </View>
                            <View style={styles.menuContent}>
                                <Text style={styles.menuTitle}>Notifications</Text>
                                <Text style={styles.menuSubtitle}>Get style tips and updates</Text>
                            </View>
                            <Switch
                                value={notificationsEnabled}
                                onValueChange={setNotificationsEnabled}
                                trackColor={{ false: colors.background.surface, true: colors.accent.primary }}
                                thumbColor={colors.text.primary}
                            />
                        </View>
                        <View style={styles.divider} />
                        <MenuItem
                            icon={Palette}
                            title="Color Preferences"
                            subtitle="Manage your color palette"
                            onPress={() => { }}
                        />
                        <View style={styles.divider} />
                        <MenuItem
                            icon={Lock}
                            title="Privacy & Security"
                            subtitle="Control your data"
                            onPress={() => { }}
                        />
                    </View>
                </Animated.View>

                {/* Account */}
                <Animated.View entering={FadeInDown.delay(600)} style={styles.section}>
                    <Text style={styles.sectionTitle}>Account</Text>
                    <View style={styles.menuCard}>
                        <MenuItem
                            icon={Settings}
                            title="Settings"
                            subtitle="App preferences and more"
                            onPress={() => { }}
                        />
                        <View style={styles.divider} />
                        <TouchableOpacity style={styles.menuItem}>
                            <View style={[styles.menuIconContainer, { backgroundColor: 'rgba(244, 63, 94, 0.1)' }]}>
                                <LogOut size={20} color={colors.accent.secondary} />
                            </View>
                            <View style={styles.menuContent}>
                                <Text style={[styles.menuTitle, { color: colors.accent.secondary }]}>Log Out</Text>
                            </View>
                        </TouchableOpacity>
                    </View>
                </Animated.View>

                <Text style={styles.version}>Version 1.0.0 (MVP)</Text>
            </ScrollView>
        </SafeAreaView>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: colors.background.primary,
    },
    scrollContent: {
        paddingBottom: 100,
    },
    profileHeader: {
        alignItems: 'center',
        paddingVertical: 32,
        paddingHorizontal: 24,
    },
    avatarContainer: {
        position: 'relative',
        marginBottom: 16,
    },
    avatar: {
        width: 100,
        height: 100,
        borderRadius: 50,
        borderWidth: 3,
        borderColor: colors.accent.primary,
    },
    editAvatarButton: {
        position: 'absolute',
        bottom: 0,
        right: 0,
        width: 32,
        height: 32,
        backgroundColor: colors.accent.primary,
        borderRadius: 16,
        justifyContent: 'center',
        alignItems: 'center',
        borderWidth: 3,
        borderColor: colors.background.primary,
    },
    userName: {
        fontFamily: typography.fonts.h2,
        fontSize: 24,
        color: colors.text.primary,
        marginBottom: 4,
    },
    userEmail: {
        fontFamily: typography.fonts.body,
        fontSize: 14,
        color: colors.text.secondary,
        marginBottom: 16,
    },
    premiumBadge: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: 8,
        paddingHorizontal: 20,
        paddingVertical: 10,
        backgroundColor: 'rgba(245, 158, 11, 0.1)',
        borderRadius: layout.borderRadius.round,
        borderWidth: 1,
        borderColor: 'rgba(245, 158, 11, 0.3)',
    },
    premiumText: {
        fontFamily: typography.fonts.h3,
        fontSize: 14,
        color: '#F59E0B',
    },
    section: {
        paddingHorizontal: 24,
        marginBottom: 24,
    },
    sectionTitle: {
        fontFamily: typography.fonts.h3,
        fontSize: 16,
        color: colors.text.primary,
        marginBottom: 12,
    },
    dnaCard: {
        backgroundColor: colors.background.elevated,
        borderRadius: layout.borderRadius.large,
        padding: 20,
        borderWidth: 1,
        borderColor: 'rgba(255,255,255,0.05)',
    },
    dnaRow: {
        flexDirection: 'row',
        marginBottom: 16,
        gap: 16,
    },
    dnaItem: {
        flex: 1,
    },
    dnaLabel: {
        fontFamily: typography.fonts.caption,
        fontSize: 11,
        color: colors.text.muted,
        textTransform: 'uppercase',
        letterSpacing: 1,
        marginBottom: 4,
    },
    dnaValue: {
        fontFamily: typography.fonts.h3,
        fontSize: 18,
        color: colors.text.primary,
    },
    updateButton: {
        backgroundColor: colors.accent.primary,
        paddingVertical: 12,
        borderRadius: layout.borderRadius.medium,
        alignItems: 'center',
        marginTop: 4,
    },
    updateButtonText: {
        fontFamily: typography.fonts.h3,
        fontSize: 14,
        color: colors.text.primary,
    },
    menuCard: {
        backgroundColor: colors.background.elevated,
        borderRadius: layout.borderRadius.large,
        overflow: 'hidden',
        borderWidth: 1,
        borderColor: 'rgba(255,255,255,0.05)',
    },
    menuItem: {
        flexDirection: 'row',
        alignItems: 'center',
        padding: 16,
        gap: 12,
    },
    menuIconContainer: {
        width: 40,
        height: 40,
        backgroundColor: 'rgba(99, 102, 241, 0.1)',
        borderRadius: 12,
        justifyContent: 'center',
        alignItems: 'center',
    },
    menuContent: {
        flex: 1,
    },
    menuTitle: {
        fontFamily: typography.fonts.h3,
        fontSize: 16,
        color: colors.text.primary,
        marginBottom: 2,
    },
    menuSubtitle: {
        fontFamily: typography.fonts.caption,
        fontSize: 12,
        color: colors.text.secondary,
    },
    divider: {
        height: 1,
        backgroundColor: 'rgba(255,255,255,0.05)',
        marginLeft: 68,
    },
    version: {
        fontFamily: typography.fonts.caption,
        fontSize: 12,
        color: colors.text.muted,
        textAlign: 'center',
        marginTop: 20,
    },
});

export default ProfileScreen;
