from flask import Blueprint, render_template

from app.models import Product, Category

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    featured = Product.query.order_by(Product.created_at.desc()).limit(8).all()
    categories = Category.query.all()
    return render_template("index.html", featured=featured, categories=categories)


@main_bp.route("/about")
def about():
    return render_template("about.html")
