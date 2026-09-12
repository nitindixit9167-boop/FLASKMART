from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    TextAreaField,
    DecimalField,
    IntegerField,
    SelectField,
    SubmitField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    NumberRange,
    Optional,
)


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(3, 64)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(
        "Confirm password",
        validators=[DataRequired(), EqualTo("password", message="Passwords must match.")],
    )
    submit = SubmitField("Create account")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log in")


class ProductForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(1, 140)])
    product_type = SelectField(
        "Type", choices=[("general", "General item"), ("book", "Book")]
    )
    author = StringField("Author (books only)", validators=[Optional(), Length(0, 140)])
    category_id = SelectField("Category", coerce=int)
    price = DecimalField("Price", validators=[DataRequired(), NumberRange(min=0)])
    stock = IntegerField("Stock", validators=[DataRequired(), NumberRange(min=0)])
    image_url = StringField("Image URL", validators=[Optional(), Length(0, 300)])
    description = TextAreaField("Description", validators=[Optional()])
    submit = SubmitField("Save product")


class ReviewForm(FlaskForm):
    rating = SelectField(
        "Rating",
        choices=[(str(i), f"{i} star{'s' if i != 1 else ''}") for i in range(5, 0, -1)],
    )
    comment = TextAreaField("Your review", validators=[Optional(), Length(0, 1000)])
    submit = SubmitField("Submit review")


class CheckoutForm(FlaskForm):
    shipping_address = TextAreaField(
        "Shipping address", validators=[DataRequired(), Length(5, 300)]
    )
    submit = SubmitField("Place order")


class CategoryForm(FlaskForm):
    name = StringField("Category name", validators=[DataRequired(), Length(1, 80)])
    submit = SubmitField("Add category")
