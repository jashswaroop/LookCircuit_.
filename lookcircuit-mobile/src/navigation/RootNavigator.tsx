import React from 'react';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import WelcomeScreen from '../screens/WelcomeScreen';
import MainNavigator from './MainNavigator';
import ResultsScreen from '../screens/ResultsScreen';
import RecommendationsScreen from '../screens/RecommendationsScreen';
import { colors } from '../theme';

const Stack = createNativeStackNavigator();

const RootNavigator = () => {
    return (
        <Stack.Navigator
            initialRouteName="Welcome"
            screenOptions={{
                headerShown: false,
                contentStyle: { backgroundColor: colors.background.primary },
                animation: 'fade',
            }}
        >
            <Stack.Screen name="Welcome" component={WelcomeScreen} />
            <Stack.Screen
                name="Main"
                component={MainNavigator}
                options={{ animation: 'slide_from_right' }}
            />
            <Stack.Screen
                name="Results"
                component={ResultsScreen}
                options={{
                    headerShown: true,
                    title: 'Analysis Results',
                    headerStyle: { backgroundColor: colors.background.surface },
                    headerTintColor: colors.text.primary,
                    presentation: 'modal'
                }}
            />
            <Stack.Screen
                name="Recommendations"
                component={RecommendationsScreen}
                options={{
                    headerShown: true,
                    title: 'Style Guide',
                    headerStyle: { backgroundColor: colors.background.surface },
                    headerTintColor: colors.text.primary,
                }}
            />
        </Stack.Navigator>
    );
};

export default RootNavigator;
