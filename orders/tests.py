import datetime

from django.test import TestCase
from django.urls import reverse

from carts.models import CartItem
from hexshop.test_utils import make_product, make_user, make_variation
from orders.models import Order, OrderProduct, Payment

ORDER_FORM = {
    'first_name': 'Sara',
    'last_name': 'Khan',
    'email': 'sara@example.com',
    'phone': '0300123456',
    'address_line_1': '12 Mall Road',
    'address_line_2': '',
    'country': 'Pakistan',
    'state': 'Punjab',
    'city': 'Lahore',
    'order_note': '',
}


class PlaceOrderTests(TestCase):
    def setUp(self):
        self.user = make_user()
        self.client.force_login(self.user)
        self.cheap = make_product(price=500)
        self.dear = make_product(price=2000)

    def fill_cart(self):
        CartItem.objects.create(product=self.cheap, user=self.user, quantity=3)
        CartItem.objects.create(product=self.dear, user=self.user, quantity=1)

    def test_the_order_total_adds_up_every_line_and_a_two_percent_tax(self):
        self.fill_cart()
        self.client.post(reverse('place_order'), ORDER_FORM)
        order = Order.objects.get()
        self.assertEqual(order.tax, 70)
        self.assertEqual(order.order_total, 3570)

    def test_the_order_number_is_the_date_followed_by_the_id(self):
        self.fill_cart()
        self.client.post(reverse('place_order'), ORDER_FORM)
        order = Order.objects.get()
        self.assertEqual(order.order_number, datetime.date.today().strftime('%Y%m%d') + str(order.id))
        self.assertFalse(order.is_ordered)

    def test_an_empty_basket_goes_back_to_the_store(self):
        response = self.client.post(reverse('place_order'), ORDER_FORM)
        self.assertRedirects(response, reverse('store'), fetch_redirect_response=False)
        self.assertEqual(Order.objects.count(), 0)

    def test_an_invalid_form_creates_no_order(self):
        self.fill_cart()
        self.client.post(reverse('place_order'), {**ORDER_FORM, 'email': 'not-an-email'})
        self.assertEqual(Order.objects.count(), 0)

    def test_getting_the_page_sends_you_to_checkout(self):
        self.fill_cart()
        response = self.client.get(reverse('place_order'))
        self.assertRedirects(response, reverse('checkout'), fetch_redirect_response=False)

    def test_it_requires_a_login(self):
        self.client.logout()
        response = self.client.post(reverse('place_order'), ORDER_FORM)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response['Location'])


class ConfirmOrderTests(TestCase):
    """Cash on Delivery: confirming turns the pending order into a placed one."""

    def setUp(self):
        self.user = make_user()
        self.client.force_login(self.user)
        self.shirt = make_product(price=1000, stock=5)
        self.red = make_variation(self.shirt, 'color', 'Red')
        self.mug = make_product(price=300, stock=2)
        line = CartItem.objects.create(product=self.shirt, user=self.user, quantity=2)
        line.variations.add(self.red)
        CartItem.objects.create(product=self.mug, user=self.user, quantity=1)
        self.client.post(reverse('place_order'), ORDER_FORM)
        self.order = Order.objects.get()

    def confirm(self, order_number=None):
        return self.client.post(
            reverse('confirm_order'), {'order_number': order_number or self.order.order_number})

    def test_confirming_places_the_order_and_records_the_payment(self):
        response = self.confirm()
        self.assertEqual(response.status_code, 200)
        self.order.refresh_from_db()
        self.assertTrue(self.order.is_ordered)
        self.assertEqual(self.order.status, 'Accepted')
        payment = Payment.objects.get()
        self.assertEqual(payment.payment_method, 'Cash on Delivery')
        self.assertEqual(payment.status, 'Pending')
        self.assertEqual(self.order.payment, payment)

    def test_each_line_is_recorded_with_its_variation_and_price(self):
        self.confirm()
        lines = OrderProduct.objects.filter(order=self.order)
        self.assertEqual(lines.count(), 2)
        shirt_line = lines.get(product=self.shirt)
        self.assertEqual(shirt_line.quantity, 2)
        self.assertEqual(shirt_line.product_price, 1000)
        self.assertEqual(list(shirt_line.variation.all()), [self.red])

    def test_stock_goes_down_and_the_basket_is_emptied(self):
        self.confirm()
        self.shirt.refresh_from_db()
        self.mug.refresh_from_db()
        self.assertEqual((self.shirt.stock, self.mug.stock), (3, 1))
        self.assertEqual(CartItem.objects.filter(user=self.user).count(), 0)

    def test_confirming_twice_does_not_charge_stock_twice(self):
        self.confirm()
        self.confirm()
        self.shirt.refresh_from_db()
        self.assertEqual(self.shirt.stock, 3)
        self.assertEqual(Payment.objects.count(), 1)
        self.assertEqual(OrderProduct.objects.count(), 2)

    def test_not_enough_stock_refuses_the_order_and_writes_nothing(self):
        self.mug.stock = 0
        self.mug.save()
        self.confirm()
        self.order.refresh_from_db()
        self.shirt.refresh_from_db()
        self.assertFalse(self.order.is_ordered)
        self.assertEqual(self.shirt.stock, 5)
        self.assertEqual(Payment.objects.count(), 0)
        self.assertEqual(OrderProduct.objects.count(), 0)
        self.assertEqual(CartItem.objects.filter(user=self.user).count(), 2)

    def test_someone_elses_order_cannot_be_confirmed(self):
        self.client.logout()
        self.client.force_login(make_user())
        self.confirm()
        self.order.refresh_from_db()
        self.assertFalse(self.order.is_ordered)

    def test_an_unknown_order_number_is_handled(self):
        response = self.confirm('00000000')
        self.assertEqual(response.status_code, 302)

    def test_getting_the_page_does_nothing(self):
        response = self.client.get(reverse('confirm_order'))
        self.assertEqual(response.status_code, 302)
        self.order.refresh_from_db()
        self.assertFalse(self.order.is_ordered)
