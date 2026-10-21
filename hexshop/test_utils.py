"""Small factories shared by the test suites of every app."""
from itertools import count

from django.contrib.auth import get_user_model

from category.models import Category
from store.models import Product, Variation

_numbers = count(1)

PASSWORD = 'CorrectHorse9!'


def make_user(email=None, active=True, password=PASSWORD):
    n = next(_numbers)
    email = email or f'buyer{n}@example.com'
    user = get_user_model().objects.create_user(
        first_name='Test',
        last_name='Buyer',
        username=f'buyer{n}',
        email=email,
        password=password,
    )
    user.is_active = active
    user.save()
    return user


def make_category(name='Clothing'):
    slug = name.lower().replace(' ', '-')
    category, _ = Category.objects.get_or_create(slug=slug, defaults={'category_name': name})
    return category


def make_product(name=None, price=1000, stock=10, category=None, available=True, description=''):
    n = next(_numbers)
    name = name or f'Product {n}'
    return Product.objects.create(
        product_name=name,
        slug=f'product-{n}',
        description=description,
        price=price,
        image='photos/products/test.jpg',
        stock=stock,
        is_available=available,
        category=category or make_category(),
    )


def make_variation(product, category, value):
    return Variation.objects.create(product=product, variation_category=category, variation_value=value)
