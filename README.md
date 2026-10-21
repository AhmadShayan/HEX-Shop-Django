# HEX Shop

[![tests](https://github.com/AhmadShayan/HEX-Shop-Django/actions/workflows/tests.yml/badge.svg)](https://github.com/AhmadShayan/HEX-Shop-Django/actions/workflows/tests.yml)

A small online shop in Python and Django 4.2, written as the final year project of a BS in Computer Science (2023) and
brought up to date in 2026. Visitors browse products by category, pick colours and sizes, fill a basket and, once signed in,
check out and pay on delivery. Shop staff manage everything in the Django admin.

## Where the code comes from

The 2023 code follows the public GreatKart course project by Rathan Kumar
([dev-rathankumar/django-greatkart-2023](https://github.com/dev-rathankumar/django-greatkart-2023)): the same five apps, the
same structure and most of the same code. That history (14 to 30 May 2023) is kept as it was. What was added in 2026 is listed
below, so the two can be told apart in the commit log.

| | 2023 | 2026 |
|---|---|---|
| Work | the course project as built in May 2023 | environment-based settings, the Cash on Delivery order flow, dashboard order history, seed data, bug and security fixes, tests, CI |

## What it does

- **Storefront:** categories, search, pagination, product pages with colour and size variations.
- **Basket:** works without an account; what a visitor collected is merged into the account basket at login.
- **Accounts:** email login, email-verified registration, forgot-password links, a dashboard with order history.
- **Orders:** a checkout form, an order number, Cash on Delivery confirmation that reduces stock and empties the basket.
- **Admin:** products, categories, users, orders and payments in the Django admin.

## What changed in 2026

- Settings come from the environment. `DEBUG` is off by default, and a deployment without `SECRET_KEY` refuses to start.
- The seed command creates no admin account unless `ADMIN_EMAIL` and `ADMIN_PASSWORD` are both set.
- Order confirmation is one transaction: stock cannot go below zero, and an order with a line that cannot be supplied writes nothing.
- Fixed: an open redirect after login, a basket merge that added one unit instead of the visitor's quantity, a registration crash when
  two people share the text before the `@`, a password-reset crash, 500 errors on unknown products and baskets, an order total that
  counted only the last line, and a forgot-password form that revealed which addresses have an account.
- 63 automated tests, run on every push.

## Known limits

- No online payment: Cash on Delivery only, and the tax is a flat 2 percent.
- No product reviews, no stock alerts, one currency.
- Removing a basket line is a plain link, not a form, so it is not protected against forged requests.
- No rate limiting on login or password reset.
- The sample data is made up.

## Run it

```bash
git clone https://github.com/AhmadShayan/HEX-Shop-Django.git
cd HEX-Shop-Django
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # fill in the values, see below
python manage.py migrate
python manage.py seed_data      # optional: 8 categories, 30 products
python manage.py runserver
```

Run the tests with `python manage.py test`.

| Variable | Meaning |
|---|---|
| `SECRET_KEY` | Required unless `DEBUG=True` |
| `DEBUG` | `True` for local work, off by default |
| `ALLOWED_HOSTS` | Comma separated hosts |
| `DATABASE_URL` | PostgreSQL URL; empty means SQLite |
| `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` | Gmail SMTP with an app password, for activation and reset emails |
| `ADMIN_EMAIL`, `ADMIN_PASSWORD` | Optional, used by `seed_data` to create the first admin |

`render.yaml` and the `Procfile` hold deployment settings for Render and for Railway-style hosts. No public demo is running.

## Licence

MIT, for the changes made in this repository. Code that comes from the course project stays under its author's terms, which that
repository does not state.
