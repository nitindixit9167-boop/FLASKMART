from flask import Blueprint, redirect, url_for, flash
from flask_login import login_required, current_user

from app.extensions import db
from app.models import Product, Review
from app.forms import ReviewForm

reviews_bp = Blueprint("reviews", __name__)


@reviews_bp.route("/product/<int:product_id>/add", methods=["POST"])
@login_required
def add_review(product_id):
    product = Product.query.get_or_404(product_id)
    form = ReviewForm()

    if form.validate_on_submit():
        existing = Review.query.filter_by(
            user_id=current_user.id, product_id=product.id
        ).first()

        if existing:
            existing.rating = int(form.rating.data)
            existing.comment = form.comment.data
            flash("Your review has been updated.", "success")
        else:
            review = Review(
                user_id=current_user.id,
                product_id=product.id,
                rating=int(form.rating.data),
                comment=form.comment.data,
            )
            db.session.add(review)
            flash("Thanks for leaving a review!", "success")

        db.session.commit()
    else:
        flash("Please choose a rating before submitting your review.", "danger")

    return redirect(url_for("products.detail", slug=product.slug) + "#reviews")


@reviews_bp.route("/<int:review_id>/delete", methods=["POST"])
@login_required
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)
    if review.user_id != current_user.id and not current_user.is_admin:
        flash("You can't delete that review.", "danger")
        return redirect(url_for("main.index"))

    slug = review.product.slug
    db.session.delete(review)
    db.session.commit()
    flash("Review deleted.", "info")
    return redirect(url_for("products.detail", slug=slug) + "#reviews")
