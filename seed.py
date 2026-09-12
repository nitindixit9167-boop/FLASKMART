"""
Run this once to set up the database with sample data:

    python seed.py

It creates all tables, an admin account, a demo customer account,
a few categories, and a handful of books/products to browse.
"""

from app import create_app
from app.extensions import db
from app.models import User, Category, Product
from app.utils import slugify

app = create_app()


def get_or_create_category(name):
    slug = slugify(name)
    category = Category.query.filter_by(slug=slug).first()
    if not category:
        category = Category(name=name, slug=slug)
        db.session.add(category)
        db.session.flush()
    return category


def get_or_create_product(name, **kwargs):
    slug = slugify(name)
    product = Product.query.filter_by(slug=slug).first()
    if not product:
        product = Product(name=name, slug=slug, **kwargs)
        db.session.add(product)
    return product


with app.app_context():
    db.create_all()

    # --- Users ---
    if not User.query.filter_by(email="admin@flaskmart.test").first():
        admin = User(username="admin", email="admin@flaskmart.test", is_admin=True)
        admin.set_password("admin123")
        db.session.add(admin)

    if not User.query.filter_by(email="demo@flaskmart.test").first():
        demo = User(username="demo", email="demo@flaskmart.test", is_admin=False)
        demo.set_password("demo1234")
        db.session.add(demo)

    db.session.commit()

    # --- Categories ---
    fiction = get_or_create_category("Fiction")
    nonfiction = get_or_create_category("Non-Fiction")
    stationery = get_or_create_category("Stationery")
    electronics = get_or_create_category("Electronics")
    home = get_or_create_category("Home & Kitchen")
    db.session.commit()

    # --- Products ---
    products = [
        dict(
            name="The Quiet Orchard",
            description="A gentle novel about three sisters rebuilding an old family orchard over one long summer.",
            price=349.00, stock=12, product_type="book", author="Meera Kulkarni",
            category_id=fiction.id, image_url="https://placehold.co/500x500?text=The+Quiet+Orchard",
        ),
        dict(
            name="Notes on Deep Work",
            description="A practical, no-nonsense guide to focused work in a distracted world.",
            price=499.00, stock=8, product_type="book", author="Arjun Rao",
            category_id=nonfiction.id, image_url="https://placehold.co/500x500?text=Notes+on+Deep+Work",
        ),
        dict(
            name="Salt and the Sea",
            description="A coastal mystery following a marine biologist investigating a string of odd tides.",
            price=399.00, stock=5, product_type="book", author="Fiona Alvares",
            category_id=fiction.id, image_url="https://placehold.co/500x500?text=Salt+and+the+Sea",
        ),
        dict(
            name="A Short History of Everyday Things",
            description="Where your fork, your zipper, and your umbrella actually came from.",
            price=549.00, stock=2, product_type="book", author="Devika Shah",
            category_id=nonfiction.id, image_url="https://placehold.co/500x500?text=Everyday+Things",
        ),
        dict(
            name="Dot-Grid Notebook (A5)",
            description="120gsm cream paper, 160 pages, lay-flat binding. Good for bullet journaling.",
            price=249.00, stock=30, product_type="general",
            category_id=stationery.id, image_url="https://placehold.co/500x500?text=Dot-Grid+Notebook",
        ),
        dict(
            name="Brass Desk Lamp",
            description="A warm-toned reading lamp with an adjustable arm and a soft-touch dimmer.",
            price=1899.00, stock=6, product_type="general",
            category_id=home.id, image_url="https://placehold.co/500x500?text=Brass+Desk+Lamp",
        ),
        dict(
            name="Wireless Earbuds Mini",
            description="Compact true-wireless earbuds with 24-hour case battery and quick charge.",
            price=2299.00, stock=0, product_type="general",
            category_id=electronics.id, image_url="https://placehold.co/500x500?text=Wireless+Earbuds",
        ),
        dict(
            name="Ceramic Pour-Over Set",
            description="A hand-glazed dripper and matching mug, made for slow mornings.",
            price=1199.00, stock=10, product_type="general",
            category_id=home.id, image_url="https://placehold.co/500x500?text=Pour-Over+Set",
        ),
    ]

    for p in products:
        get_or_create_product(p.pop("name"), **p)

    db.session.commit()
    print("Database seeded.")
    print("Admin login:  admin@flaskmart.test / admin123")
    print("Demo login:   demo@flaskmart.test  / demo1234")
