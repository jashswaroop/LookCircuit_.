import React, { useState } from 'react';
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
import Animated, { FadeInDown } from 'react-native-reanimated';
import { Shirt, Heart, Trash2, Plus, Grid, List } from 'lucide-react-native';
import { colors, typography, layout } from '../theme';

const { width } = Dimensions.get('window');

interface WardrobeItem {
    id: string;
    name: string;
    category: string;
    image: string;
    color: string;
    dateAdded: string;
}

const MOCK_WARDROBE: WardrobeItem[] = [
    { id: '1', name: 'Navy Blazer', category: 'Jackets', image: 'https://via.placeholder.com/150/27272A/FFFFFF?text=Blazer', color: '#27272A', dateAdded: '2024-01-15' },
    { id: '2', name: 'White Oxford Shirt', category: 'Shirts', image: 'https://via.placeholder.com/150/FAFAFA/000000?text=Shirt', color: '#FAFAFA', dateAdded: '2024-01-10' },
    { id: '3', name: 'Dark Denim Jeans', category: 'Pants', image: 'https://via.placeholder.com/150/6366F1/FFFFFF?text=Jeans', color: '#6366F1', dateAdded: '2024-01-05' },
    { id: '4', name: 'Brown Leather Boots', category: 'Shoes', image: 'https://via.placeholder.com/150/8B5A3C/FFFFFF?text=Boots', color: '#8B5A3C', dateAdded: '2023-12-20' },
];

