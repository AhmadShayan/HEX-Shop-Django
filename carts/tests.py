from django.test import TestCase
from django.urls import reverse

from carts.models import Cart, CartItem
from hexshop.test_utils import make_product, make_user, make_variation


class AddToCartTests(TestCase):
    def setUp(self):
        self.product = make_product(price=1000)
        self.red = make_variation(self.product, 'color', 'Red')
        self.blue = make_variation(self.product, 'color', 'Blue')
        self.url = reverse('add_cart', args=[self.product.id])

    def test_anonymous_visitor_gets_a_cart_and_a_line(self):
        self.client.post(self.url, {'color': 'Red'})
        self.assertEqual(Cart.objects.count(), 1)
        item = CartItem.objects.get()
        self.assertEqual(item.quantity, 1)
        self.assertEqual(list(item.variations.all()), [self.red])
        self.assertIsNone(item.user)

    def test_same_variation_increases_quantity(self):
        self.client.post(self.url, {'color': 'Red'})
        self.client.post(self.url, {'color': 'Red'})
        item = CartItem.objects.get()
        self.assertEqual(item.quantity, 2)

    def test_different_variation_is_a_separate_line(self):
        self.client.post(self.url, {'color': 'Red'})
        self.client.post(self.url, {'color': 'Blue'})
        self.assertEqual(CartItem.objects.count(), 2)

    def test_unknown_form_fields_are_ignored(self):
        self.client.post(self.url, {'color': 'Purple', 'csrfmiddlewaretoken': 'x'})
        item = CartItem.objects.get()
        self.assertEqual(item.variations.count(), 0)

    def test_logged_in_user_gets_a_line_without_a_session_cart(self):
        user = make_user()
        self.client.force_login(user)
        self.client.post(self.url, {'color': 'Blue'})
        item = CartItem.objects.get()
        self.assertEqual(item.user, user)
        self.assertEqual(Cart.objects.count(), 0)


class RemoveFromCartTests(TestCase):
    def setUp(self):
        self.product = make_product()
        self.user = make_user()
        self.client.force_login(self.user)
        self.item = CartItem.objects.create(product=self.product, user=self.user, quantity=2)

    def test_remove_cart_decrements_then_deletes(self):
        url = reverse('remove_cart', args=[self.product.id, self.item.id])
        self.client.get(url)
        self.item.refresh_from_db()
        self.assertEqual(self.item.quantity, 1)
        self.client.get(url)
        self.assertFalse(CartItem.objects.filter(id=self.item.id).exists())

    def test_remove_cart_item_deletes_the_whole_line(self):
        self.client.get(reverse('remove_cart_item', args=[self.product.id, self.item.id]))
        self.assertFalse(CartItem.objects.filter(id=self.item.id).exists())

    def test_removing_from_a_visitor_basket_that_does_not_exist_is_harmless(self):
        self.client.logout()
        response = self.client.get(reverse('remove_cart', args=[self.product.id, self.item.id]))
        self.assertRedirects(response, reverse('cart'), fetch_redirect_response=False)

    def test_another_users_line_cannot_be_removed(self):
        stranger = make_user()
        theirs = CartItem.objects.create(product=self.product, user=stranger, quantity=1)
        response = self.client.get(reverse('remove_cart_item', args=[self.product.id, theirs.id]))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(CartItem.objects.filter(id=theirs.id).exists())


class CartPageTests(TestCase):
    def test_totals_use_a_two_percent_tax_and_skip_inactive_lines(self):
        user = make_user()
        self.client.force_login(user)
        a = make_product(price=1000)
        b = make_product(price=500)
        CartItem.objects.create(product=a, user=user, quantity=2)
        CartItem.objects.create(product=b, user=user, quantity=1)
        CartItem.objects.create(product=b, user=user, quantity=9, is_active=False)
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.context['total'], 2500)
        self.assertEqual(response.context['tax'], 50)
        self.assertEqual(response.context['grand_total'], 2550)
        self.assertEqual(response.context['quantity'], 3)

    def test_empty_cart_renders(self):
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)

    def test_cart_counter_counts_units_for_the_user(self):
        user = make_user()
        self.client.force_login(user)
        CartItem.objects.create(product=make_product(), user=user, quantity=3)
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.context['cart_count'], 3)

    def test_checkout_requires_login(self):
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response['Location'])
