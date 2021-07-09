from flask import Blueprint, render_template, redirect, url_for, flash, request
from . import db
from .models import Item, User
# from werkzeug.security import generate_password_hash
from .form import RegisterForm, LoginForm, PurchaseForm, SellForm  #, NewItemForm
from flask_login import login_user, logout_user, current_user, login_required

views = Blueprint('views', __name__)



@views.route('/')
@views.route('/home')
def home_page():
    return render_template('home.html')

@views.route('/market', methods=['POST', 'GET'])
@login_required
def market_page():
    # db.drop_all()
    # db.create_all()
    # new_user = User(username = 'nancy', email="nancy@yahoo.com", password = generate_password_hash('mypassword') )
    # db.session.add(new_user)
    # new_user = User(username='grail', email="grailG@mail.com", password=generate_password_hash('hispassword'))
    # db.session.add(new_user)
    # user_id = User.query.filter_by(username="nancy").first().id
    # new_item = Item(name = 'phone1', barcode = '893212299896', price=500, description='the another phone on sale')
    # db.session.add(new_item)
    # user_id = User.query.filter_by(username="grail").first().id
    # new_item = Item(name='television1', barcode='873948472047', price=1499, description='new smart tv'
    #                 )
    # db.session.add(new_item)
    # db.session.commit()

    # to help restore the budget
    # user = User.query.filter_by(username='cow').first()
    # if user:
    #     user.budget = 2000
    #     db.session.commit()

    global items, owned_items

    purchase_form = PurchaseForm()
    sell_form = SellForm()
    if request.method == 'POST':
        # To access the 'hidden' part of the form
        purchased_item= request.form.get('purchased_item')
        purchased_item_object = Item.query.filter_by(id = purchased_item).first()

        if purchased_item_object:
            if current_user.can_purchase(purchased_item_object):
                purchased_item_object.to_purchase_the_item()
                # purchased_item_object.owner_id = current_user.id
                # current_user.budget -= purchased_item_object.price
                # db.session.commit()
                flash(f'Congradulation! You have successfully purchased {purchased_item_object.name} for {purchased_item_object.price}', category='success')
            else:
                flash('Unfortunately, you don not have sufficient funds to do the purchase of this item', category='danger')
        # owned_items
        sell_item_id = request.form.get('sold_item')
        sold_item = Item.query.filter_by(id=sell_item_id).first()
        if sold_item:
            if current_user.can_sell(sold_item):
                sold_item.to_sell_the_item()
            # sold_item.owner_id =None
            # current_user.budget += sold_item.price
            # db.session.commit()
            flash(f'You have successfully sold {sold_item.name} for {sold_item.price} back to the market')
        else:
            flash('Something went wrong, this item can not be located within your owned items ')

        # creat a new listing
        # new_item_form = NewItemForm()
        # if new_item_form.validate_on_submit():
        #     new_item_created = Item(name = new_item_form.item_name.data,
        #                             price = new_item_form.item_price.data,
        #                             barcode = new_item_form.item_barcode.data,
        #                             description = new_item_form.item_description.data,
        #                             owner_id = new_item_form.id.data)
        #     db.session.add(new_item_created)
        #     db.session.commit()


        return redirect(url_for('views.market_page'))
    if request.method == "GET":
        items = Item.query.filter_by(owner_id = None)
        owned_items = Item.query.filter_by(owner_id=current_user.id)
        return render_template('market.html', items = items, purchase_form=purchase_form, sell_form = sell_form,owned_items = owned_items)

@views.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        new_User = User(username=form.username.data,
                        email= form.email.data,
                        password_hash = form.password1.data)
        db.session.add(new_User)
        db.session.commit()
        login_user(new_User)
        flash(f'You have successfully created an account, Now you are logged in as { new_User.username }', category='info')

        return redirect(url_for( 'views.market_page'))
    if form.errors != {}:
        for message in form.errors.values():
            flash(message,category='danger')
    return render_template('register.html', form = form)

@views.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user:
            if attempted_user.check_password_validation(input_password=form.password.data):
                login_user(attempted_user)
                flash(f'Success! You are now logged in as {attempted_user.username }', category='success')
                return redirect(url_for('views.market_page'))
            else:
                flash('Your login username and password don not match, please try again' )
        else:
            flash('This username is not existed')

    return render_template('login.html', form = form)

@views.route('/logout')
def logout_page():
    logout_user()
    return redirect(url_for('views.login_page'))

@views.route('/user')
def user_page():
    users = User.query.all()
    return render_template('user.html', users = users)