const WardrobeScreen = () => {
    const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
    const [selectedTab, setSelectedTab] = useState<'owned' | 'wishlist'>('owned');

    const renderGridItem = (item: WardrobeItem, index: number) => (
        <Animated.View
            key={item.id}
            entering={FadeInDown.delay(index * 100).duration(600)}
            style={styles.gridCard}
        >
            <Image source={{ uri: item.image }} style={styles.gridImage} />
            <TouchableOpacity style={styles.cardActionButton}>
                <Heart size={16} color={colors.text.muted} />
            </TouchableOpacity>
            <View style={styles.gridInfo}>
                <Text style={styles.itemName} numberOfLines={1}>{item.name}</Text>
                <Text style={styles.itemCategory}>{item.category}</Text>
            </View>
        </Animated.View>
    );

    const renderListItem = (item: WardrobeItem, index: number) => (
        <Animated.View
            key={item.id}
            entering={FadeInDown.delay(index * 100).duration(600)}
            style={styles.listCard}
        >
            <Image source={{ uri: item.image }} style={styles.listImage} />
            <View style={styles.listInfo}>
                <Text style={styles.itemName}>{item.name}</Text>
                <Text style={styles.itemCategory}>{item.category}</Text>
                <Text style={styles.itemDate}>Added {new Date(item.dateAdded).toLocaleDateString()}</Text>
            </View>
            <View style={styles.listActions}>
                <TouchableOpacity style={styles.listActionButton}>
                    <Heart size={20} color={colors.text.muted} />
                </TouchableOpacity>
                <TouchableOpacity style={styles.listActionButton}>
                    <Trash2 size={20} color={colors.accent.warning} />
                </TouchableOpacity>
            </View>
        </Animated.View>
    );

    return (
        <SafeAreaView style={styles.container}>
            {/* Header */}
            <View style={styles.header}>
                <View>
                    <Text style={styles.title}>Closet</Text>
                    <Text style={styles.subtitle}>{MOCK_WARDROBE.length} items in your wardrobe</Text>
                </View>
                <TouchableOpacity style={styles.addButton}>
                    <Plus size={24} color={colors.text.primary} />
                </TouchableOpacity>
            </View>

            {/* Tabs */}
            <View style={styles.tabContainer}>
                <TouchableOpacity
                    style={[styles.tab, selectedTab === 'owned' && styles.tabActive]}
                    onPress={() => setSelectedTab('owned')}
                >
                    <Shirt size={18} color={selectedTab === 'owned' ? colors.accent.primary : colors.text.muted} />
                    <Text style={[styles.tabText, selectedTab === 'owned' && styles.tabTextActive]}>
                        Owned
                    </Text>
                </TouchableOpacity>
                <TouchableOpacity
                    style={[styles.tab, selectedTab === 'wishlist' && styles.tabActive]}
                    onPress={() => setSelectedTab('wishlist')}
                >
                    <Heart size={18} color={selectedTab === 'wishlist' ? colors.accent.primary : colors.text.muted} />
                    <Text style={[styles.tabText, selectedTab === 'wishlist' && styles.tabTextActive]}>
                        Wishlist
                    </Text>
                </TouchableOpacity>
            </View>

            {/* View Toggle */}
            <View style={styles.controlsRow}>
                <Text style={styles.resultCount}>Showing all items</Text>
                <View style={styles.viewToggle}>
                    <TouchableOpacity
                        style={[styles.viewButton, viewMode === 'grid' && styles.viewButtonActive]}
                        onPress={() => setViewMode('grid')}
                    >
                        <Grid size={18} color={viewMode === 'grid' ? colors.accent.primary : colors.text.muted} />
                    </TouchableOpacity>
                    <TouchableOpacity
                        style={[styles.viewButton, viewMode === 'list' && styles.viewButtonActive]}
                        onPress={() => setViewMode('list')}
                    >
                        <List size={18} color={viewMode === 'list' ? colors.accent.primary : colors.text.muted} />
                    </TouchableOpacity>
                </View>
            </View>

            {/* Content */}
            <ScrollView
                contentContainerStyle={styles.scrollContent}
                showsVerticalScrollIndicator={false}
            >
                {selectedTab === 'owned' ? (
                    viewMode === 'grid' ? (
                        <View style={styles.gridContainer}>
                            {MOCK_WARDROBE.map((item, index) => renderGridItem(item, index))}
                        </View>
                    ) : (
                        <View style={styles.listContainer}>
                            {MOCK_WARDROBE.map((item, index) => renderListItem(item, index))}
                        </View>
                    )
                ) : (
                    <View style={styles.emptyState}>
                        <Heart size={48} color={colors.text.muted} />
                        <Text style={styles.emptyTitle}>No wishlist items yet</Text>
                        <Text style={styles.emptyText}>Items you favorite will appear here</Text>
                    </View>
                )}
            </ScrollView>
        </SafeAreaView>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: colors.background.primary,
    },
    header: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        paddingHorizontal: 24,
        paddingTop: 20,
        paddingBottom: 16,
    },
    title: {
        fontFamily: typography.fonts.h1,
        fontSize: 32,
        color: colors.text.primary,
        marginBottom: 4,
    },
    subtitle: {
        fontFamily: typography.fonts.body,
        fontSize: 14,
        color: colors.text.secondary,
    },
    addButton: {
        width: 48,
        height: 48,
        backgroundColor: colors.accent.primary,
        borderRadius: 24,
        justifyContent: 'center',
        alignItems: 'center',
    },
    tabContainer: {
        flexDirection: 'row',
        paddingHorizontal: 24,
        gap: 12,
        marginBottom: 16,
    },
    tab: {
        flex: 1,
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'center',
        gap: 8,
        paddingVertical: 12,
        backgroundColor: colors.background.elevated,
        borderRadius: layout.borderRadius.medium,
        borderWidth: 1,
        borderColor: 'rgba(255,255,255,0.05)',
    },
    tabActive: {
        backgroundColor: 'rgba(99, 102, 241, 0.1)',
        borderColor: colors.accent.primary,
    },
    tabText: {
        fontFamily: typography.fonts.body,
        fontSize: 14,
        color: colors.text.secondary,
    },
    tabTextActive: {
        fontFamily: typography.fonts.h3,
        color: colors.accent.primary,
    },
    controlsRow: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        paddingHorizontal: 24,
        marginBottom: 16,
    },
    resultCount: {
        fontFamily: typography.fonts.caption,
        fontSize: 12,
        color: colors.text.muted,
    },
    viewToggle: {
        flexDirection: 'row',
        backgroundColor: colors.background.elevated,
        borderRadius: layout.borderRadius.small,
        padding: 4,
        gap: 4,
    },
    viewButton: {
        width: 36,
        height: 36,
        justifyContent: 'center',
        alignItems: 'center',
        borderRadius: 6,
    },
    viewButtonActive: {
        backgroundColor: colors.background.surface,
    },
    scrollContent: {
        paddingHorizontal: 24,
        paddingBottom: 100,
    },

    // Grid View
    gridContainer: {
        flexDirection: 'row',
        flexWrap: 'wrap',
        gap: 16,
    },
    gridCard: {
        width: (width - 64) / 2,
        backgroundColor: colors.background.elevated,
        borderRadius: layout.borderRadius.large,
        overflow: 'hidden',
        borderWidth: 1,
        borderColor: 'rgba(255,255,255,0.05)',
    },
    gridImage: {
        width: '100%',
        height: (width - 64) / 2,
        resizeMode: 'cover',
    },
    cardActionButton: {
        position: 'absolute',
        top: 8,
        right: 8,
        width: 32,
        height: 32,
        backgroundColor: 'rgba(0,0,0,0.6)',
        borderRadius: 16,
        justifyContent: 'center',
        alignItems: 'center',
    },
    gridInfo: {
        padding: 12,
    },

    // List View
    listContainer: {
        gap: 12,
    },
    listCard: {
        flexDirection: 'row',
        backgroundColor: colors.background.elevated,
        borderRadius: layout.borderRadius.large,
        padding: 12,
        borderWidth: 1,
        borderColor: 'rgba(255,255,255,0.05)',
        gap: 12,
    },
    listImage: {
        width: 80,
        height: 80,
        borderRadius: layout.borderRadius.medium,
    },
    listInfo: {
        flex: 1,
        justifyContent: 'center',
    },
    itemName: {
        fontFamily: typography.fonts.h3,
        fontSize: 16,
        color: colors.text.primary,
        marginBottom: 4,
    },
    itemCategory: {
        fontFamily: typography.fonts.caption,
        fontSize: 12,
        color: colors.text.secondary,
        marginBottom: 4,
    },
    itemDate: {
        fontFamily: typography.fonts.caption,
        fontSize: 11,
        color: colors.text.muted,
    },
    listActions: {
        justifyContent: 'center',
        gap: 8,
    },
    listActionButton: {
        width: 36,
        height: 36,
        backgroundColor: colors.background.surface,
        borderRadius: 18,
        justifyContent: 'center',
        alignItems: 'center',
    },

    // Empty State
    emptyState: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        paddingTop: 80,
    },
    emptyTitle: {
        fontFamily: typography.fonts.h3,
        fontSize: 18,
        color: colors.text.primary,
        marginTop: 16,
    },
    emptyText: {
        fontFamily: typography.fonts.body,
        fontSize: 14,
        color: colors.text.secondary,
        marginTop: 4,
    },
});

export default WardrobeScreen;
