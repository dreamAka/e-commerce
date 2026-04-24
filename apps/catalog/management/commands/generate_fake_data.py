"""
Generate fake data for NexGear — categories, brands, products, users, orders
Usage: python manage.py generate_fake_data
"""
import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from faker import Faker

from apps.accounts.models import CustomUser
from apps.catalog.models import Category, Brand, Product, ProductVariant, HeroSection
from apps.orders.models import Order, OrderItem
from apps.warehouse.models import Warehouse, Inventory


fake = Faker()


class Command(BaseCommand):
    help = "NexGear uchun test ma'lumotlar yaratadi"

    def handle(self, *args, **options):
        self.stdout.write("🚀 Fake data yaratish boshlandi...\n")

        # ── Categories ──
        categories_data = [
            ('Sichqonchalar', 'sichqonchalar', '🖱️ Gaming sichqonchalar'),
            ('Klaviaturalar', 'klaviaturalar', '⌨️ Mexanik gaming klaviaturalar'),
            ('Quloqchalar', 'quloqchalar', '🎧 Gaming quloqchalar'),
            ('Monitorlar', 'monitorlar', '🖥️ Gaming monitorlar'),
            ('Gamepadlar', 'gamepadlar', '🎮 Gamepad va kontrollerlar'),
            ('Stullar', 'stullar', '🪑 Gaming stullar'),
        ]
        cats = []
        for name, slug, desc in categories_data:
            cat, _ = Category.objects.get_or_create(
                slug=slug, defaults={'category_name': name, 'description': desc}
            )
            cats.append(cat)
        self.stdout.write(f"  ✅ {len(cats)} kategoriya")

        # ── Brands ──
        brands_data = ['Razer', 'Logitech', 'HyperX', 'SteelSeries', 'Corsair', 'ASUS ROG', 'MSI', 'BenQ']
        brands = []
        for name in brands_data:
            brand, _ = Brand.objects.get_or_create(
                brand_name=name, defaults={'country_of_origin': 'AQSH'}
            )
            brands.append(brand)
        self.stdout.write(f"  ✅ {len(brands)} brend")

        # ── Products ──
        products_data = [
            # Sichqonchalar
            ('Razer DeathAdder V3 Pro', cats[0], brands[0], 890000, 749000, 'Eng yengil gaming sichqoncha. 63g. 30K DPI sensor.'),
            ('Razer Viper V3 HyperSpeed', cats[0], brands[0], 1200000, None, 'Ultra-tez wireless. 34K sensor. 60 soat batareya.'),
            ('Logitech G Pro X Superlight 2', cats[0], brands[1], 1350000, 1199000, 'eSports uchun yaratilgan. HERO 2 sensor. 60g.'),
            ('Logitech G502 X Plus', cats[0], brands[1], 1500000, None, 'LIGHTFORCE switches. RGB. 13 tugma.'),
            ('HyperX Pulsefire Haste 2', cats[0], brands[2], 450000, 380000, 'Ultra-yengil. 53g. 26K DPI.'),
            ('SteelSeries Aerox 5 Wireless', cats[0], brands[3], 980000, None, 'AquaBarrier™ suv himoyasi. 74g.'),
            ('Corsair M75 Wireless', cats[0], brands[4], 850000, 720000, '26K DPI. CORSAIR MARKSMAN sensor.'),

            # Klaviaturalar
            ('Razer Huntsman V3 Pro', cats[1], brands[0], 2500000, 2100000, 'Analog optik switchlar. E-sport uchun.'),
            ('Razer BlackWidow V4 75%', cats[1], brands[0], 1800000, None, 'Hot-swappable. RGB. Tactile Green.'),
            ('Logitech G915 X TKL', cats[1], brands[1], 2200000, 1950000, 'Low-profile GL switches. LIGHTSPEED wireless.'),
            ('HyperX Alloy Origins 65', cats[1], brands[2], 750000, None, '65% compact. HyperX Red switches.'),
            ('Corsair K100 RGB', cats[1], brands[4], 2800000, 2450000, 'CORSAIR OPX switches. 4000Hz polling.'),
            ('SteelSeries Apex Pro TKL', cats[1], brands[3], 2100000, None, 'OmniPoint 2.0 adjustable switches.'),

            # Quloqchalar
            ('Razer BlackShark V2 Pro', cats[2], brands[0], 1600000, 1350000, 'THX Spatial Audio. 70 soat batareya.'),
            ('HyperX Cloud III Wireless', cats[2], brands[2], 1100000, None, 'DTS Headphone:X. 120 soat batareya.'),
            ('SteelSeries Arctis Nova Pro', cats[2], brands[3], 2900000, 2500000, 'Hi-Fi audio. ANC. Dual wireless.'),
            ('Logitech G Pro X 2', cats[2], brands[1], 1800000, None, 'PRO-G GRAPHENE drayverlari. DTS.'),
            ('Corsair HS80 Max Wireless', cats[2], brands[4], 1200000, 999000, 'Dolby Atmos. 65ft wireless.'),

            # Monitorlar
            ('ASUS ROG Swift PG27AQDM', cats[3], brands[5], 8500000, 7999000, '27" OLED. 1440p. 240Hz. 0.03ms.'),
            ('BenQ Zowie XL2546X', cats[3], brands[7], 5500000, None, '240Hz. DyAc⁺. 24.5" TN. eSports.'),
            ('MSI MEG 321URX', cats[3], brands[6], 12000000, 10500000, '32" 4K mini-LED. 240Hz. QD.'),
            ('ASUS ROG Swift PG34WCDM', cats[3], brands[5], 15000000, None, '34" QD-OLED. 3440x1440. 240Hz.'),
            ('Corsair XENEON 27QHD240', cats[3], brands[4], 6500000, 5800000, '27" QHD. 240Hz. IPS.'),

            # Gamepadlar
            ('Razer Wolverine V3 Pro', cats[4], brands[0], 1800000, None, 'Mecha-tactile. Hall Effect. RGB.'),
            ('HyperX Clutch Gladiate', cats[4], brands[2], 350000, 299000, 'Xbox uchun. Wired. Ergonomik.'),

            # Stullar
            ('Razer Iskur V2', cats[5], brands[0], 4500000, 3999000, 'Lumbar support. 4D armrest. EPU leather.'),
            ('Corsair TC200 Gaming Chair', cats[5], brands[4], 3200000, None, 'Premium fabric. 120kg. Ergonomik.'),
        ]

        created_products = []
        for name, cat, brand, base, sale, desc in products_data:
            slug = slugify(name)
            sku = f"NXG-{slug[:8].upper()}-{random.randint(100,999)}"
            product, created = Product.objects.get_or_create(
                slug=slug,
                defaults={
                    'product_name': name,
                    'category': cat,
                    'brand': brand,
                    'sku': sku,
                    'description': desc,
                    'base_price': Decimal(str(base)),
                    'sale_price': Decimal(str(sale)) if sale else None,
                    'product_status': 'active',
                    'is_featured': random.choice([True, False]),
                    'total_sales': random.randint(5, 200),
                    'average_rating': Decimal(str(round(random.uniform(3.5, 5.0), 1))),
                }
            )
            created_products.append(product)

        self.stdout.write(f"  ✅ {len(created_products)} mahsulot")

        # ── Variants ──
        color_variants = ['Qora', 'Oq', 'Qizil', 'Ko\'k']
        for p in created_products[:10]:
            for color in random.sample(color_variants, k=min(2, len(color_variants))):
                ProductVariant.objects.get_or_create(
                    product=p, variant_name=color,
                    defaults={
                        'sku': f"{p.sku}-{color[:3].upper()}",
                        'price_adjustment': Decimal(str(random.choice([0, 0, 50000, 100000]))),
                        'stock_quantity': random.randint(5, 50),
                    }
                )
        self.stdout.write("  ✅ Variantlar yaratildi")

        # ── Users ──
        users = []
        for i in range(15):
            username = fake.user_name() + str(random.randint(1, 99))
            user, created = CustomUser.objects.get_or_create(
                username=username,
                defaults={
                    'email': f"{username}@gmail.com",
                    'phone': f"+998 {random.randint(90,99)} {random.randint(100,999)} {random.randint(10,99)} {random.randint(10,99)}",
                    'first_name': fake.first_name(),
                    'last_name': fake.last_name(),
                    'loyalty_points': random.randint(0, 500),
                }
            )
            if created:
                user.set_password('test123')
                user.save()
            users.append(user)
        self.stdout.write(f"  ✅ {len(users)} foydalanuvchi (parol: test123)")

        # ── Orders ──
        statuses = ['pending', 'confirmed', 'processing', 'shipped', 'delivered', 'delivered', 'delivered']
        for user in users[:10]:
            num_orders = random.randint(1, 3)
            for _ in range(num_orders):
                items_count = random.randint(1, 3)
                order_products = random.sample(created_products, min(items_count, len(created_products)))
                total = Decimal('0')

                order = Order.objects.create(
                    user=user,
                    order_status=random.choice(statuses),
                    payment_status=random.choice(['paid', 'paid', 'pending']),
                    payment_method=random.choice(['naqd', 'karta', 'click']),
                )

                for prod in order_products:
                    qty = random.randint(1, 2)
                    price = prod.current_price
                    oi = OrderItem.objects.create(
                        order=order, product=prod, quantity=qty,
                        unit_price=price, subtotal=price * qty,
                    )
                    total += oi.subtotal

                order.subtotal = total
                order.total_amount = total
                order.save()

        order_count = Order.objects.count()
        self.stdout.write(f"  ✅ {order_count} buyurtma")

        # ── Warehouse ──
        wh, _ = Warehouse.objects.get_or_create(
            warehouse_name='Asosiy Ombor',
            defaults={'address': 'Toshkent, Yunusobod', 'city': 'Toshkent', 'region': 'Toshkent'}
        )
        for p in created_products:
            Inventory.objects.get_or_create(
                product=p, warehouse=wh,
                defaults={
                    'quantity_available': random.randint(0, 100),
                    'quantity_reserved': random.randint(0, 10),
                }
            )
        self.stdout.write("  ✅ Ombor zaxirasi yaratildi")

        # ── Hero Sections ──
        heroes_data = [
            ('Razer DeathAdder V3 Pro', 'Eng yengil professional gaming sichqoncha', '#44d62c', 1),
            ('Razer Huntsman V3 Pro', 'Eng tez analog optik klaviatura', '#00aaff', 2),
            ('Razer BlackShark V2 Pro', 'THX Spatial Audio quloqchalari', '#ff6600', 3),
            ('ASUS ROG OLED Monitor', '4K OLED 240Hz gaming monitor', '#ff0055', 4),
        ]
        for title, sub, color, order in heroes_data:
            HeroSection.objects.get_or_create(
                title=title,
                defaults={'subtitle': sub, 'accent_color': color, 'order': order, 'button_text': 'Batafsil'}
            )
        self.stdout.write("  ✅ Hero bannerlar yaratildi")

        self.stdout.write(self.style.SUCCESS("\n🎉 Fake data muvaffaqiyatli yaratildi!"))
        self.stdout.write(f"   Kategoriyalar: {len(cats)}")
        self.stdout.write(f"   Brendlar: {len(brands)}")
        self.stdout.write(f"   Mahsulotlar: {len(created_products)}")
        self.stdout.write(f"   Foydalanuvchilar: {len(users)}")
        self.stdout.write(f"   Buyurtmalar: {order_count}")
