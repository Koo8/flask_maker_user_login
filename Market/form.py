from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import Length, Email, EqualTo, InputRequired
from .models import User


class RegisterForm(FlaskForm):
    # add validate_username and validate_email def
    username = StringField(label="User Name", validators=[Length(min=3, max=20), InputRequired()])
    email = StringField(label='Email Address', validators=[Email(), InputRequired()])
    password1 = PasswordField(label="Password", validators=[Length(min=4), InputRequired()])
    password2 = PasswordField(label="Confirm Password", validators=[EqualTo('password1'), InputRequired()])
    submit = SubmitField(label="Create Account")

    def validate_username(self, user_name):
        user = User.query.filter_by(username=user_name.data).first()
        if user:
            raise ValidationError("This username has been taken, please choose another one.")

    def validate_email(self, theemail):
        user = User.query.filter_by(email=theemail.data).first()
        if user:
            raise ValidationError('This email address has been registered, please go to login page.')


class LoginForm(FlaskForm):
    username = StringField(label='User Name', validators=[InputRequired()])
    password = PasswordField(label='Password', validators=[InputRequired()])
    submit = SubmitField(label='Sign In')


class PurchaseForm(FlaskForm):
    submit = SubmitField(label='Purchase')


class SellForm(FlaskForm):
    submit = SubmitField(label='Sell')


# TODO: I need to add a 'create a new listing' modal page, that use the following form for register the new item to the db, also asign the id to the
#  current_user so that the newly created listing will appear in the right panel of owned items of the current_user

#
# class NewItemForm(FlaskForm):
#     item_name = StringField(label="Item Name", validators=[Length(min=3, max=20), InputRequired()])
#     item_price = StringField(label='Price', validators=[InputRequired()])
#     item_barcode = StringField(label="Barcode(12 Digits)", validators=[Length(min=12), InputRequired()])
#     item_description = StringField(label="Description", validators=[Length(min=20, max=2000),InputRequired()])
#     submit = SubmitField(label="Create New Listing")
