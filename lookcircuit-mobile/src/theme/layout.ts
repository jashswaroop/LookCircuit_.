// LookCircuit Design System - Layout & Spacing
// Based on PRD v1.0

export const layout = {
    borderRadius: {
        small: 8,    // Icons
        medium: 12,  // Buttons, Inputs
        large: 20,   // Cards
        xl: 28,      // Hero Cards
        round: 9999, // Pills, Avatars
    },

    spacing: {
        xs: 4,
        s: 8,
        m: 16,
        l: 24,
        xl: 32,
        xxl: 48,
    },

    shadows: {
        // Note: React Native shadows work differently on iOS vs Android
        // These are approximations, standard elevation is used for Android
        level1: {
            shadowColor: '#000',
            shadowOffset: { width: 0, height: 4 },
            shadowOpacity: 0.4,
            shadowRadius: 24,
            elevation: 4,
        },
        level2: {
            shadowColor: '#000',
            shadowOffset: { width: 0, height: 8 },
            shadowOpacity: 0.6,
            shadowRadius: 32,
            elevation: 8,
        },
        level3: {
            shadowColor: '#000',
            shadowOffset: { width: 0, height: 12 },
            shadowOpacity: 0.8,
            shadowRadius: 48,
            elevation: 12,
        },
        glow: (color: string) => ({
            shadowColor: color,
            shadowOffset: { width: 0, height: 0 },
            shadowOpacity: 0.6,
            shadowRadius: 16,
            elevation: 6,
        })
    }
};
