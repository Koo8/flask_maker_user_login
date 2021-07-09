from . import db, bcrypt, login_manager
from flask_login import UserMixin, current_user

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique =True)
    password = db.Column(db.String(60), nullable=False)
    budget = db.Column(db.Integer, default=1000)
    item = db.relationship('Item', backref ='owned_user', lazy = True)

    @property
    def password_hash(self):
        return self.password_hash

    @password_hash.setter
    def password_hash(self,passed_in_password):
        self.password = bcrypt.generate_password_hash(passed_in_password).decode('utf-8')

    @property
    def beautify_budget(self):
        if len(str(self.budget))>=4:
            return f'{str(self.budget)[:-3]},{str(self.budget)[-3:]}'
        else:
            return self.budget

    def check_password_validation(self,input_password):
        return bcrypt.check_password_hash(self.password, input_password)

    def can_purchase(self, item_to_purchase):
        return self.budget >= item_to_purchase.price

    def can_sell(self, item_to_sell):
        # return self.id == item_to_sell.owner_id
#  OR
        return item_to_sell in self.item





@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))

class Item(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30), nullable = False)
    barcode = db.Column(db.String(12), nullable = False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    description = db.Column(db.String(1024), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Item: {self.name}'

    def to_purchase_the_item(self):
        self.owner_id = current_user.id
        current_user.budget -= self.price
        db.session.commit()

    def to_sell_the_item(self):
        self.owner_id = None
        current_user.budget += self.price
        db.session.commit()

