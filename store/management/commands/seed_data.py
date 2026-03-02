"""
Management command to seed the database with sample categories, products, and variations.
Idempotent: safe to run multiple times.
"""
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from category.models import Category
from store.models import Product, Variation


CATEGORIES = [
    {
        'name': 'Men\'s Fashion',
        'slug': 'mens-fashion',
        'description': 'Trendy clothing and apparel for men.',
        'image': 'photos/categories/mens-fashion.jpg',
    },
    {
        'name': 'Women\'s Fashion',
        'slug': 'womens-fashion',
        'description': 'Latest fashion trends for women.',
        'image': 'photos/categories/womens-fashion.jpg',
    },
    {
        'name': 'Electronics',
        'slug': 'electronics',
        'description': 'Gadgets, accessories and electronic devices.',
        'image': 'photos/categories/electronics.jpg',
    },
    {
        'name': 'Footwear',
        'slug': 'footwear',
        'description': 'Shoes, sneakers and sandals for every occasion.',
        'image': 'photos/categories/footwear.jpg',
    },
    {
        'name': 'Accessories',
        'slug': 'accessories',
        'description': 'Bags, wallets, sunglasses and more.',
        'image': 'photos/categories/accessories.jpg',
    },
]

PRODUCTS = [
    {
        'name': 'Classic White T-Shirt',
        'slug': 'classic-white-tshirt',
        'description': 'A timeless everyday essential. Soft cotton fabric with a relaxed fit — perfect for any casual occasion.',
        'price': 1500,
        'stock': 50,
        'category': 'mens-fashion',
        'image': 'photos/products/white-tshirt.jpg',
        'colors': ['White', 'Black', 'Navy Blue'],
        'sizes': ['S', 'M', 'L', 'XL'],
    },
    {
        'name': 'Slim Fit Jeans',
        'slug': 'slim-fit-jeans',
        'description': 'Modern slim fit denim jeans with a comfortable stretch fabric. Versatile enough for work and weekend.',
        'price': 3500,
        'stock': 35,
        'category': 'mens-fashion',
        'image': 'photos/products/slim-jeans.jpg',
        'colors': ['Blue', 'Black', 'Grey'],
        'sizes': ['30', '32', '34', '36'],
    },
    {
        'name': 'Men\'s Polo Shirt',
        'slug': 'mens-polo-shirt',
        'description': 'Classic polo shirt crafted from premium pique cotton. Smart-casual style for any setting.',
        'price': 2200,
        'stock': 40,
        'category': 'mens-fashion',
        'image': 'photos/products/polo-shirt.jpg',
        'colors': ['White', 'Navy Blue', 'Forest Green'],
        'sizes': ['S', 'M', 'L', 'XL'],
    },
    {
        'name': 'Oversized Hoodie',
        'slug': 'oversized-hoodie',
        'description': 'Ultra-soft fleece hoodie with an oversized fit. Stay cozy without sacrificing style.',
        'price': 3800,
        'stock': 30,
        'category': 'mens-fashion',
        'image': 'photos/products/hoodie.jpg',
        'colors': ['Charcoal', 'Cream', 'Olive Green'],
        'sizes': ['S', 'M', 'L', 'XL', 'XXL'],
    },
    {
        'name': 'Floral Summer Dress',
        'slug': 'floral-summer-dress',
        'description': 'Light and breezy floral print dress, perfect for warm weather. Features a flattering A-line silhouette.',
        'price': 2800,
        'stock': 25,
        'category': 'womens-fashion',
        'image': 'photos/products/summer-dress.jpg',
        'colors': ['Pink Floral', 'Blue Floral', 'Yellow Floral'],
        'sizes': ['S', 'M', 'L'],
    },
    {
        'name': 'Women\'s Formal Blazer',
        'slug': 'womens-formal-blazer',
        'description': 'Structured blazer with a tailored cut — elevate your office look or dress it down on weekends.',
        'price': 5500,
        'stock': 20,
        'category': 'womens-fashion',
        'image': 'photos/products/womens-blazer.jpg',
        'colors': ['Black', 'Beige', 'Dusty Rose'],
        'sizes': ['S', 'M', 'L', 'XL'],
    },
    {
        'name': 'Wireless Earbuds Pro',
        'slug': 'wireless-earbuds-pro',
        'description': 'Premium true wireless earbuds with active noise cancellation, 30-hour battery life and crystal-clear sound.',
        'price': 7999,
        'stock': 45,
        'category': 'electronics',
        'image': 'photos/products/wireless-earbuds.jpg',
        'colors': ['Midnight Black', 'Pearl White', 'Rose Gold'],
        'sizes': [],
    },
    {
        'name': 'Adjustable Phone Stand',
        'slug': 'adjustable-phone-stand',
        'description': 'Foldable aluminum desktop phone stand with adjustable height. Compatible with all smartphones and tablets.',
        'price': 850,
        'stock': 80,
        'category': 'electronics',
        'image': 'photos/products/phone-stand.jpg',
        'colors': ['Space Grey', 'Silver', 'Black'],
        'sizes': [],
    },
    {
        'name': 'Men\'s Running Shoes',
        'slug': 'mens-running-shoes',
        'description': 'Lightweight performance running shoes with cushioned soles and breathable mesh upper. Built for speed and comfort.',
        'price': 5500,
        'stock': 30,
        'category': 'footwear',
        'image': 'photos/products/running-shoes.jpg',
        'colors': ['Black/White', 'All White', 'Navy/Orange'],
        'sizes': ['40', '41', '42', '43', '44'],
    },
    {
        'name': 'Women\'s Casual Sneakers',
        'slug': 'womens-casual-sneakers',
        'description': 'Versatile everyday sneakers with a minimalist design. Comfortable cushioning for all-day wear.',
        'price': 4200,
        'stock': 28,
        'category': 'footwear',
        'image': 'photos/products/casual-sneakers.jpg',
        'colors': ['White', 'Pastel Pink', 'Lavender'],
        'sizes': ['36', '37', '38', '39', '40'],
    },
    {
        'name': 'Premium Leather Wallet',
        'slug': 'premium-leather-wallet',
        'description': 'Handcrafted genuine leather wallet with RFID blocking. Slim design with multiple card slots.',
        'price': 2200,
        'stock': 60,
        'category': 'accessories',
        'image': 'photos/products/leather-wallet.jpg',
        'colors': ['Tan Brown', 'Jet Black', 'Cognac'],
        'sizes': [],
    },
    {
        'name': 'Classic Aviator Sunglasses',
        'slug': 'classic-aviator-sunglasses',
        'description': 'Iconic aviator sunglasses with UV400 protection lenses and a lightweight metal frame. A wardrobe staple.',
        'price': 2800,
        'stock': 50,
        'category': 'accessories',
        'image': 'photos/products/sunglasses.jpg',
        'colors': ['Gold/Brown', 'Silver/Grey', 'Black/Green'],
        'sizes': [],
    },
]


