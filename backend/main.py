from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)

db = SQLAlchemy(app)
jwt = JWTManager(app)

# Создаем движок и сессию
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Session = sessionmaker(bind=engine)

# Модели (таблицы в базе данных)
class Product(db.Model):
    __tablename__ = 'site_products'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    isact = db.Column(db.Boolean, nullable=False)
    about = db.Column(db.String)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    registrationdate = db.Column(db.String, nullable=False)

class CartItem(db.Model):
    __tablename__ = 'cart_items'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('site_products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

## Блок для каталога ##
@app.route('/api/all_products', methods=['GET'])
def get_all_products():
    products = Product.query.all()
    dict_db = [{"id": product.id, "name": product.title.rstrip(), "price": product.price, "status": product.isact,
                "about": product.about} for product in products]
    return jsonify({"results": dict_db})
####

## Блок для пользователей ##
@app.route('/api/users/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']

    if User.query.filter_by(username=username.lower()).first():
        return jsonify({"status": "not_success", "message": "Пользователь уже существует!"})

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    current_time = datetime.now().strftime("%d-%m-%Y")
    new_user = User(username=username.lower(), password=hashed_password, registrationdate=current_time)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"status": "success", "message": "Пользователь зарегистрирован!"}), 200

@app.route('/api/users/user/login', methods=['POST'])
def log_in():
    data = request.get_json()
    username = data['username']
    password = data['password']
    user = User.query.filter_by(username=username.lower()).first()
    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=str(user.id))
        return jsonify({"message": "Добро пожаловать!", "username": username.lower(), "access_token": access_token}), 200
    else:
        return jsonify({"status": "not_success", "message": "Неверное имя пользователя или пароль!"}), 401

@app.route('/api/users/user/profile', methods=['GET'])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    with Session() as session:
        user = session.get(User, user_id)
        if user:
            return jsonify({"username": user.username, "datareg": user.registrationdate})
        else: return jsonify({"status": "not_success", "message": "Пользователь не найден!"}), 404

@app.route('/api/users/user/profile/update', methods=['PUT'])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    with Session() as session:
        user = session.get(User, user_id)
        if not user:
            return jsonify({"message": "Пользователь не найден"}), 404

        data = request.get_json()
        new_username = data.get('username')

        if not new_username:
            return jsonify({"message": "Имя пользователя не может быть пустым"}), 400

        # Проверяем, существует ли новое имя пользователя в базе данных
        existing_user = session.query(User).filter(User.username == new_username).first()
        if existing_user and existing_user.id != user_id:
            return jsonify({"message": "Имя пользователя уже занято"}), 400

        user.username = new_username
        session.commit()
        return jsonify({"username": user.username}), 200

@app.route('/api/users/user/logout', methods=['POST'])
def logout():
    return jsonify({"message": "Вы вышли из аккаунта!"})

@app.route('/api/cart/add', methods=['POST'])
@jwt_required()
def add_to_cart():
    user_id = get_jwt_identity()
    with Session() as session:
        if 'product_id' not in request.json:
            return jsonify({"message": "Отсутствует product_id."}), 400

        product_id = request.json['product_id']
        product = session.get(Product, product_id)
        if not product:
            return jsonify({"message": "Продукт не найден."}), 404

        # Проверяем, есть ли уже этот товар в корзине
        cart_item = session.query(CartItem).filter_by(user_id=user_id, product_id=product_id).first()
        if cart_item: cart_item.quantity += 1  # Увеличиваем количество
        else:
            cart_item = CartItem(user_id=user_id, product_id=product_id, quantity=1)
            session.add(cart_item)

        try:
            session.commit()
        except Exception as e:
            session.rollback()  # Откат транзакции в случае ошибки
            return jsonify({"message": "Ошибка при добавлении товара в корзину."}), 500

        return jsonify({"message": "Товар добавлен в корзину!"}), 201

@app.route('/api/cart', methods=['GET'])
@jwt_required()
def get_cart():
    user_id = get_jwt_identity()
    with Session() as session:
        cart_items = session.query(CartItem).filter_by(user_id=user_id).all()
        items = []
        for item in cart_items:
            product = session.get(Product, item.product_id)
            if product is None:
                return jsonify({"msg": "Товар не найден"}), 404
            items.append({
                "product_id": product.id,
                "name": product.title,
                "price": product.price,
                "quantity": item.quantity
            })

        return jsonify({"cart": items})

@app.route('/api/cart/remove/<int:product_id>', methods=['DELETE'])
@jwt_required()
def remove_from_cart(product_id):
    user_id = get_jwt_identity()
    with Session() as session:
        cart_item = session.query(CartItem).filter_by(user_id=user_id, product_id=product_id).first()

        if cart_item:
            session.delete(cart_item)
            session.commit()
            return jsonify({"message": "Товар удален из корзины!"})
        else: return jsonify({"message": "Товар не найден в корзине!"})

####

# Запуск приложения
if __name__ == '__main__':
    app.run(debug=True)