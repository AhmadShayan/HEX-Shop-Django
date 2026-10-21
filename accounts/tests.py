
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.test import TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from carts.models import CartItem
from hexshop.test_utils import PASSWORD, make_product, make_user, make_variation
from orders.models import Order

Account = get_user_model()


def registration_data(email='newbie@example.com', password=PASSWORD, confirm=None):
    return {
        'first_name': 'New',
        'last_name': 'Buyer',
        'phone_number': '0300111222',
        'email': email,
        'password': password,
        'confirm_password': confirm or password,
    }


class RegistrationTests(TestCase):
    def test_registration_creates_an_inactive_account_and_sends_an_activation_link(self):
        response = self.client.post(reverse('register'), registration_data())
        self.assertEqual(response.status_code, 302)
        user = Account.objects.get(email='newbie@example.com')
        self.assertFalse(user.is_active)
        self.assertTrue(user.check_password(PASSWORD))
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['newbie@example.com'])
        self.assertRegex(mail.outbox[0].body, r'/accounts/activate/[^/]+/[^/]+/')

    def test_mismatched_passwords_create_nothing(self):
        self.client.post(reverse('register'), registration_data(confirm='Different9!'))
        self.assertFalse(Account.objects.filter(email='newbie@example.com').exists())
        self.assertEqual(len(mail.outbox), 0)

    def test_two_people_with_the_same_name_before_the_at_sign_can_both_register(self):
        self.client.post(reverse('register'), registration_data(email='sam@example.com'))
        response = self.client.post(reverse('register'), registration_data(email='sam@example.org'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Account.objects.filter(email__startswith='sam@').count(), 2)
        self.assertEqual(Account.objects.values('username').distinct().count(), 2)

    def test_registering_the_same_email_twice_is_refused_cleanly(self):
        self.client.post(reverse('register'), registration_data())
        response = self.client.post(reverse('register'), registration_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Account.objects.filter(email='newbie@example.com').count(), 1)


class ActivationTests(TestCase):
    def setUp(self):
        self.user = make_user(active=False)
        self.uid = urlsafe_base64_encode(force_bytes(self.user.pk))

    def test_a_valid_link_activates_the_account(self):
        token = default_token_generator.make_token(self.user)
        self.client.get(reverse('activate', args=[self.uid, token]))
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

    def test_a_tampered_token_does_not(self):
        self.client.get(reverse('activate', args=[self.uid, 'abc-123']))
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

    def test_an_unknown_user_does_not_crash(self):
        uid = urlsafe_base64_encode(force_bytes(99999))
        response = self.client.get(reverse('activate', args=[uid, 'abc-123']))
        self.assertEqual(response.status_code, 302)


class LoginTests(TestCase):
    def setUp(self):
        self.user = make_user(email='login@example.com')
        self.url = reverse('login')

    def test_wrong_password_is_refused(self):
        response = self.client.post(self.url, {'email': 'login@example.com', 'password': 'nope'})
        self.assertRedirects(response, reverse('login'), fetch_redirect_response=False)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_an_unactivated_account_cannot_log_in(self):
        make_user(email='sleeper@example.com', active=False)
        self.client.post(self.url, {'email': 'sleeper@example.com', 'password': PASSWORD})
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_login_goes_to_the_dashboard(self):
        response = self.client.post(self.url, {'email': 'login@example.com', 'password': PASSWORD})
        self.assertRedirects(response, reverse('dashboard'), fetch_redirect_response=False)

    def test_a_local_next_page_is_honoured(self):
        referer = 'http://testserver/accounts/login/?next=/carts/checkout/'
        response = self.client.post(
            self.url, {'email': 'login@example.com', 'password': PASSWORD}, HTTP_REFERER=referer)
        self.assertRedirects(response, '/carts/checkout/', fetch_redirect_response=False)

    def test_an_external_next_page_is_never_followed(self):
        referer = 'http://testserver/accounts/login/?next=https://evil.example/phish'
        response = self.client.post(
            self.url, {'email': 'login@example.com', 'password': PASSWORD}, HTTP_REFERER=referer)
        self.assertRedirects(response, reverse('dashboard'), fetch_redirect_response=False)

    def test_a_scheme_relative_next_page_is_never_followed(self):
        referer = 'http://testserver/accounts/login/?next=//evil.example/phish'
        response = self.client.post(
            self.url, {'email': 'login@example.com', 'password': PASSWORD}, HTTP_REFERER=referer)
        self.assertRedirects(response, reverse('dashboard'), fetch_redirect_response=False)


class CartMergeAtLoginTests(TestCase):
    """What a visitor put in the basket before signing in must end up in the account basket."""

    def setUp(self):
        self.user = make_user(email='merge@example.com')
        self.shirt = make_product(name='Shirt')
        self.red = make_variation(self.shirt, 'color', 'Red')
        self.blue = make_variation(self.shirt, 'color', 'Blue')
        self.mug = make_product(name='Mug')

    def sign_in(self):
        self.client.post(reverse('login'), {'email': 'merge@example.com', 'password': PASSWORD})

    def test_a_matching_line_adds_the_visitors_quantity_and_leaves_no_orphan(self):
        existing = CartItem.objects.create(product=self.shirt, user=self.user, quantity=1)
        existing.variations.add(self.red)
        add = reverse('add_cart', args=[self.shirt.id])
        self.client.post(add, {'color': 'Red'})
        self.client.post(add, {'color': 'Red'})
        self.sign_in()
        existing.refresh_from_db()
        self.assertEqual(existing.quantity, 3)
        self.assertEqual(CartItem.objects.filter(user=self.user).count(), 1)
        self.assertEqual(CartItem.objects.filter(user__isnull=True).count(), 0)

    def test_a_different_variation_and_a_different_product_both_come_across(self):
        existing = CartItem.objects.create(product=self.shirt, user=self.user, quantity=1)
        existing.variations.add(self.red)
        self.client.post(reverse('add_cart', args=[self.shirt.id]), {'color': 'Blue'})
        self.client.post(reverse('add_cart', args=[self.mug.id]), {})
        self.sign_in()
        lines = CartItem.objects.filter(user=self.user)
        self.assertEqual(lines.count(), 3)
        self.assertEqual(sum(line.quantity for line in lines), 3)

    def test_signing_in_with_an_empty_basket_is_fine(self):
        self.sign_in()
        self.assertEqual(CartItem.objects.count(), 0)


class PasswordResetTests(TestCase):
    def setUp(self):
        self.user = make_user(email='forgetful@example.com')

    def test_a_known_address_gets_a_reset_link(self):
        self.client.post(reverse('forgotPassword'), {'email': 'forgetful@example.com'})
        self.assertEqual(len(mail.outbox), 1)
        self.assertRegex(mail.outbox[0].body, r'/accounts/resetpassword_validate/[^/]+/[^/]+/')

    def test_an_unknown_address_looks_exactly_the_same_and_sends_nothing(self):
        known = self.client.post(reverse('forgotPassword'), {'email': 'forgetful@example.com'})
        mail.outbox.clear()
        unknown = self.client.post(reverse('forgotPassword'), {'email': 'nobody@example.com'})
        self.assertEqual(unknown.status_code, known.status_code)
        self.assertEqual(unknown['Location'], known['Location'])
        self.assertEqual(len(mail.outbox), 0)

    def test_the_whole_reset_flow_sets_the_new_password(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        self.client.get(reverse('resetpassword_validate', args=[uid, token]))
        self.client.post(reverse('resetPassword'), {'password': 'BrandNew77!', 'confirm_password': 'BrandNew77!'})
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('BrandNew77!'))

    def test_posting_a_new_password_without_a_valid_link_changes_nothing(self):
        response = self.client.post(
            reverse('resetPassword'), {'password': 'BrandNew77!', 'confirm_password': 'BrandNew77!'})
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(PASSWORD))

    def test_a_bad_token_is_refused(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.client.get(reverse('resetpassword_validate', args=[uid, 'bad-token']))
        self.assertNotIn('uid', self.client.session)


class DashboardTests(TestCase):
    def test_it_requires_a_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_it_lists_only_the_users_own_placed_orders(self):
        mine = make_user()
        other = make_user()
        common = dict(first_name='A', last_name='B', phone='1', email='a@example.com', address_line_1='x',
                      country='PK', state='P', city='L', order_total=10, tax=0)
        Order.objects.create(user=mine, order_number='1', is_ordered=True, **common)
        Order.objects.create(user=mine, order_number='2', is_ordered=False, **common)
        Order.objects.create(user=other, order_number='3', is_ordered=True, **common)
        self.client.force_login(mine)
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.context['order_count'], 1)
        self.assertEqual([o.order_number for o in response.context['orders']], ['1'])