class Command(BaseCommand):
    help = 'Seed the database with sample categories, products and variations.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding categories...')
        category_map = {}
        for cat_data in CATEGORIES:
            cat, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={
                    'category_name': cat_data['name'],
                    'description': cat_data['description'],
                    'cat_image': cat_data['image'],
                }
            )
            category_map[cat_data['slug']] = cat
            status = 'Created' if created else 'Already exists'
            self.stdout.write(f'  {status}: {cat.category_name}')

        self.stdout.write('Seeding products...')
        for prod_data in PRODUCTS:
            category = category_map.get(prod_data['category'])
            if not category:
                self.stdout.write(self.style.WARNING(f"  Category not found for {prod_data['name']}"))
                continue

            product, created = Product.objects.get_or_create(
                slug=prod_data['slug'],
                defaults={
                    'product_name': prod_data['name'],
                    'description': prod_data['description'],
                    'price': prod_data['price'],
                    'stock': prod_data['stock'],
                    'category': category,
                    'image': prod_data['image'],
                    'is_available': True,
                }
            )

            if created:
                for color in prod_data.get('colors', []):
                    Variation.objects.get_or_create(
                        product=product,
                        variation_category='color',
                        variation_value=color,
                        defaults={'is_active': True}
                    )
                for size in prod_data.get('sizes', []):
                    Variation.objects.get_or_create(
                        product=product,
                        variation_category='size',
                        variation_value=size,
                        defaults={'is_active': True}
                    )
                status = 'Created'
            else:
                status = 'Already exists'

            self.stdout.write(f'  {status}: {product.product_name}')

        self.stdout.write(self.style.SUCCESS('Database seeding complete!'))
