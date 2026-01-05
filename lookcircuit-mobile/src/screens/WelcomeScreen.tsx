import React, { useState, useEffect } from 'react';
import {
    View,
    Text,
    StyleSheet,
    TouchableOpacity,
    Dimensions,
    TextInput,
    KeyboardAvoidingView,
    Platform,
    Alert
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { StatusBar } from 'expo-status-bar';
import Animated, {
    useSharedValue,
    useAnimatedStyle,
    withRepeat,
    withTiming,
    withSequence,
    Easing,
    FadeInDown,
    SlideInDown,
    SlideOutDown
} from 'react-native-reanimated';
import { Mail, Lock, ArrowRight, X } from 'lucide-react-native';
import { BlurView } from 'expo-blur';

import { colors, typography, layout } from '../theme';

const { width, height } = Dimensions.get('window');

const WelcomeScreen = ({ navigation }: any) => {
    const [showEmailLogin, setShowEmailLogin] = useState(false);
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    // Animation for logo
    const logoRotation = useSharedValue(0);
    const logoScale = useSharedValue(1);

    useEffect(() => {
        logoRotation.value = withRepeat(
            withSequence(
                withTiming(10, { duration: 2000, easing: Easing.inOut(Easing.quad) }),
                withTiming(-10, { duration: 2000, easing: Easing.inOut(Easing.quad) })
            ),
            -1,
            true
        );
        logoScale.value = withRepeat(
            withSequence(
                withTiming(1.1, { duration: 3000 }),
                withTiming(1, { duration: 3000 })
            ),
            -1,
            true
        );
    }, []);

    const animatedLogoStyle = useAnimatedStyle(() => ({
        transform: [
            { rotate: `${logoRotation.value}deg` },
            { scale: logoScale.value }
        ],
    }));

    const handleSkip = () => {
        navigation.replace('Main');
    };

    const handleLogin = () => {
        if (email && password) {
            // Mock login
            navigation.replace('Main');
        } else {
            Alert.alert('Error', 'Please enter email and password');
        }
    };

    return (
        <View style={styles.container}>
            <StatusBar style="light" />

            {/* Background Gradient */}
            <LinearGradient
                colors={[colors.accent.primary, colors.background.primary, colors.accent.secondary]}
                start={{ x: 0, y: 0 }}
                end={{ x: 1, y: 1 }}
                style={StyleSheet.absoluteFill}
                opacity={0.8}
            />
            <View style={styles.overlay} />

            <SafeAreaView style={styles.safeArea}>
                <View style={styles.content}>
                    {/* Logo Section */}
                    <View style={styles.logoSection}>
                        <Animated.View style={[styles.logoContainer, animatedLogoStyle]}>
                            <View style={styles.logoDiamond} />
                            <View style={styles.logoInner} />
                        </Animated.View>
                        <Text style={styles.brandName}>LookCircuit</Text>
                        <Text style={styles.tagline}>Your AI Style Consultant</Text>
                    </View>

                    {/* Auth Options */}
                    <Animated.View
                        entering={FadeInDown.delay(500).duration(1000)}
                        style={styles.authContainer}
                    >
                        <TouchableOpacity
                            style={[styles.button, styles.googleButton]}
                            onPress={handleSkip}
                        >
                            <Text style={styles.buttonText}>Continue with Google</Text>
                        </TouchableOpacity>

                        <View style={styles.divider}>
                            <View style={styles.line} />
                            <Text style={styles.orText}>or</Text>
                            <View style={styles.line} />
                        </View>

                        <TouchableOpacity
                            style={[styles.button, styles.emailButton]}
                            onPress={() => setShowEmailLogin(true)}
                        >
                            <Mail size={20} color={colors.text.primary} style={{ marginRight: 10 }} />
                            <Text style={styles.buttonText}>Enter your email</Text>
                        </TouchableOpacity>

                        <TouchableOpacity style={styles.skipButton} onPress={handleSkip}>
                            <Text style={styles.skipText}>Skip for now →</Text>
                        </TouchableOpacity>
                    </Animated.View>
                </View>
            </SafeAreaView>

            {/* Password Modal / Email Login Sheet */}
            {showEmailLogin && (
                <Animated.View
                    style={StyleSheet.absoluteFill}
                    entering={FadeInDown}
                    exiting={SlideOutDown}
                >
                    <BlurView intensity={20} tint="dark" style={StyleSheet.absoluteFill}>
                        <KeyboardAvoidingView
                            behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
                            style={styles.modalContainer}
                        >
                            <View style={styles.modalContent}>
                                <TouchableOpacity
                                    style={styles.closeButton}
                                    onPress={() => setShowEmailLogin(false)}
                                >
                                    <X size={24} color={colors.text.muted} />
                                </TouchableOpacity>

                                <Text style={styles.modalTitle}>Welcome back</Text>

                                <View style={styles.inputContainer}>
                                    <Mail size={20} color={colors.text.muted} style={styles.inputIcon} />
                                    <TextInput
                                        style={styles.input}
                                        placeholder="Email address"
                                        placeholderTextColor={colors.text.muted}
                                        value={email}
                                        onChangeText={setEmail}
                                        autoCapitalize="none"
                                        keyboardType="email-address"
                                    />
                                </View>

                                <View style={styles.inputContainer}>
                                    <Lock size={20} color={colors.text.muted} style={styles.inputIcon} />
                                    <TextInput
                                        style={styles.input}
                                        placeholder="Password"
                                        placeholderTextColor={colors.text.muted}
                                        value={password}
                                        onChangeText={setPassword}
                                        secureTextEntry
                                    />
                                </View>

                                <TouchableOpacity
                                    style={[styles.button, styles.loginButton]}
                                    onPress={handleLogin}
                                >
                                    <Text style={styles.buttonText}>Continue</Text>
                                    <ArrowRight size={20} color={colors.text.primary} style={{ marginLeft: 8 }} />
                                </TouchableOpacity>

                                <TouchableOpacity style={styles.forgotButton}>
                                    <Text style={styles.forgotText}>Forgot password?</Text>
                                </TouchableOpacity>
                            </View>
                        </KeyboardAvoidingView>
                    </BlurView>
                </Animated.View>
            )}
        </View>
    );
};

// Simplified SafeArea for plain View usage if standard SafeAreaView has issues with full screen backgrounds
const SafeAreaView = ({ style, children }: any) => (
    <View style={[style, { paddingTop: 60, paddingBottom: 40 }]}>{children}</View>
);

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: colors.background.primary,
    },
    overlay: {
        ...StyleSheet.absoluteFillObject,
        backgroundColor: 'rgba(9, 9, 11, 0.85)', // Void black overlay to darken gradient
    },
    safeArea: {
        flex: 1,
    },
    content: {
        flex: 1,
        justifyContent: 'space-between',
        paddingHorizontal: 24,
    },
    logoSection: {
        alignItems: 'center',
        marginTop: height * 0.15,
    },
    logoContainer: {
        width: 80,
        height: 80,
        justifyContent: 'center',
        alignItems: 'center',
        marginBottom: 24,
    },
    logoDiamond: {
        width: 60,
        height: 60,
        borderWidth: 2,
        borderColor: colors.accent.primary,
        transform: [{ rotate: '45deg' }],
        shadowColor: colors.accent.primary,
        shadowOffset: { width: 0, height: 0 },
        shadowOpacity: 0.8,
        shadowRadius: 20,
        elevation: 10,
        backgroundColor: 'rgba(99, 102, 241, 0.2)',
    },
    logoInner: {
        position: 'absolute',
        width: 30,
        height: 30,
        backgroundColor: colors.accent.secondary,
        transform: [{ rotate: '45deg' }],
        shadowColor: colors.accent.secondary,
        shadowOffset: { width: 0, height: 0 },
        shadowOpacity: 0.8,
        shadowRadius: 15,
        elevation: 10,
    },
    brandName: {
        fontFamily: typography.fonts.display,
        fontSize: typography.sizes.display,
        color: colors.text.primary,
        marginBottom: 8,
    },
    tagline: {
        fontFamily: typography.fonts.body,
        fontSize: typography.sizes.body,
        color: colors.text.secondary,
        letterSpacing: 1,
    },
    authContainer: {
        width: '100%',
        marginBottom: 40,
    },
    button: {
        flexDirection: 'row',
        height: 56,
        borderRadius: layout.borderRadius.medium,
        justifyContent: 'center',
        alignItems: 'center',
        marginBottom: 16,
    },
    googleButton: {
        backgroundColor: colors.background.elevated,
        borderWidth: 1,
        borderColor: 'rgba(255,255,255,0.1)',
    },
    emailButton: {
        backgroundColor: 'rgba(255,255,255,0.05)',
        borderWidth: 1,
        borderColor: 'rgba(255,255,255,0.1)',
    },
    loginButton: {
        backgroundColor: colors.accent.primary,
        marginTop: 24,
        width: '100%',
    },
    buttonText: {
        fontFamily: typography.fonts.h3,
        fontSize: 16,
        color: colors.text.primary,
    },
    divider: {
        flexDirection: 'row',
        alignItems: 'center',
        marginVertical: 20,
    },
    line: {
        flex: 1,
        height: 1,
        backgroundColor: 'rgba(255,255,255,0.1)',
    },
    orText: {
        color: colors.text.muted,
        marginHorizontal: 16,
        fontFamily: typography.fonts.caption,
    },
    skipButton: {
        alignItems: 'center',
        marginTop: 8,
        padding: 10,
    },
    skipText: {
        color: colors.text.secondary,
        fontFamily: typography.fonts.body,
    },

    // Modal Styles
    modalContainer: {
        flex: 1,
        justifyContent: 'flex-end',
    },
    modalContent: {
        backgroundColor: colors.background.elevated,
        borderTopLeftRadius: 24,
        borderTopRightRadius: 24,
        padding: 24,
        paddingTop: 32,
        paddingBottom: 50,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: -4 },
        shadowOpacity: 0.3,
        shadowRadius: 12,
        elevation: 20,
        borderTopWidth: 1,
        borderTopColor: 'rgba(255,255,255,0.1)',
    },
    modalTitle: {
        fontFamily: typography.fonts.h2,
        fontSize: 24,
        color: colors.text.primary,
        marginBottom: 24,
    },
    closeButton: {
        position: 'absolute',
        top: 20,
        right: 20,
        padding: 8,
        zIndex: 1,
    },
    inputContainer: {
        flexDirection: 'row',
        alignItems: 'center',
        backgroundColor: 'rgba(0,0,0,0.2)',
        borderRadius: layout.borderRadius.medium,
        height: 56,
        marginBottom: 16,
        paddingHorizontal: 16,
        borderWidth: 1,
        borderColor: 'rgba(255,255,255,0.05)',
    },
    inputIcon: {
        marginRight: 12,
    },
    input: {
        flex: 1,
        color: colors.text.primary,
        fontFamily: typography.fonts.body,
        fontSize: 16,
    },
    forgotButton: {
        alignItems: 'center',
        marginTop: 16,
    },
    forgotText: {
        color: colors.text.accent,
        fontFamily: typography.fonts.caption,
    },
});

export default WelcomeScreen;
