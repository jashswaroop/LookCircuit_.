import React from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { BlurView } from 'expo-blur';
import { StyleSheet, View } from 'react-native';
import { Sparkles, ScanFace, ShoppingBag, Shirt, UserCircle } from 'lucide-react-native';

import HomeScreen from '../screens/HomeScreen';
import CameraScreen from '../screens/CameraScreen';
import ShopScreen from '../screens/ShopScreen';
import WardrobeScreen from '../screens/WardrobeScreen';
import ProfileScreen from '../screens/ProfileScreen';

import { colors } from '../theme';

const Tab = createBottomTabNavigator();

const MainNavigator = () => {
    return (
        <Tab.Navigator
            screenOptions={{
                headerShown: false,
                tabBarStyle: {
                    position: 'absolute',
                    bottom: 0,
                    left: 0,
                    right: 0,
                    height: 84,
                    borderTopWidth: 0,
                    elevation: 0,
                    backgroundColor: 'transparent',
                },
                tabBarBackground: () => (
                    <BlurView
                        tint="dark"
                        intensity={80}
                        style={StyleSheet.absoluteFill}
                    />
                ),
                tabBarActiveTintColor: colors.accent.primary,
                tabBarInactiveTintColor: colors.text.muted,
                tabBarShowLabel: true,
                tabBarLabelStyle: {
                    fontSize: 10,
                    fontFamily: 'Inter-Medium',
                    paddingBottom: 8,
                },
            }}
        >
            <Tab.Screen
                name="Home"
                component={HomeScreen}
                options={{
                    tabBarLabel: 'Home',
                    tabBarIcon: ({ color, size }) => (
                        <Sparkles size={24} color={color} strokeWidth={1.5} />
                    ),
                }}
            />
            <Tab.Screen
                name="Scan"
                component={CameraScreen}
                options={{
                    tabBarLabel: 'Analyze',
                    tabBarIcon: ({ color, size }) => (
                        <ScanFace size={24} color={color} strokeWidth={1.5} />
                    ),
                }}
            />
            <Tab.Screen
                name="Shop"
                component={ShopScreen}
                options={{
                    tabBarLabel: 'Discover',
                    tabBarIcon: ({ color, size }) => (
                        <ShoppingBag size={24} color={color} strokeWidth={1.5} />
                    ),
                }}
            />
            <Tab.Screen
                name="Closet"
                component={WardrobeScreen}
                options={{
                    tabBarLabel: 'Wardrobe',
                    tabBarIcon: ({ color, size }) => (
                        <Shirt size={24} color={color} strokeWidth={1.5} />
                    ),
                }}
            />
            <Tab.Screen
                name="Profile"
                component={ProfileScreen}
                options={{
                    tabBarLabel: 'You',
                    tabBarIcon: ({ color, size }) => (
                        <UserCircle size={24} color={color} strokeWidth={1.5} />
                    ),
                }}
            />
        </Tab.Navigator>
    );
};

export default MainNavigator;
