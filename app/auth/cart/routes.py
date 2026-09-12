from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from app.extensions import db
from app.models import CartItem, Product

cart_bp = Blueprint("cart", __name__, template_folder="../templates/cart")


@cart_bp.route("/")
@login_required
def view_cart():
    items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = sum(item.subtotal for item in items)
    return render_template("cart/view.html", items=items, total=total)


@cart_bp.route("/add/<int:product_id>", methods=["POST"])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    quantity = request.form.get("quantity", 1, type=int)
    quantity = max(1, quantity)

    if not product.in_stock:
        flash(f"Sorry, {product.name} is out of stock.", "warning")
        return redirect(request.referrer or url_for("products.list_products"))

    existing = CartItem.query.filter_by(
        user_id=current_user.id, product_id=product.id
    ).first()

    if existing:
        existing.quantity += quantity
    else:
        existing = CartItem(user_id=current_user.id, product_id=product.id, quantity=quantity)
        db.session.add(existing)

    # Don't let cart quantity exceed available stock
    if existing.quantity > product.stock:
        existing.quantity = product.stock

    db.session.commit()
    flash(f"Added {product.name} to your cart.", "success")
    return redirect(request.referrer or url_for("products.list_products"))


@cart_bp.route("/update/<int:item_id>", methods=["POST"])
@login_required
def update_item(item_id):
    item = CartItem.query.get_or_404(item_id)
    if item.user_id != current_user.id:
        flash("You can't modify that cart item.", "danger")
        return redirect(url_for("cart.view_cart"))

    quantity = request.form.get("quantity", 1, type=int)
    if quantity <= 0:
        db.session.delete(item)
    else:
        item.quantity = min(quantity, item.product.stock)
    db.session.commit()
    return redirect(url_for("cart.view_cart"))


@cart_bp.route("/remove/<int:item_id>", methods=["POST"])
@login_required
def remove_item(item_id):
    item = CartItem.query.get_or_404(item_id)
    if item.user_id != current_user.id:
        flash("You can't modify that cart item.", "danger")
        return redirect(url_for("cart.view_cart"))

    db.session.delete(item)
    db.session.commit()
    flash("Item removed from cart.", "info")
    return redirect(url_for("cart.view_cart"))
