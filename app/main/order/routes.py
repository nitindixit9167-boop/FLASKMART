from flask import Blueprint, render_template, request, current_app

from app.models import Product, Category
from app.forms import ReviewForm

products_bp = Blueprint("products", __name__, template_folder="../templates/products")


@products_bp.route("/")
def list_products():
    query = Product.query

    search = request.args.get("q", "").strip()
    category_id = request.args.get("category", type=int)
    product_type = request.args.get("type", "")
    sort = request.args.get("sort", "newest")
    page = request.args.get("page", 1, type=int)

    if search:
        like = f"%{search}%"
        query = query.filter(
            (Product.name.ilike(like)) | (Product.author.ilike(like))
        )
    if category_id:
        query = query.filter(Product.category_id == category_id)
    if product_type in ("book", "general"):
        query = query.filter(Product.product_type == product_type)

    if sort == "price_low":
        query = query.order_by(Product.price.asc())
    elif sort == "price_high":
        query = query.order_by(Product.price.desc())
    elif sort == "name":
        query = query.order_by(Product.name.asc())
    else:
        query = query.order_by(Product.created_at.desc())

    per_page = current_app.config.get("PRODUCTS_PER_PAGE", 8)
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    categories = Category.query.all()

    return render_template(
        "products/list.html",
        pagination=pagination,
        products=pagination.items,
        categories=categories,
        search=search,
        category_id=category_id,
        product_type=product_type,
        sort=sort,
    )


@products_bp.route("/<slug>")
def detail(slug):
    product = Product.query.filter_by(slug=slug).first_or_404()
    review_form = ReviewForm()
    reviews = sorted(product.reviews, key=lambda r: r.created_at, reverse=True)
    return render_template(
        "products/detail.html", product=product, review_form=review_form, reviews=reviews
    )
