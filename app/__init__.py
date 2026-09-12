from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from app.extensions import db
from app.models import CartItem, Order, OrderItem
from app.forms import CheckoutForm

orders_bp = Blueprint("orders", __name__, template_folder="../templates/orders")


@orders_bp.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    items = CartItem.query.filter_by(user_id=current_user.id).all()
    if not items:
        flash("Your cart is empty.", "warning")
        return redirect(url_for("cart.view_cart"))

    form = CheckoutForm()
    total = sum(item.subtotal for item in items)

    if form.validate_on_submit():
        # Re-check stock before finalizing the order
        for item in items:
            if item.quantity > item.product.stock:
                flash(
                    f"Not enough stock for {item.product.name}. "
                    f"Only {item.product.stock} left.",
                    "danger",
                )
                return redirect(url_for("cart.view_cart"))

        order = Order(
            user_id=current_user.id,
            total_amount=total,
            shipping_address=form.shipping_address.data,
            status="pending",
        )
        db.session.add(order)
        db.session.flush()  # get order.id before commit

        for item in items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price_at_purchase=item.product.price,
            )
            item.product.stock -= item.quantity
            db.session.add(order_item)
            db.session.delete(item)

        db.session.commit()
        flash("Order placed successfully! Thank you for shopping with FlaskMart.", "success")
        return redirect(url_for("orders.detail", order_id=order.id))

    return render_template("orders/checkout.html", form=form, items=items, total=total)


@orders_bp.route("/")
@login_required
def list_orders():
    orders = (
        Order.query.filter_by(user_id=current_user.id)
        .order_by(Order.created_at.desc())
        .all()
    )
    return render_template("orders/list.html", orders=orders)


@orders_bp.route("/<int:order_id>")
@login_required
def detail(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id and not current_user.is_admin:
        flash("You don't have permission to view that order.", "danger")
        return redirect(url_for("orders.list_orders"))
    return render_template("orders/detail.html", order=order)
