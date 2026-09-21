# Cafe 11:11

An offline cafe management system built with Django: menu management, a
point-of-sale/billing screen, inventory tracking, staff accounts, and a
sales dashboard. It runs entirely on your own computer with a local
SQLite database — no internet connection needed once installed.

## Features

- **Menu management** — categories, add/edit/delete items, price, availability, optional photo.
- **Point of Sale (billing)** — tap items to build an order, checkout with payment method, printable receipt.
- **Inventory** — stock items with units and reorder levels, low-stock alerts, restock/wastage log. Menu items can optionally be linked to a stock item so a sale auto-deducts stock.
- **Staff accounts** — Admin and Cashier roles. Admins manage menu/inventory/staff; cashiers use the POS and view reports.
- **Dashboard** — today's sales, this month's sales, a 7-day sales chart, top-selling items, low-stock alerts.
- **Order history** — every past order with status and payment method.

## 1. Requirements

- Python 3.10 or newer (check with `python --version` or `python3 --version`)

## Quick test drive (skip setup, try it now)

This copy already ships with a migrated database and sample menu/inventory
data so you can click around immediately:

```bash
python -m venv venv && source venv/bin/activate   # macOS/Linux
# or: py -m venv venv && venv\Scripts\activate     # Windows
pip install -r requirements.txt
python manage.py runserver
```

Then open **http://127.0.0.1:8000/** and log in with:

- Admin: `admin` / `admin1234`
- Cashier: `cashier1` / `cashier1234`

**Change these passwords (or delete `db.sqlite3` and start fresh — see
step 2) before using this for real business data.**

## 2. Full setup from scratch (optional — do this if you deleted db.sqlite3)

Open a terminal in this folder and run:

```bash
# Windows
py -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

Then install the dependencies:

```bash
pip install -r requirements.txt
```

Set up the database:

```bash
python manage.py migrate
```

Create your first admin account:

```bash
python manage.py createsuperuser
```

Follow the prompts (username, email is optional, password). This account
logs into both the app and Django's built-in admin panel. After creating
it, you can promote it to the "Admin" role from the app's Staff page, or
run this instead in `python manage.py shell`:

```python
from accounts.models import User
u = User.objects.get(username='your-username')
u.role = 'ADMIN'
u.save()
```

(A superuser created with `createsuperuser` already gets full admin
access regardless of this `role` field.)

## 3. Running it day-to-day

```bash
# activate the virtual environment first (see step 2), then:
python manage.py runserver
```

Open **http://127.0.0.1:8000/** in your browser. Log in with the account
you created. Press `Ctrl+C` in the terminal to stop the server.

Everything (menu, orders, inventory, users) is stored in the `db.sqlite3`
file in this folder — back that file up regularly (copy it somewhere
safe) since it's your entire cafe's data.

## 4. Day-to-day usage

- **Admin** logs in → *Menu* to add items/categories, *Inventory* to add
  stock items, *Staff* to create a Cashier account for counter staff.
- **Cashier** logs in → *POS* to ring up orders and print/checkout
  receipts. Use a browser's Print (Ctrl+P) on the receipt page — a
  regular printer or a receipt printer set as the default printer both
  work.
- The **Dashboard** (home page) shows today's and this month's sales,
  a 7-day chart, top sellers, and low-stock warnings at a glance.

## 5. Running on multiple counters (optional, same local network)

This is a single-computer setup by default. If you later want a second
till/counter to use the same database over your cafe's Wi-Fi:

1. Find the server computer's local IP address (e.g. `192.168.1.10`).
2. Add that IP to `ALLOWED_HOSTS` in `cafe_manager/settings.py`.
3. Run `python manage.py runserver 0.0.0.0:8000` on the server computer.
4. On the other device's browser, go to `http://192.168.1.10:8000/`.

## 6. Notes

- `DEBUG = True` is fine for local/offline use. If you ever deploy this
  on a shared network long-term, set `DEBUG = False` and give
  `SECRET_KEY` (in `settings.py`) a private value of your own.
- Product photos are stored in the `media/` folder.
- To reset everything, stop the server, delete `db.sqlite3`, and re-run
  `python manage.py migrate` and `python manage.py createsuperuser`.

## Project structure

```
cafe_manager/     Django project settings/urls
accounts/         custom user model, roles, staff CRUD
menu/             categories & menu items
inventory/        stock items, restock/wastage log
orders/           POS/cart, checkout, receipts, order history
dashboard/        sales analytics & charts
templates/        all HTML templates
static/           CSS + the dashboard's chart script (no external CDN)
```
# Cafe_manager
