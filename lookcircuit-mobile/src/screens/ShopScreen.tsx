import React, { useState } from 'react';
import {
    View,
    Text,
    StyleSheet,
    ScrollView,
    SafeAreaView,
    TouchableOpacity,
    TextInput,
    Image,
    Dimensions,
    FlatList,
} from 'react-native';
import Animated, { FadeInDown } from 'react-native-reanimated';
import { Search, SlidersHorizontal, Heart, ShoppingBag } from 'lucide-react-native';
import { colors, typography, layout } from '../theme';

const { width } = Dimensions.get('window');
const CARD_WIDTH = (width - 48) / 2; // 2 columns with padding

interface Product {
    id: string;
    name: string;
    category: string;
    price: number;
    image: string;
    color: string;
    inStock: boolean;
}

const MOCK_PRODUCTS: Product[] = [
    { id: '1', name: 'Classic Linen Shirt', category: 'Shirts', price: 49.99, image: 'https://via.placeholder.com/200x280/6366F1/FFFFFF?text=Shirt', color: '#6366F1', inStock: true },
    { id: '2', name: 'Slim Fit Chinos', category: 'Pants', price: 59.99, image: 'https://via.placeholder.com/200x280/F43F5E/FFFFFF?text=Chinos', color: '#D4A574', inStock: true },
    { id: '3', name: 'Leather Oxford Shoes', category: 'Shoes', price: 129.99, image: 'https://via.placeholder.com/200x280/4A3728/FFFFFF?text=Shoes', color: '#4A3728', inStock: true },
    { id: '4', name: 'Wool Blazer', category: 'Jackets', price: 199.99, image: 'https://via.placeholder.com/200x280/27272A/FFFFFF?text=Blazer', color: '#27272A', inStock: true },
    { id: '5', name: 'Patterned Tie', category: 'Accessories', price: 29.99, image: 'https://via.placeholder.com/200x280/F59E0B/FFFFFF?text=Tie', color: '#F59E0B', inStock: false },
    { id: '6', name: 'Cotton Polo', category: 'Shirts', price: 39.99, image: 'https://via.placeholder.com/200x280/10B981/FFFFFF?text=Polo', color: '#10B981', inStock: true },
];

const CATEGORIES = ['All', 'Shirts', 'Pants', 'Jackets', 'Shoes', 'Accessories'];

