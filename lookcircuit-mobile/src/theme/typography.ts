// LookCircuit Design System - Typography
// Based on PRD v1.0
// Uses Outfit (Display) and Inter (Body)

export const typography = {
    fonts: {
        display: 'Outfit-Bold',
        h1: 'Outfit-SemiBold',
        h2: 'Outfit-SemiBold',
        h3: 'Inter-SemiBold',
        body: 'Inter-Regular',
        bodyMedium: 'Inter-Medium',
        caption: 'Inter-Regular',
        overline: 'Inter-SemiBold',
    },

    sizes: {
        display: 36,
        h1: 28,
        h2: 22,
        h3: 18,
        body: 16,
        caption: 14,
        overline: 12, // Also metadata
        small: 10,
    },

    lineHeights: {
        display: 40, // ~1.1
        h1: 34,      // ~1.2
        h2: 29,      // ~1.3
        h3: 25,      // ~1.4
        body: 24,    // 1.5
        caption: 20, // 1.4
        overline: 16, // 1.3
    },

    letterSpacing: {
        display: -0.02, // em roughly handled by pixels in RN, but usually just numbers
        h1: -0.28,      // -0.01em * 28
        caption: 0.14,  // 0.01em
        overline: 0.96, // 0.08em * 12
        metadata: 0.24, // 0.02em
    }
};
