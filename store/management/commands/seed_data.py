"""
Management command to seed the database with professional sample data.
Idempotent: safe to run multiple times on every deploy.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from category.models import Category
from store.models import Product, Variation

Account = get_user_model()

CATEGORIES = [
    {
        'name': "Men's Fashion",
        'slug': 'mens-fashion',
        'description': 'Premium clothing and apparel for the modern man.',
        'image': 'photos/categories/mens-fashion.jpg',
    },
    {
        'name': "Women's Fashion",
        'slug': 'womens-fashion',
        'description': 'Curated fashion for the contemporary woman.',
        'image': 'photos/categories/womens-fashion.jpg',
    },
    {
        'name': 'Electronics',
        'slug': 'electronics',
        'description': 'Latest gadgets, accessories and smart devices.',
        'image': 'photos/categories/electronics.jpg',
    },
    {
        'name': 'Footwear',
        'slug': 'footwear',
        'description': 'Step out in style — shoes for every occasion.',
        'image': 'photos/categories/footwear.jpg',
    },
    {
        'name': 'Accessories',
        'slug': 'accessories',
        'description': 'Watches, wallets, bags and finishing touches.',
        'image': 'photos/categories/accessories.jpg',
    },
    {
        'name': 'Sports & Fitness',
        'slug': 'sports-fitness',
        'description': 'Gear up for your best performance.',
        'image': 'photos/categories/sports-fitness.jpg',
    },
    {
        'name': 'Home & Living',
        'slug': 'home-living',
        'description': 'Elevate your living space with premium home essentials.',
        'image': 'photos/categories/home-living.jpg',
    },
    {
        'name': 'Beauty & Care',
        'slug': 'beauty-care',
        'description': 'Skincare, fragrances and self-care essentials.',
        'image': 'photos/categories/beauty-care.jpg',
    },
]

PRODUCTS = [
    # ── MEN'S FASHION ──────────────────────────────────────────────────────────
    {
        'name': 'Classic Cotton T-Shirt',
        'slug': 'classic-cotton-tshirt',
        'description': 'A wardrobe staple crafted from 100% combed cotton. Breathable, lightweight and perfectly fitted for everyday wear. Pre-shrunk fabric ensures it keeps its shape wash after wash.',
        'price': 1499,
        'stock': 120,
        'category': 'mens-fashion',
        'image': 'photos/products/white-tshirt.jpg',
        'colors': ['White', 'Black', 'Navy Blue', 'Olive Green'],
        'sizes': ['S', 'M', 'L', 'XL', 'XXL'],
    },
    {
        'name': 'Slim Fit Stretch Jeans',
        'slug': 'slim-fit-stretch-jeans',
        'description': 'Modern slim-fit denim with 2% elastane for all-day comfort and flexibility. Five-pocket styling with a mid-rise waist. Machine washable and built to last.',
        'price': 3799,
        'stock': 60,
        'category': 'mens-fashion',
        'image': 'photos/products/slim-jeans.jpg',
        'colors': ['Indigo Blue', 'Jet Black', 'Stone Grey'],
        'sizes': ['30', '32', '34', '36', '38'],
    },
    {
        'name': "Men's Pique Polo Shirt",
        'slug': 'mens-pique-polo-shirt',
        'description': 'Premium pique cotton polo with a classic three-button placket and ribbed collar. Smart-casual versatility — wear it to the office or on weekends.',
        'price': 2299,
        'stock': 75,
        'category': 'mens-fashion',
        'image': 'photos/products/polo-shirt.jpg',
        'colors': ['White', 'Navy Blue', 'Burgundy', 'Forest Green'],
        'sizes': ['S', 'M', 'L', 'XL'],
    },
    {
        'name': 'Premium Oxford Dress Shirt',
        'slug': 'premium-oxford-dress-shirt',
        'description': 'Crafted from fine Oxford cotton with a subtle texture. The perfect dress shirt for formal meetings, dinners and special occasions. Slim fit with single button cuffs.',
        'price': 3299,
        'stock': 45,
        'category': 'mens-fashion',
        'image': 'photos/products/formal-shirt.jpg',
        'colors': ['White', 'Light Blue', 'Pale Pink', 'Lavender'],
        'sizes': ['S', 'M', 'L', 'XL', 'XXL'],
    },
    {
        'name': 'Fleece Oversized Hoodie',
        'slug': 'fleece-oversized-hoodie',
        'description': 'Ultra-soft 320gsm fleece hoodie with a relaxed oversized silhouette. Features a kangaroo pocket, adjustable drawstring and ribbed cuffs. The ultimate cozy essential.',
        'price': 4299,
        'stock': 55,
        'category': 'mens-fashion',
        'image': 'photos/products/hoodie.jpg',
        'colors': ['Charcoal', 'Cream', 'Sage Green', 'Dusty Mauve'],
        'sizes': ['S', 'M', 'L', 'XL', 'XXL'],
    },
    # ── WOMEN'S FASHION ────────────────────────────────────────────────────────
    {
        'name': 'Floral Wrap Midi Dress',
        'slug': 'floral-wrap-midi-dress',
        'description': 'Effortlessly elegant wrap-style midi dress in a vibrant floral print. Made from lightweight chiffon with a flattering V-neckline and adjustable waist tie. Perfect for brunch, events and vacations.',
        'price': 3299,
        'stock': 40,
        'category': 'womens-fashion',
        'image': 'photos/products/summer-dress.jpg',
        'colors': ['Rose Floral', 'Teal Floral', 'Sunflower Floral'],
        'sizes': ['XS', 'S', 'M', 'L', 'XL'],
    },
    {
        'name': "Women's Structured Blazer",
        'slug': 'womens-structured-blazer',
        'description': 'A power blazer with sharp tailoring and a cinched waist for a polished silhouette. Single-button closure with flap pockets. Pair with trousers for the office or jeans for a chic casual look.',
        'price': 6499,
        'stock': 30,
        'category': 'womens-fashion',
        'image': 'photos/products/womens-blazer.jpg',
        'colors': ['Jet Black', 'Ivory', 'Camel', 'Deep Navy'],
        'sizes': ['XS', 'S', 'M', 'L', 'XL'],
    },
    {
        'name': 'High-Waist Wide-Leg Trousers',
        'slug': 'high-waist-wide-leg-trousers',
        'description': 'Sleek high-rise trousers in a fluid wide-leg cut that elongates the silhouette. Crafted from a wrinkle-resistant crepe fabric. A versatile piece that transitions seamlessly from desk to dinner.',
        'price': 3799,
        'stock': 35,
        'category': 'womens-fashion',
        'image': 'photos/products/high-waist-trousers.jpg',
        'colors': ['Black', 'Ecru', 'Chocolate Brown', 'Slate Blue'],
        'sizes': ['XS', 'S', 'M', 'L'],
    },
    {
        'name': 'Ribbed Knit Cardigan',
        'slug': 'ribbed-knit-cardigan',
        'description': 'Cozy ribbed-knit cardigan with a relaxed open-front silhouette and deep pockets. Crafted from a soft acrylic-wool blend. Layer it over anything for instant elevated style.',
        'price': 2999,
        'stock': 50,
        'category': 'womens-fashion',
        'image': 'photos/products/knit-cardigan.jpg',
        'colors': ['Oatmeal', 'Dusty Rose', 'Forest Green', 'Stone Grey'],
        'sizes': ['S', 'M', 'L', 'XL'],
    },
    {
        'name': 'Satin Midi Skirt',
        'slug': 'satin-midi-skirt',
        'description': 'Luxurious satin-finish midi skirt with a flowing A-line silhouette and elasticated waistband. Dresses up beautifully for evenings out or pairs with a tee for day-to-day elegance.',
        'price': 2799,
        'stock': 38,
        'category': 'womens-fashion',
        'image': 'photos/products/midi-skirt.jpg',
        'colors': ['Champagne', 'Cobalt Blue', 'Emerald', 'Blush Pink'],
        'sizes': ['XS', 'S', 'M', 'L'],
    },
    # ── ELECTRONICS ────────────────────────────────────────────────────────────
    {
        'name': 'ProSound Wireless Earbuds',
        'slug': 'prosound-wireless-earbuds',
        'description': 'True wireless earbuds with Hybrid Active Noise Cancellation, 10mm drivers for rich bass, and up to 32 hours of total battery life with the charging case. IPX5 water resistant. Touch controls and seamless pairing.',
        'price': 8999,
        'stock': 60,
        'category': 'electronics',
        'image': 'photos/products/wireless-earbuds.jpg',
        'colors': ['Midnight Black', 'Pearl White', 'Rose Gold'],
        'sizes': [],
    },
    {
        'name': 'UltraCharge 20000mAh Power Bank',
        'slug': 'ultracharge-20000mah-power-bank',
        'description': 'Slim high-capacity power bank with 22.5W fast charging, dual USB-A ports and USB-C input/output. Charges your smartphone up to 5 times. LED power indicator and travel-friendly design.',
        'price': 4499,
        'stock': 80,
        'category': 'electronics',
        'image': 'photos/products/power-bank.jpg',
        'colors': ['Matte Black', 'White'],
        'sizes': [],
    },
    {
        'name': '7-in-1 USB-C Hub',
        'slug': '7-in-1-usbc-hub',
        'description': 'Expand your laptop connectivity with this premium aluminum USB-C hub. Includes 4K HDMI, 2x USB-A 3.0, USB-C PD 100W, SD/microSD card readers and a 3.5mm audio jack. Plug-and-play, no drivers needed.',
        'price': 3299,
        'stock': 45,
        'category': 'electronics',
        'image': 'photos/products/usb-hub.jpg',
        'colors': ['Space Grey', 'Silver'],
        'sizes': [],
    },
    {
        'name': 'Mechanical Gaming Keyboard',
        'slug': 'mechanical-gaming-keyboard',
        'description': 'Compact TKL mechanical keyboard with tactile clicky switches, per-key RGB backlighting and a durable aluminum top plate. Anti-ghosting with full N-key rollover. Detachable USB-C cable.',
        'price': 9999,
        'stock': 25,
        'category': 'electronics',
        'image': 'photos/products/gaming-keyboard.jpg',
        'colors': ['Black', 'White'],
        'sizes': [],
    },
    {
        'name': 'Foldable Aluminum Phone Stand',
        'slug': 'foldable-aluminum-phone-stand',
        'description': 'Adjustable desktop phone and tablet stand machined from premium aluminum alloy. Folds flat to slip into any bag. Compatible with all devices from 4" to 13". Non-slip silicone pads protect your device.',
        'price': 999,
        'stock': 100,
        'category': 'electronics',
        'image': 'photos/products/phone-stand.jpg',
        'colors': ['Space Grey', 'Silver', 'Rose Gold'],
        'sizes': [],
    },
    # ── FOOTWEAR ───────────────────────────────────────────────────────────────
    {
        'name': "Men's Performance Running Shoes",
        'slug': 'mens-performance-running-shoes',
        'description': 'Engineered for runners who demand the best. Lightweight breathable mesh upper, responsive foam midsole and durable rubber outsole with multi-directional traction. Reflective details for low-light visibility.',
        'price': 6999,
        'stock': 40,
        'category': 'footwear',
        'image': 'photos/products/running-shoes.jpg',
        'colors': ['Black/White', 'All White', 'Navy/Orange', 'Grey/Lime'],
        'sizes': ['40', '41', '42', '43', '44', '45'],
    },
    {
        'name': "Women's Platform Sneakers",
        'slug': 'womens-platform-sneakers',
        'description': 'Chunky platform sneakers with a retro-inspired silhouette and a 4cm platform sole. Padded ankle collar, cushioned insole and a durable vulcanized rubber outsole. Equal parts comfort and style.',
        'price': 5299,
        'stock': 35,
        'category': 'footwear',
        'image': 'photos/products/casual-sneakers.jpg',
        'colors': ['Triple White', 'Black', 'Pastel Pink', 'Lavender'],
        'sizes': ['36', '37', '38', '39', '40', '41'],
    },
    {
        'name': "Men's Genuine Leather Loafers",
        'slug': 'mens-genuine-leather-loafers',
        'description': 'Handcrafted from full-grain leather with a penny keeper strap and leather-lined interior for breathability. A timeless silhouette that pairs beautifully with both suits and casual denim.',
        'price': 7999,
        'stock': 25,
        'category': 'footwear',
        'image': 'photos/products/leather-loafers.jpg',
        'colors': ['Tan', 'Dark Brown', 'Black'],
        'sizes': ['40', '41', '42', '43', '44'],
    },
    {
        'name': "Women's Block Heel Sandals",
        'slug': 'womens-block-heel-sandals',
        'description': 'Elegant strappy sandals with a stable 7cm block heel and cushioned footbed for all-day comfort. Adjustable ankle strap with a polished gold buckle. From workdays to evening events.',
        'price': 4599,
        'stock': 30,
        'category': 'footwear',
        'image': 'photos/products/block-heels.jpg',
        'colors': ['Nude', 'Black', 'Champagne Gold', 'Cobalt Blue'],
        'sizes': ['36', '37', '38', '39', '40'],
    },
    # ── ACCESSORIES ───────────────────────────────────────────────────────────
    {
        'name': 'RFID Slim Leather Wallet',
        'slug': 'rfid-slim-leather-wallet',
        'description': 'Handstitched from full-grain vegetable-tanned leather. RFID-blocking lining protects your cards from digital theft. Fits 8 cards plus cash with a minimalist profile that slips easily into any pocket.',
        'price': 2799,
        'stock': 90,
        'category': 'accessories',
        'image': 'photos/products/leather-wallet.jpg',
        'colors': ['Cognac', 'Jet Black', 'Dark Brown', 'Midnight Navy'],
        'sizes': [],
    },
    {
        'name': 'Polarized Aviator Sunglasses',
        'slug': 'polarized-aviator-sunglasses',
        'description': 'Iconic teardrop aviator frames with polarized UV400 lenses that eliminate glare. Lightweight stainless steel frame with adjustable nose pads. Includes a premium leather case and microfibre cloth.',
        'price': 3299,
        'stock': 65,
        'category': 'accessories',
        'image': 'photos/products/sunglasses.jpg',
        'colors': ['Gold/Brown', 'Silver/Grey', 'Black/Green', 'Rose Gold/Pink'],
        'sizes': [],
    },
    {
        'name': 'Heavy Canvas Tote Bag',
        'slug': 'heavy-canvas-tote-bag',
        'description': 'Spacious 15oz heavyweight canvas tote with reinforced double stitching, interior zip pocket and long shoulder straps. Ethically made and roomy enough for groceries, books or a gym kit.',
        'price': 1999,
        'stock': 70,
        'category': 'accessories',
        'image': 'photos/products/tote-bag.jpg',
        'colors': ['Natural', 'Black', 'Olive', 'Navy'],
        'sizes': [],
    },
    {
        'name': 'Minimalist Stainless Steel Watch',
        'slug': 'minimalist-stainless-steel-watch',
        'description': 'Swiss-inspired minimalist timepiece with a clean dial, sapphire-coated crystal glass and a brushed stainless steel case (40mm). Japanese quartz movement. Water resistant to 50m. Interchangeable strap.',
        'price': 12999,
        'stock': 20,
        'category': 'accessories',
        'image': 'photos/products/steel-watch.jpg',
        'colors': ['Silver/White', 'Gold/Black', 'Rose Gold/Cream'],
        'sizes': [],
    },
    # ── SPORTS & FITNESS ──────────────────────────────────────────────────────
    {
        'name': 'Premium Non-Slip Yoga Mat',
        'slug': 'premium-non-slip-yoga-mat',
        'description': '6mm thick TPE yoga mat with natural rubber grip surface and alignment guide lines. Lightweight, odour-resistant and sweat-proof. Includes a carry strap. Suitable for yoga, Pilates and home workouts.',
        'price': 2999,
        'stock': 55,
        'category': 'sports-fitness',
        'image': 'photos/products/yoga-mat.jpg',
        'colors': ['Purple', 'Teal', 'Black', 'Coral'],
        'sizes': [],
    },
    {
        'name': 'Resistance Bands Set (5 Levels)',
        'slug': 'resistance-bands-set-5-levels',
        'description': 'Set of 5 progressive resistance bands ranging from 5lbs to 50lbs. Made from natural latex with anti-snap protection. Includes a carrying bag and exercise guide. Perfect for strength, mobility and rehab.',
        'price': 1799,
        'stock': 80,
        'category': 'sports-fitness',
        'image': 'photos/products/resistance-bands.jpg',
        'colors': ['Multicolor Set'],
        'sizes': [],
    },
    {
        'name': 'Insulated Sports Water Bottle',
        'slug': 'insulated-sports-water-bottle',
        'description': 'Double-wall vacuum insulated stainless steel bottle that keeps drinks cold for 24 hours and hot for 12. BPA-free, leak-proof lid with a straw and spout option. Wide-mouth opening for easy cleaning.',
        'price': 1299,
        'stock': 100,
        'category': 'sports-fitness',
        'image': 'photos/products/water-bottle.jpg',
        'colors': ['Matte Black', 'White', 'Sky Blue', 'Coral Red'],
        'sizes': ['500ml', '750ml', '1L'],
    },
    # ── HOME & LIVING ─────────────────────────────────────────────────────────
    {
        'name': 'Artisan Ceramic Mug Set (4 Mugs)',
        'slug': 'artisan-ceramic-mug-set',
        'description': 'Set of four handcrafted stoneware mugs with a reactive glaze finish — each piece is uniquely different. 350ml capacity, microwave and dishwasher safe. Packaged in a premium gift box.',
        'price': 2499,
        'stock': 40,
        'category': 'home-living',
        'image': 'photos/products/mug-set.jpg',
        'colors': ['Ocean Blue', 'Forest Green', 'Terracotta', 'Slate Grey'],
        'sizes': [],
    },
    {
        'name': 'Luxury Scented Soy Candle',
        'slug': 'luxury-scented-soy-candle',
        'description': 'Hand-poured 100% natural soy wax candle with lead-free cotton wick. Up to 55 hours of clean, even burn. Presented in a reusable frosted glass jar with a minimalist label.',
        'price': 1699,
        'stock': 60,
        'category': 'home-living',
        'image': 'photos/products/soy-candle.jpg',
        'colors': ['Vanilla & Sandalwood', 'Jasmine & Rose', 'Cedarwood & Amber', 'Fresh Linen'],
        'sizes': [],
    },
    # ── BEAUTY & CARE ─────────────────────────────────────────────────────────
    {
        'name': 'Hyaluronic Acid Vitamin C Serum',
        'slug': 'hyaluronic-acid-vitamin-c-serum',
        'description': 'Clinical-strength brightening serum with 20% Vitamin C, 3.5% Niacinamide and Hyaluronic Acid. Visibly fades dark spots, firms skin and delivers all-day hydration. Fragrance-free, dermatologist tested. 30ml.',
        'price': 3499,
        'stock': 50,
        'category': 'beauty-care',
        'image': 'photos/products/face-serum.jpg',
        'colors': [],
        'sizes': ['30ml'],
    },
    {
        'name': 'Signature Eau de Parfum',
        'slug': 'signature-eau-de-parfum',
        'description': 'A captivating unisex fragrance with top notes of bergamot and black pepper, a heart of oud and rose, and a warm base of musk and amber. Long-lasting 8+ hour projection. Presented in a heavy crystal bottle.',
        'price': 7999,
        'stock': 30,
        'category': 'beauty-care',
        'image': 'photos/products/perfume.jpg',
        'colors': [],
        'sizes': ['50ml', '100ml'],
    },
]


class Command(BaseCommand):
    help = 'Seed database with professional sample data. Idempotent — safe to run on every deploy.'

    def handle(self, *args, **kwargs):
        self._seed_superuser()
        self._seed_categories()
        self._seed_products()
        self.stdout.write(self.style.SUCCESS('✓ Database seeding complete!'))

    def _seed_superuser(self):
        if not Account.objects.filter(is_superadmin=True).exists():
            Account.objects.create_superuser(
                first_name='Admin',
                last_name='HEX',
                username='hexadmin',
                email='admin@hexshop.com',
                password='HexShop@2024',
            )
            self.stdout.write('  Created superuser: admin@hexshop.com / HexShop@2024')
        else:
            self.stdout.write('  Superuser already exists.')

    def _seed_categories(self):
        self.stdout.write('Seeding categories...')
        self._category_map = {}
        for cat in CATEGORIES:
            obj, created = Category.objects.get_or_create(
                slug=cat['slug'],
                defaults={
                    'category_name': cat['name'],
                    'description': cat['description'],
                    'cat_image': cat['image'],
                }
            )
            self._category_map[cat['slug']] = obj
            self.stdout.write(f'  {"+" if created else "="} {obj.category_name}')

    def _seed_products(self):
        self.stdout.write('Seeding products...')
        for p in PRODUCTS:
            cat = self._category_map.get(p['category'])
            if not cat:
                continue

            product, created = Product.objects.get_or_create(
                slug=p['slug'],
                defaults={
                    'product_name': p['name'],
                    'description': p['description'],
                    'price': p['price'],
                    'stock': p['stock'],
                    'category': cat,
                    'image': p['image'],
                    'is_available': True,
                }
            )

            if created:
                for color in p.get('colors', []):
                    Variation.objects.create(
                        product=product,
                        variation_category='color',
                        variation_value=color,
                        is_active=True,
                    )
                for size in p.get('sizes', []):
                    Variation.objects.create(
                        product=product,
                        variation_category='size',
                        variation_value=size,
                        is_active=True,
                    )

            self.stdout.write(f'  {"+" if created else "="} {product.product_name}')
