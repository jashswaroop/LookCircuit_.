import React, { useState, useRef, useEffect } from 'react';
import {
    View,
    Text,
    StyleSheet,
    TouchableOpacity,
    SafeAreaView,
    Alert,
    Image,
    ActivityIndicator,
    Dimensions,
} from 'react-native';
import { CameraView, useCameraPermissions } from 'expo-camera';
import * as ImagePicker from 'expo-image-picker';
import { BlurView } from 'expo-blur';
import { Camera, RotateCcw, Check, Shield, Upload, Image as ImageIcon } from 'lucide-react-native';
import Animated, {
    useSharedValue,
    useAnimatedStyle,
    withRepeat,
    withTiming,
    withSequence,
    Easing,
    FadeInDown
} from 'react-native-reanimated';
import { colors, typography, layout } from '../theme';

const { width, height } = Dimensions.get('window');

const CameraScreen = ({ navigation }: any) => {
    const [permission, requestPermission] = useCameraPermissions();
    const [facing, setFacing] = useState<'front' | 'back'>('front');
    const [isCapturing, setIsCapturing] = useState(false);
    const [capturedImage, setCapturedImage] = useState<string | null>(null);
    const [showCamera, setShowCamera] = useState(false);
    const cameraRef = useRef<any>(null);

    // Animation values
    const scanLinePosition = useSharedValue(0);

    useEffect(() => {
        if (showCamera) {
            scanLinePosition.value = withRepeat(
                withTiming(280, { duration: 2000, easing: Easing.inOut(Easing.quad) }),
                -1,
                true
            );
        }
    }, [showCamera]);

    const animatedScanLineStyle = useAnimatedStyle(() => ({
        transform: [{ translateY: scanLinePosition.value }],
    }));

    const pickImage = async () => {
        const result = await ImagePicker.launchImageLibraryAsync({
            mediaTypes: ImagePicker.MediaTypeOptions.Images,
            allowsEditing: true,
            aspect: [3, 4],
            quality: 0.8,
        });

        if (!result.canceled && result.assets[0]) {
            setCapturedImage(result.assets[0].uri);
        }
    };

    const openCamera = async () => {
        if (!permission?.granted) {
            const response = await requestPermission();
            if (!response.granted) {
                Alert.alert('Permission Denied', 'Camera access is required to take photos.');
                return;
            }
        }
        setShowCamera(true);
    };

    const takePicture = async () => {
        if (cameraRef.current && !isCapturing) {
            setIsCapturing(true);
            try {
                const photo = await cameraRef.current.takePictureAsync({
                    quality: 0.8,
                    base64: true,
                });
                setCapturedImage(photo.uri);
                setShowCamera(false);
            } catch (error) {
                Alert.alert('Error', 'Failed to capture photo');
            }
            setIsCapturing(false);
        }
    };

    const retake = () => {
        setCapturedImage(null);
        setShowCamera(false);
    };

    const analyzePhoto = () => {
        navigation.navigate('Results', {
            imageUri: capturedImage,
            analysisResults: {
                skinTone: { type: 3, undertone: 'warm', hex: '#D4A574' },
                faceShape: { shape: 'oval', confidence: 0.92 },
                hairCoverage: { level: 'full', percentage: 95 },
                colorSeason: 'spring'
            }
        });
    };

    // Preview state after image selection/capture
    if (capturedImage) {
        return (
            <View style={styles.container}>
                <Image source={{ uri: capturedImage }} style={styles.preview} />
                <BlurView intensity={80} tint="dark" style={styles.previewControls}>
                    <TouchableOpacity style={styles.retakeButton} onPress={retake}>
                        <RotateCcw size={20} color={colors.text.primary} style={{ marginRight: 8 }} />
                        <Text style={styles.buttonText}>Retake</Text>
                    </TouchableOpacity>
                    <TouchableOpacity style={styles.analyzeButton} onPress={analyzePhoto}>
                        <Check size={20} color={colors.text.primary} style={{ marginRight: 8 }} />
                        <Text style={styles.buttonText}>Analyze</Text>
                    </TouchableOpacity>
                </BlurView>
            </View>
        );
    }

    // Camera view
    if (showCamera) {
        return (
            <View style={styles.container}>
                <CameraView
                    ref={cameraRef}
                    style={styles.camera}
                    facing={facing}
                >
                    {/* Face Guide Overlay */}
                    <View style={styles.overlay}>
                        <View style={styles.faceGuide}>
                            {/* Corners */}
                            <View style={[styles.corner, styles.topLeft]} />
                            <View style={[styles.corner, styles.topRight]} />
                            <View style={[styles.corner, styles.bottomLeft]} />
                            <View style={[styles.corner, styles.bottomRight]} />

                            {/* Scanning Line Animation */}
                            <Animated.View style={[styles.scanLine, animatedScanLineStyle]} />
                        </View>

                        <View style={styles.instructionPill}>
                            <Text style={styles.instructionText}>Position face in frame</Text>
                        </View>

                        {/* Privacy Indicator */}
                        <View style={styles.privacyContainer}>
                            <Shield size={12} color={colors.text.muted} style={{ marginRight: 4 }} />
                            <Text style={styles.privacyText}>Encrypted & Private</Text>
                        </View>
                    </View>
                </CameraView>

                {/* Bottom Controls */}
                <BlurView intensity={30} tint="dark" style={styles.controls}>
                    <TouchableOpacity
                        style={styles.flipButton}
                        onPress={() => setFacing(f => f === 'back' ? 'front' : 'back')}
                    >
                        <RotateCcw size={24} color={colors.text.primary} />
                    </TouchableOpacity>

                    <TouchableOpacity
                        style={[styles.captureButton, isCapturing && styles.capturing]}
                        onPress={takePicture}
                        disabled={isCapturing}
                    >
                        {isCapturing ? (
                            <ActivityIndicator color={colors.accent.primary} size="small" />
                        ) : (
                            <View style={styles.captureInner} />
                        )}
                    </TouchableOpacity>

                    <TouchableOpacity
                        style={styles.flipButton}
                        onPress={() => setShowCamera(false)}
                    >
                        <Text style={styles.cancelText}>Cancel</Text>
                    </TouchableOpacity>
                </BlurView>
            </View>
        );
    }

    // Initial selection screen
    return (
        <SafeAreaView style={styles.container}>
            <View style={styles.selectionContainer}>
                <Animated.View entering={FadeInDown.delay(200)} style={styles.header}>
                    <Text style={styles.title}>Style Analysis</Text>
                    <Text style={styles.subtitle}>Choose how you want to analyze your style</Text>
                </Animated.View>

                <View style={styles.optionsContainer}>
                    <Animated.View entering={FadeInDown.delay(400)}>
                        <TouchableOpacity
                            style={styles.optionCard}
                            onPress={openCamera}
                        >
                            <View style={[styles.iconCircle, { backgroundColor: 'rgba(99, 102, 241, 0.1)' }]}>
                                <Camera size={32} color={colors.accent.primary} />
                            </View>
                            <Text style={styles.optionTitle}>Take Photo</Text>
                            <Text style={styles.optionDescription}>
                                Capture a new photo with your camera
                            </Text>
                        </TouchableOpacity>
                    </Animated.View>

                    <Animated.View entering={FadeInDown.delay(600)}>
                        <TouchableOpacity
                            style={styles.optionCard}
                            onPress={pickImage}
                        >
                            <View style={[styles.iconCircle, { backgroundColor: 'rgba(244, 63, 94, 0.1)' }]}>
                                <Upload size={32} color={colors.accent.secondary} />
                            </View>
                            <Text style={styles.optionTitle}>Upload Photo</Text>
                            <Text style={styles.optionDescription}>
                                Choose an existing photo from your gallery
                            </Text>
                        </TouchableOpacity>
                    </Animated.View>
                </View>

                <View style={styles.tipsContainer}>
                    <Text style={styles.tipsTitle}>💡 Tips for best results</Text>
                    <Text style={styles.tipItem}>• Use well-lit photos</Text>
                    <Text style={styles.tipItem}>• Face the camera directly</Text>
                    <Text style={styles.tipItem}>• Remove sunglasses or hats</Text>
                    <Text style={styles.tipItem}>• Use recent photos</Text>
                </View>
            </View>
        </SafeAreaView>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: colors.background.primary,
    },
    selectionContainer: {
        flex: 1,
        padding: 24,
    },
    header: {
        marginTop: 20,
        marginBottom: 40,
    },
    title: {
        fontFamily: typography.fonts.h1,
        fontSize: 32,
        color: colors.text.primary,
        marginBottom: 8,
    },
    subtitle: {
        fontFamily: typography.fonts.body,
        fontSize: 16,
        color: colors.text.secondary,
        lineHeight: 24,
    },
    optionsContainer: {
        gap: 16,
    },
    optionCard: {
        backgroundColor: colors.background.elevated,
        borderRadius: layout.borderRadius.large,
        padding: 24,
        borderWidth: 1,
        borderColor: 'rgba(255,255,255,0.05)',
        alignItems: 'center',
    },
    iconCircle: {
        width: 80,
        height: 80,
        borderRadius: 40,
        justifyContent: 'center',
        alignItems: 'center',
        marginBottom: 16,
    },
    optionTitle: {
        fontFamily: typography.fonts.h3,
        fontSize: 20,
        color: colors.text.primary,
        marginBottom: 8,
    },
    optionDescription: {
        fontFamily: typography.fonts.body,
        fontSize: 14,
        color: colors.text.secondary,
        textAlign: 'center',
    },
    tipsContainer: {
        marginTop: 40,
        padding: 20,
        backgroundColor: 'rgba(99, 102, 241, 0.05)',
        borderRadius: layout.borderRadius.medium,
        borderWidth: 1,
        borderColor: 'rgba(99, 102, 241, 0.1)',
    },
    tipsTitle: {
        fontFamily: typography.fonts.h3,
        fontSize: 16,
        color: colors.text.primary,
        marginBottom: 12,
    },
    tipItem: {
        fontFamily: typography.fonts.body,
        fontSize: 14,
        color: colors.text.secondary,
        marginBottom: 6,
        lineHeight: 20,
    },
    camera: {
        flex: 1,
    },
    overlay: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
    },
    faceGuide: {
        width: 280,
        height: 360,
        position: 'relative',
    },
    scanLine: {
        position: 'absolute',
        width: '100%',
        height: 2,
        backgroundColor: colors.accent.primary,
        shadowColor: colors.accent.primary,
        shadowOffset: { width: 0, height: 0 },
        shadowOpacity: 1,
        shadowRadius: 10,
        elevation: 5,
    },
    corner: {
        position: 'absolute',
        width: 40,
        height: 40,
        borderColor: colors.accent.primary,
        opacity: 0.8,
    },
    topLeft: {
        top: 0, left: 0,
        borderTopWidth: 2, borderLeftWidth: 2,
        borderTopLeftRadius: 12,
    },
    topRight: {
        top: 0, right: 0,
        borderTopWidth: 2, borderRightWidth: 2,
        borderTopRightRadius: 12,
    },
    bottomLeft: {
        bottom: 0, left: 0,
        borderBottomWidth: 2, borderLeftWidth: 2,
        borderBottomLeftRadius: 12,
    },
    bottomRight: {
        bottom: 0, right: 0,
        borderBottomWidth: 2, borderRightWidth: 2,
        borderBottomRightRadius: 12,
    },
    instructionPill: {
        marginTop: 32,
        backgroundColor: 'rgba(0,0,0,0.6)',
        paddingHorizontal: 20,
        paddingVertical: 10,
        borderRadius: 20,
        borderWidth: 1,
        borderColor: 'rgba(255,255,255,0.1)',
    },
    instructionText: {
        color: colors.text.primary,
        fontFamily: typography.fonts.body,
        fontSize: 14,
    },
    privacyContainer: {
        position: 'absolute',
        top: 60,
        flexDirection: 'row',
        alignItems: 'center',
        opacity: 0.7,
    },
    privacyText: {
        color: colors.text.muted,
        fontSize: 10,
        fontFamily: typography.fonts.caption,
    },
    controls: {
        position: 'absolute',
        bottom: 0,
        left: 0,
        right: 0,
        height: 120,
        flexDirection: 'row',
        justifyContent: 'space-around',
        alignItems: 'center',
        paddingBottom: 20,
    },
    flipButton: {
        width: 50,
        height: 50,
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: 'rgba(255,255,255,0.1)',
        borderRadius: 25,
    },
    cancelText: {
        color: colors.text.primary,
        fontFamily: typography.fonts.body,
        fontSize: 14,
    },
    captureButton: {
        width: 80,
        height: 80,
        borderRadius: 40,
        borderWidth: 4,
        borderColor: 'rgba(255,255,255,0.3)',
        justifyContent: 'center',
        alignItems: 'center',
    },
    capturing: {
        opacity: 0.6,
    },
    captureInner: {
        width: 64,
        height: 64,
        borderRadius: 32,
        backgroundColor: colors.text.primary,
    },
    preview: {
        flex: 1,
        resizeMode: 'cover',
    },
    previewControls: {
        position: 'absolute',
        bottom: 0,
        left: 0,
        right: 0,
        flexDirection: 'row',
        justifyContent: 'space-around',
        paddingVertical: 40,
        paddingBottom: 60,
    },
    retakeButton: {
        flexDirection: 'row',
        alignItems: 'center',
        paddingHorizontal: 24,
        paddingVertical: 12,
        backgroundColor: colors.background.elevated,
        borderRadius: layout.borderRadius.medium,
    },
    analyzeButton: {
        flexDirection: 'row',
        alignItems: 'center',
        paddingHorizontal: 24,
        paddingVertical: 12,
        backgroundColor: colors.accent.primary,
        borderRadius: layout.borderRadius.medium,
    },
    buttonText: {
        color: colors.text.primary,
        fontSize: 16,
        fontFamily: typography.fonts.h3,
    },
});

export default CameraScreen;