const ShopScreen = () => {
    const [searchQuery, setSearchQuery] = useState('');
    const [selectedCategory, setSelectedCategory] = useState('All');
    const [favorites, setFavorites] = useState<Set<string>>(new Set());

    const filteredProducts = MOCK_PRODUCTS.filter(product => {
        const matchesSearch = product.name.toLowerCase().includes(searchQuery.toLowerCase());
        const matchesCategory = selectedCategory === 'All' || product.category === selectedCategory;
        return matchesSearch && matchesCategory;
    });

    const toggleFavorite = (id: string) => {
        const newFavorites = new Set(favorites);
        if (newFavorites.has(id)) {
            newFavorites.delete(id);
        } else {
            newFavorites.add(id);
        }
        setFavorites(newFavorites);
    };

    const renderProduct = ({ item, index }: { item: Product; index: number }) => (
        <Animated.View
            entering={FadeInDown.delay(index * 100).duration(600)}
            style={styles.productCard}
        >
            <View style={styles.imageContainer}>
                <Image source={{ uri: item.image }} style={styles.productImage} />
                <TouchableOpacity
                    style={styles.favoriteButton}
                    onPress={() => toggleFavorite(item.id)}
                >
                    <Heart
                        size={20}
                        color={favorites.has(item.id) ? colors.accent.secondary : colors.text.muted}
                        fill={favorites.has(item.id) ? colors.accent.secondary : 'transparent'}
                    />
                </TouchableOpacity>
                {!item.inStock && (
                    <View style={styles.outOfStockBadge}>
                        <Text style={styles.outOfStockText}>Out of Stock</Text>
                    </View>
                )}
            </View>
            <View style={styles.productInfo}>
                <Text style={styles.productCategory}>{item.category}</Text>
                <Text style={styles.productName} numberOfLines={2}>{item.name}</Text>
                <View style={styles.priceRow}>
                    <Text style={styles.productPrice}>${item.price}</Text>
                    <View style={[styles.colorDot, { backgroundColor: item.color }]} />
                </View>
            </View>
        </Animated.View>
    );

    return (
        <SafeAreaView style={styles.container}>
            <View style={styles.header}>
                <Text style={styles.title}>Discover</Text>
                <Text style={styles.subtitle}>AI-Curated for Your Style</Text>
            </View>

            {/* Search Bar */}
            <View style={styles.searchContainer}>
                <View style={styles.searchBar}>
                    <Search size={20} color={colors.text.muted} />
                    <TextInput
                        style={styles.searchInput}
                        placeholder="Search products..."
                        placeholderTextColor={colors.text.muted}
                        value={searchQuery}
                        onChangeText={setSearchQuery}
                    />
                </View>
                <TouchableOpacity style={styles.filterButton}>
                    <SlidersHorizontal size={20} color={colors.text.primary} />
                </TouchableOpacity>
            </View>

            {/* Category Filters */}
            <ScrollView
                horizontal
                showsHorizontalScrollIndicator={false}
                contentContainerStyle={styles.categoriesContainer}
            >
                {CATEGORIES.map((category) => (
                    <TouchableOpacity
                        key={category}
                        style={[
                            styles.categoryChip,
                            selectedCategory === category && styles.categoryChipActive
                        ]}
                        onPress={() => setSelectedCategory(category)}
                    >
                        <Text style={[
                            styles.categoryText,
                            selectedCategory === category && styles.categoryTextActive
                        ]}>
                            {category}
                        </Text>
                    </TouchableOpacity>
                ))}
            </ScrollView>

            {/* Products Grid */}
            <FlatList
                data={filteredProducts}
                renderItem={renderProduct}
                keyExtractor={item => item.id}
                numColumns={2}
                contentContainerStyle={styles.productsGrid}
                showsVerticalScrollIndicator={false}
                columnWrapperStyle={styles.productRow}
                ListEmptyComponent={
                    <View style={styles.emptyContainer}>
                        <ShoppingBag size={48} color={colors.text.muted} />
                        <Text style={styles.emptyText}>No products found</Text>
                        <Text style={styles.emptySubtext}>Try adjusting your search or filters</Text>
                    </View>
                }
            />
        </SafeAreaView>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: colors.background.primary,
    },
    header: {
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
    searchContainer: {
        flexDirection: 'row',
        paddingHorizontal: 24,
        gap: 12,
        marginBottom: 16,
    },
    searchBar: {
        flex: 1,
        flexDirection: 'row',
        alignItems: 'center',
        backgroundColor: colors.background.elevated,
        borderRadius: layout.borderRadius.medium,
        paddingHorizontal: 16,
        height: 48,
        gap: 12,
        borderWidth: 1,
        borderColor: 'rgba(255,255,255,0.05)',
    },
    searchInput: {
        flex: 1,
        fontFamily: typography.fonts.body,
        fontSize: 16,
        color: colors.text.primary,
    },
    filterButton: {
        width: 48,
        height: 48,
        backgroundColor: colors.background.elevated,
        borderRadius: layout.borderRadius.medium,
        justifyContent: 'center',
        alignItems: 'center',
        borderWidth: 1,
        borderColor: 'rgba(255,255,255,0.05)',
    },
    categoriesContainer: {
        paddingHorizontal: 24,
        gap: 8,
        marginBottom: 20,
    },
    categoryChip: {
        paddingHorizontal: 20,
        paddingVertical: 10,
        backgroundColor: colors.background.elevated,
        borderRadius: layout.borderRadius.round,
        borderWidth: 1,
        borderColor: 'rgba(255,255,255,0.05)',
    },
    categoryChipActive: {
        backgroundColor: colors.accent.primary,
        borderColor: colors.accent.primary,
    },
    categoryText: {
        fontFamily: typography.fonts.body,
        fontSize: 14,
        color: colors.text.secondary,
    },
    categoryTextActive: {
        color: colors.text.primary,
        fontFamily: typography.fonts.h3,
    },
    productsGrid: {
        paddingHorizontal: 24,
        paddingBottom: 100, // Space for tab bar
    },
    productRow: {
        justifyContent: 'space-between',
        marginBottom: 16,
    },
    productCard: {
        width: CARD_WIDTH,
        backgroundColor: colors.background.elevated,
        borderRadius: layout.borderRadius.large,
        overflow: 'hidden',
        borderWidth: 1,
        borderColor: 'rgba(255,255,255,0.05)',
    },
    imageContainer: {
        width: '100%',
        height: CARD_WIDTH * 1.4,
        position: 'relative',
    },
    productImage: {
        width: '100%',
        height: '100%',
        resizeMode: 'cover',
    },
    favoriteButton: {
        position: 'absolute',
        top: 12,
        right: 12,
        width: 36,
        height: 36,
        backgroundColor: 'rgba(0,0,0,0.6)',
        borderRadius: 18,
        justifyContent: 'center',
        alignItems: 'center',
    },
    outOfStockBadge: {
        position: 'absolute',
        bottom: 8,
        left: 8,
        backgroundColor: 'rgba(0,0,0,0.8)',
        paddingHorizontal: 8,
        paddingVertical: 4,
        borderRadius: 6,
    },
    outOfStockText: {
        fontFamily: typography.fonts.caption,
        fontSize: 10,
        color: colors.text.muted,
    },
    productInfo: {
        padding: 12,
    },
    productCategory: {
        fontFamily: typography.fonts.caption,
        fontSize: 10,
        color: colors.text.muted,
        textTransform: 'uppercase',
        letterSpacing: 1,
        marginBottom: 4,
    },
    productName: {
        fontFamily: typography.fonts.h3,
        fontSize: 14,
        color: colors.text.primary,
        marginBottom: 8,
        height: 36, // Fixed height for consistency
    },
    priceRow: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
    },
    productPrice: {
        fontFamily: typography.fonts.h3,
        fontSize: 16,
        color: colors.accent.primary,
    },
    colorDot: {
        width: 20,
        height: 20,
        borderRadius: 10,
        borderWidth: 2,
        borderColor: 'rgba(255,255,255,0.2)',
    },
    emptyContainer: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        paddingTop: 80,
    },
    emptyText: {
        fontFamily: typography.fonts.h3,
        fontSize: 18,
        color: colors.text.primary,
        marginTop: 16,
    },
    emptySubtext: {
        fontFamily: typography.fonts.body,
        fontSize: 14,
        color: colors.text.secondary,
        marginTop: 4,
    },
});

export default ShopScreen;
