# HEX Shop — Django E-Commerce Platform

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python)
![Django](https://img.shields.io/badge/Django-4.2-092E20?style=flat-square&logo=django)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=flat-square&logo=postgresql)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Render](https://img.shields.io/badge/Deployed-Render-46E3B7?style=flat-square)

HEX Shop is a full-featured e-commerce web application built with Django as a final year university project. It covers the complete online shopping experience — from product browsing and cart management to user authentication, order placement, and admin control.

---

## Features

### Storefront
- Product catalogue with category filtering
- Product search
- Product detail pages with image support
- Responsive front-end (HTML/CSS/JS)

### Shopping Cart
- Add / remove / update cart items
- Anonymous cart merged with user account on login
- Cart item count shown globally via context processor

### User Accounts
- Custom user model (`Account`) — email-based login (not username)
- Registration and profile management
- Secure password reset via email token
- User dashboard with order history

### Orders
- Full checkout flow with order form
- Cash on Delivery support
- Order confirmation page
- Order and payment records in database

### Admin Panel
- Full Django admin integration
- Manage products, categories, users, orders, payments
- Custom admin configuration per app

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | Django 4.2.1 |
| Language | Python 3.11 |
| Database | PostgreSQL (production) / SQLite (development) |
| ORM | Django ORM |
| Image Processing | Pillow 10.0 |
| Static Files | WhiteNoise 6.5 |
| WSGI Server | Gunicorn 21.2 |
| DB URL Parsing | dj-database-url 2.1 |
| Environment Config | python-decouple 3.8 |
| Deployment | Render |

---

## Local Development Setup

### Prerequisites
- Python 3.11+
- pip
- Git

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/AhmadShayan/HEX-Shop-Django.git
cd HEX-Shop-Django

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env with your values (see below)

# 5. Run database migrations
python manage.py migrate

# 6. (Optional) Seed sample data
python manage.py seed_data

# 7. Start the development server
python manage.py runserver
```

App runs at `http://127.0.0.1:8000` by default.

### Required `.env` Variables

```env
SECRET_KEY=your-very-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Email (Gmail SMTP — use an App Password, not your account password)
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password

# Database (leave empty to use SQLite for local dev)
DATABASE_URL=
```

---

## Project Structure

```
HEX-Shop-Django/
  hexshop/          # Django project config (settings, urls, wsgi)
  accounts/         # Custom user model, auth, password reset, dashboard
  store/            # Product and category models, product views
  category/         # Category model and context processor
  carts/            # Cart and CartItem models, cart views
  orders/           # Order and Payment models, checkout flow
  templates/        # HTML templates for all apps
  static/           # CSS, JavaScript, project-level assets
  media/            # User-uploaded product and category images
  requirements.txt  # Python dependencies
  render.yaml       # Render deployment configuration
  .env.example      # Environment variable template
```

---

## Deployment

This project is configured for deployment on **[Render](https://render.com)** using `render.yaml`.

The configuration:
- Installs dependencies and runs migrations at build time
- Serves with Gunicorn
- Uses a managed PostgreSQL database
- Auto-generates `SECRET_KEY` in production
- Sets `DEBUG=False` in production

To deploy your own instance, fork the repo and connect it to a new Render Web Service.

---

## License

MIT — Free to use, fork, and build on.

---

## Built by Ahmasoft

This project was built by **[Ahmasoft](https://ahmasoft.com)** — an AI automation agency based in Lahore, Pakistan.

HEX Shop is an open-source academic project. It demonstrates full-stack Django development with production-ready deployment practices.

---

### What We Do

We help businesses automate the repetitive so their teams can focus on what actually matters.

| Service | What We Build |
|---|---|
| AI Workflow Automation | Multi-step automations with n8n, Make.com, Zapier + AI decision logic |
| AI Agents & Assistants | Custom AI agents for support, lead qualification, and research |
| Business Process Automation | End-to-end automation for sales, finance, HR, and operations |
| Custom Python Automation | Scripts, scrapers, ETL pipelines, and AI-powered data processing |
| n8n Solutions | Expert n8n builds — self-hosted setup, complex workflows, AI integrations |
| Social Media Automation | LinkedIn and Instagram content pipelines using AI + official APIs |

**Starter from $500 · Growth from $1,500 · Enterprise custom**

---

### Work With Us

| | |
|---|---|
| Website | [ahmasoft.com](https://ahmasoft.com) |
| Email | info@ahmasoft.com |
| LinkedIn | [linkedin.com/company/ahmasoft](https://www.linkedin.com/company/ahmasoft) |
| Instagram | [instagram.com/ahmasoft](https://www.instagram.com/ahmasoft/) |
| Founder | [Ahmad Shayan](https://ahmadshayan.com) |

> Get a free AI audit of your business at **[ahmasoft.com/audit](https://ahmasoft.com/audit)** — we identify exactly where automation can save you time and money, with a personalized report in minutes.
