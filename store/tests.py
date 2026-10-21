import os
from io import StringIO
from unittest import mock

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from category.models import Category
from hexshop.test_utils import make_category, make_product
from store.models import Product, Variation


class StoreListingTests(TestCase):
    def test_only_available_products_are_listed(self):
        make_product(name='Visible')
        make_product(name='Hidden', available=False)
        response = self.client.get(reverse('store'))
        names = [p.product_name for p in response.context['products']]
        self.assertEqual(names, ['Visible'])
        self.assertEqual(response.context['product_count'], 1)

    def test_the_store_page_holds_six_products(self):
        for _ in range(8):
            make_product()
        response = self.client.get(reverse('store'))
        self.assertEqual(len(response.context['products']), 6)
        self.assertEqual(len(self.client.get(reverse('store') + '?page=2').context['products']), 2)

    def test_a_category_page_holds_three_and_only_its_own_products(self):
        shoes = make_category('Shoes')
        hats = make_category('Hats')
        for _ in range(4):
            make_product(category=shoes)
        make_product(category=hats)
        response = self.client.get(reverse('products_by_category', args=[shoes.slug]))
        self.assertEqual(len(response.context['products']), 3)
        self.assertEqual(response.context['product_count'], 4)

    def test_an_unknown_category_is_a_404(self):
        self.assertEqual(self.client.get(reverse('products_by_category', args=['nothing'])).status_code, 404)


class ProductDetailTests(TestCase):
    def test_a_product_page_renders(self):
        product = make_product()
        response = self.client.get(product.get_url())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['single_product'], product)

    def test_an_unknown_product_is_a_404_not_a_crash(self):
        category = make_category()
        response = self.client.get(reverse('product_detail', args=[category.slug, 'no-such-thing']))
        self.assertEqual(response.status_code, 404)


class SearchTests(TestCase):
    def setUp(self):
        make_product(name='Blue Hoodie', description='Warm and soft')
        make_product(name='Mug', description='Holds a hoodie-sized coffee')

    def test_it_matches_name_and_description(self):
        response = self.client.get(reverse('search'), {'keyword': 'hoodie'})
        self.assertEqual(response.context['product_count'], 2)

    def test_it_is_not_case_sensitive(self):
        response = self.client.get(reverse('search'), {'keyword': 'MUG'})
        self.assertEqual(response.context['product_count'], 1)

    def test_an_empty_or_missing_keyword_does_not_crash(self):
        self.assertEqual(self.client.get(reverse('search'), {'keyword': ''}).status_code, 200)
        self.assertEqual(self.client.get(reverse('search')).status_code, 200)


class SeedDataTests(TestCase):
    def run_seed(self, **env):
        with mock.patch.dict(os.environ, env):
            call_command('seed_data', stdout=StringIO())

    def test_it_is_safe_to_run_twice(self):
        self.run_seed()
        counts = (Category.objects.count(), Product.objects.count(), Variation.objects.count())
        self.run_seed()
        self.assertEqual(counts, (Category.objects.count(), Product.objects.count(), Variation.objects.count()))
        self.assertGreater(counts[1], 20)

    def test_it_creates_no_admin_account_by_default(self):
        with mock.patch.dict(os.environ, {}, clear=False):
            os.environ.pop('ADMIN_EMAIL', None)
            os.environ.pop('ADMIN_PASSWORD', None)
            call_command('seed_data', stdout=StringIO())
        self.assertEqual(get_user_model().objects.count(), 0)

    def test_it_needs_both_variables_for_an_admin(self):
        self.run_seed(ADMIN_EMAIL='boss@example.com')
        self.assertEqual(get_user_model().objects.filter(email='boss@example.com').count(), 0)

    def test_it_creates_the_admin_from_the_environment(self):
        self.run_seed(ADMIN_EMAIL='boss@example.com', ADMIN_PASSWORD='from-the-environment-1')
        admin = get_user_model().objects.get(email='boss@example.com')
        self.assertTrue(admin.is_superadmin)
        self.assertTrue(admin.check_password('from-the-environment-1'))
