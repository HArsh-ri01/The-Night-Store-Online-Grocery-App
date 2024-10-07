import csv
from operator import and_
from flask import Flask, request, jsonify, send_file, send_from_directory, render_template
from werkzeug.utils import secure_filename
from sqlalchemy import func
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import joinedload
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import timedelta, datetime
from celery_worker import make_celery
from sqlalchemy import func, or_
from flask_mail import Mail, Message
from flask_caching import Cache
from dateutil import parser
from celery.schedules import crontab
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import os
import random
import string
from functools import wraps
from flask_mail import Mail
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
)



SMTP_SERVER_HOST = "localhost"
SMTP_SERVER_PORT = 1025
SENDER_EMAIL = "HarshitGunjal22@gmail.com"
SENDER_PASSWORD = ""

def send_mail (to, subject, message_body):
    msg = MIMEMultipart()
    msg["To"] = to
    msg ["From"]= SENDER_EMAIL
    msg["Subject"] = subject
    msg.attach (MIMEText (message_body, "html"))
    server = smtplib.SMTP(host = SMTP_SERVER_HOST, port = SMTP_SERVER_PORT)
    server.login(user = SENDER_EMAIL, password=SENDER_PASSWORD)
    server.send_message(msg)
    server.quit()


app = Flask(__name__)
CORS(
    app,
    resources={
        r"/*": {
            "origins": "*",
            "supports_credentials": True,
            "headers": "Authorization",
        }
    },
)


app.config["UPLOAD_FOLDER"] = "Uploads"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "your_jwt_secret_key_here"

app.config.update(
    broker_url='redis://localhost:6379',
    result_backend='redis://localhost:6379',
    CACHE_TYPE='redis',
    CACHE_REDIS_URL='redis://localhost:6379/0'
)

celery = make_celery(app)
cache = Cache(app)

db = SQLAlchemy(app)
jwt = JWTManager(app)


@app.route("/Uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def random_string(length):
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for x in range(length))

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Runs every 30 days 
    # timedelta(days=30).total_seconds(),
    sender.add_periodic_task(10, send_monthly_report.s(), name='send_monthly_report')

@celery.on_after_configure.connect
def setup_daily_reminder(sender, **kwargs):
    # Runs every day
    # timedelta(days=1).total_seconds(),
    sender.add_periodic_task(10, send_daily_reminder.s(), name='send_daily_reminder')

"""-----------------------Database Models--------------------------"""


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)


roles_users = db.Table(
    "roles_users",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("role_id", db.Integer, db.ForeignKey("role.id"), primary_key=True),
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    last_login = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(), nullable=False, default="Not Active")
    roles = db.relationship(
        "Role", secondary=roles_users, backref=db.backref("users", lazy="dynamic")
    )

    def has_role(self, role_name):
        return any(role.name == role_name for role in self.roles)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    image_path = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(), nullable=False, default="Active")
    products = db.relationship("Product", backref="category", lazy=True)


class CategoryChange(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=True)
    name = db.Column(db.String(50), nullable=False)
    image_name = db.Column(db.String(100), nullable=False)
    action = db.Column(db.String(10), nullable=False)  # 'add', 'update', 'delete'
    category_status = db.Column(db.String(), nullable=False)
    status_change = db.Column(db.String(), nullable=False, default="Pending")
    category = db.relationship("Category", backref="changes", lazy=True)


class Product(db.Model):
    id = db.Column(db.Integer(), nullable=False, primary_key=True, unique=True)
    name = db.Column(db.String(50), nullable=False)
    stock = db.Column(db.Integer())
    sold = db.Column(db.Integer(), nullable=False, default=0)
    price_per_unit = db.Column(db.Integer(), nullable=False)
    exp = db.Column(db.Date(), nullable=False)
    mfg = db.Column(db.Date(), nullable=False)
    # favorite = db.Column(db.Boolean(), nullable=False, default="default")
    image_path = db.Column(db.String(50), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    status = db.Column(db.String(), nullable=False, default="Active")


class OrderProductAssociation(db.Model):
    __tablename__ = "order_product_association"
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), primary_key=True)
    quantity = db.Column(db.Integer(), nullable=False)
    product = db.relationship("Product", backref="OrderProductAssociation", lazy=True)
    price = db.Column(db.Integer(), nullable=False)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", backref=db.backref("orders", lazy=True))
    total_price = db.Column(db.Float, nullable=False)
    order_date = db.Column(db.Date(), nullable=False)
    order_items = db.relationship("OrderProductAssociation", backref="order", lazy=True)


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", backref=db.backref("cart", lazy=True))
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    product = db.relationship("Product", backref=db.backref("carts", lazy=True))
    quantity = db.Column(db.Integer(), nullable=False)
    price = db.Column(db.Integer(), nullable=False)


with app.app_context():
    db.create_all()


def add_sample_data():
    with app.app_context():
        admin_role = Role.query.filter_by(name="admin").first()

        if not admin_role:
            admin_role = Role(name="admin")
            db.session.add(admin_role)

        manager_role = Role.query.filter_by(name="manager").first()
        if not manager_role:
            manager_role = Role(name="manager")
            db.session.add(manager_role)

        user_role = Role.query.filter_by(name="user").first()
        if not user_role:
            user_role = Role(name="user")
            db.session.add(user_role)

        admin_user = User.query.filter_by(username="admin").first()
        if not admin_user:
            admin_user = User(
                username="admin",
                email="admin@example.com",
                password="admin_password",
                status="Active",
            )
            admin_user.roles.append(admin_role)
            db.session.add(admin_user)

        db.session.commit()


def manager_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        user = User.query.filter_by(username=current_user).first()

        if "manager" not in [role.name for role in user.roles]:
            return jsonify({"message": "Access denied. Manager role required."}), 403
        # g.user_id=user.id
        return fn(*args, **kwargs)

    return wrapper


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        user = User.query.filter_by(username=current_user).first()

        if "admin" not in [role.name for role in user.roles]:
            return jsonify({"message": "Access denied. Admin role required."}), 403
        # g.user_id=user.id
        return fn(*args, **kwargs)

    return wrapper


def admin_or_manager_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        user = User.query.filter_by(username=current_user).first()

        if "admin" in [role.name for role in user.roles] or "manager" in [
            role.name for role in user.roles
        ]:
            return fn(*args, **kwargs)
        else:
            return (
                jsonify({"message": "Access denied. Admin or manager role required."}),
                403,
            )

    return wrapper


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    role_name = data.get("role")

    existing_user = User.query.filter_by(username=username).first()
    existing_email = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({"message": "Username already exists"}), 409
    if existing_email:
        return jsonify({"message": "Email already exists"}), 409

    role = Role.query.filter_by(name=role_name).first()

    if not role:
        role = Role(name=role_name)
        db.session.add(role)

    new_user = User(username=username, email=email, password=password)
    if role_name == "manager":
        new_user.status = "Not Active"
    else:
        new_user.status = "Active"

    new_user.roles.append(role)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(
        username=username, password=password, status="Active"
    ).first()

    if user:
        expires_delta = timedelta(hours=1)

        access_token = create_access_token(
            identity=username, expires_delta=expires_delta
        )
        user_roles = [role.name for role in user.roles] if user.roles else []
        print("User Roles:", user_roles)
        user.last_login = datetime.utcnow()
        db.session.commit()
        return (
            jsonify(
                {
                    "username": user.username,
                    "roles": user_roles,  # Correct the key to be 'roles' instead of 'role'
                    "access_token": access_token,
                }
            ),
            200,
        )
    else:
        return jsonify({"message": "Invalid credentials or user is not active"}), 401


@app.route("/adminpage")
@jwt_required()
@admin_required
def admin_page():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    if user and user.has_role("admin"):
        return jsonify({"message": "Welcome to the Admin Page!"}), 200
    else:
        return jsonify({"error": "Unauthorized"}), 401


@app.route("/users/manager", methods=["GET"])
@jwt_required()
@admin_required
def get_manager_users():
    manager_users = User.query.filter(User.roles.any(name="manager")).all()
    serialized_users = [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "status": user.status,
        }
        for user in manager_users
    ]
    return jsonify({"users": serialized_users}), 200


@app.route("/activate-user/<int:user_id>", methods=["PUT"])
@jwt_required()
def activate_user(user_id):
    current_user = get_jwt_identity()
    admin_user = User.query.filter_by(username=current_user).first()

    if admin_user and admin_user.has_role("admin"):
        user_to_activate = User.query.get(user_id)

        if user_to_activate:
            user_to_activate.status = "Active"
            db.session.commit()
            return (
                jsonify(
                    {
                        "message": f"User '{user_to_activate.username}' activated successfully"
                    }
                ),
                200,
            )
        else:
            return jsonify({"message": "User not found"}), 404
    else:
        return jsonify({"error": "Unauthorized"}), 401


@app.route("/deactivate-user/<int:user_id>", methods=["PUT"])
@jwt_required()
def Deactivate_user(user_id):
    current_user = get_jwt_identity()
    admin_user = User.query.filter_by(username=current_user).first()

    if admin_user and admin_user.has_role("admin"):
        user_to_deactivate = User.query.get(user_id)

        if user_to_deactivate:
            user_to_deactivate.status = "Not Active"
            db.session.commit()
            return (
                jsonify(
                    {
                        "message": f"User '{user_to_deactivate.username}' deactivated successfully"
                    }
                ),
                200,
            )
        else:
            return jsonify({"message": "User not found"}), 404
    else:
        return jsonify({"error": "Unauthorized"}), 401


@app.route("/admin/categories", methods=["GET"])
@jwt_required()
@admin_required
# @cache.cached(timeout=30)
def get_all_categories():
    categories = Category.query.all()
    serialized_categories = [
        {"id": category.id, "name": category.name, "image_path": category.image_path, "status": category.status}
        for category in categories
    ]
    return jsonify({"categories": serialized_categories}), 200


@app.route("/categories", methods=["GET"])
@jwt_required()
def get_categories():
    categories = Category.query.filter_by(status="Active").all()
    serialized_categories = [
        {"id": category.id, "name": category.name, "image_path": category.image_path}
        for category in categories
    ]
    return jsonify({"categories": serialized_categories}), 200


@app.route("/categories/<int:category_id>", methods=["GET"])
@jwt_required()
@admin_or_manager_required
def get_category(category_id):
    category = Category.query.get(category_id)

    if category:
        serialized_category = {
            "id": category.id,
            "name": category.name,
            "image_path": category.image_path,
            "status": category.status,
        }
        return jsonify({"category": serialized_category}), 200
    else:
        return jsonify({"message": "Category not found"}), 404


@app.route('/admin/categories/<int:category_id>', methods=['PATCH'])
@jwt_required()
@admin_required
def toggle_category_status(category_id):
    try:
        category = Category.query.get(category_id)
        if not category:
            return jsonify({"error": "Category not found"}), 404

        # Toggle the category status
        category.status = 'Inactive' if category.status == 'Active' else 'Active'
        db.session.commit()

        return jsonify({"message": "Category status toggled successfully", "status": category.status}), 200

    except Exception as e:
        return jsonify({"message": "Internal server error", "error": str(e)}), 500


@app.route("/add-category", methods=["POST"])
@jwt_required()
@admin_required
def add_category():
    try:
        if "name" not in request.form or "image" not in request.files:
            return jsonify({"message": "Missing required data"}), 400

        category_name = request.form["name"]
        category_image = request.files["image"]

        if not allowed_file(category_image.filename):
            return jsonify({"message": "Invalid file type"}), 400

        secure_filename_category_image = secure_filename(category_image.filename)
        unique_filename = f"{random_string(10)}_{secure_filename_category_image}"
        image_path = os.path.join(app.config["UPLOAD_FOLDER"], unique_filename)
        category_image.save(image_path)

        new_category = Category(
            name=category_name, image_path=unique_filename, status="Active"
        )

        db.session.add(new_category)
        db.session.commit()

        return jsonify({"message": "Category added successfully"}), 201

    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"}), 500


@app.route("/edit-category/<int:categoryId>", methods=["PUT"])
@jwt_required()
@admin_required
def edit_category(categoryId):
    try:
        category = Category.query.get(categoryId)
        if not category:
            return jsonify({"message": "Category not found"}), 404

        if "name" not in request.form:
            return jsonify({"message": "Missing required data"}), 400

        category_name = request.form["name"]
        if "image" in request.files:
            category_image = request.files["image"]

            if not allowed_file(category_image.filename):
                return jsonify({"message": "Invalid file type"}), 400

            secure_filename_category_image = secure_filename(category_image.filename)
            unique_filename = f"{random_string(10)}_{secure_filename_category_image}"
            image_path = os.path.join(app.config["UPLOAD_FOLDER"], unique_filename)
            category_image.save(image_path)
        else:
            unique_filename = category.image_path

        category.name = category_name
        category.image_path = unique_filename

        db.session.commit()

        return jsonify({"message": "Category updated successfully"}), 200

    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"}), 500


@app.route('/products', methods=['GET'])
@jwt_required()
@manager_required
def get_all_products():
    try:
        categories = Category.query.all()
        products_by_category = {}
        
        for category in categories:
            products = Product.query.filter_by(category_id=category.id).all()
            products_data = [{'id': product.id, 'name': product.name, 'stock': product.stock, 'price_per_unit': product.price_per_unit, 'image_path': product.image_path, 'exp': product.exp.isoformat(), 'mfg': product.mfg.isoformat(), 'status': product.status, 'category_id': product.category_id}
                             for product in products]
            
            products_by_category[category.name] = products_data

        return jsonify({'products_by_category': products_by_category})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/products/<int:product_id>', methods=['GET'])
def get_product_details(product_id):
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({"error": "Product not found"}), 404

        product_data = {
            "id": product.id,
            "name": product.name,
            "stock": product.stock,
            "price_per_unit": product.price_per_unit,
            "exp": product.exp.isoformat(),
            "mfg": product.mfg.isoformat(),
            "category_id": product.category_id,
            # "image_path": product.image_path,
            "status": product.status,
        }

        return jsonify({"product": product_data})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route("/add-product/<int:category_id>", methods=["POST"])
@jwt_required()
@admin_or_manager_required
def add_product(category_id):
    try:
        required_fields = [
            "name",
            "stock",
            "price_per_unit",
            "exp",
            "mfg",
            "category_id",
        ]
        if (
            not all(field in request.form for field in required_fields)
            or "image" not in request.files
        ):
            return jsonify({"message": "Missing required data"}), 400

        product_name = request.form.get("name")
        stock = int(request.form.get("stock"))
        price_per_unit = int(request.form.get("price_per_unit"))
        exp = datetime.strptime(request.form.get("exp"), "%Y-%m-%d").date()
        mfg = datetime.strptime(request.form.get("mfg"), "%Y-%m-%d").date()
        product_image = request.files["image"]

        if not allowed_file(product_image.filename):
            return jsonify({"message": "Invalid file type"}), 400

        secure_filename_product_image = secure_filename(product_image.filename)

        unique_filename = f"{random_string(10)}_{secure_filename_product_image}"

        image_path = os.path.join(app.config["UPLOAD_FOLDER"], unique_filename)
        product_image.save(image_path)

        category = Category.query.get(category_id)
        if not category:
            return jsonify({"error": "Category not found"}), 404

        new_product = Product(
            name=product_name,
            stock=stock,
            price_per_unit=price_per_unit,
            exp=exp,
            mfg=mfg,
            image_path=unique_filename,
            category_id=category_id,
            status="Active",
        )

        category.products.append(new_product)
        db.session.add(new_product)
        db.session.commit()

        return jsonify({"message": "Product added successfully"}), 201

    except Exception as e:
        print(e)
        print("Product Name:", product_name)
        print("Stock:", stock)
        # ... add more print statements for other variables
        return jsonify({"message": "Internal server error"}), 500


@app.route("/edit-product/<int:product_id>", methods=["PUT"])
@jwt_required()
@manager_required
def edit_product(product_id):
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({"error": "Product not found"}), 404

        # Check if the required fields are present in the request
        required_fields = [
            "name",
            "stock",
            "price_per_unit",
            "exp",
            "mfg",
            "category_id",
        ]
        if not all(field in request.form for field in required_fields):
            return jsonify({"message": "Missing required data"}), 400

        # Update product fields based on the request data
        product.name = request.form.get("name")
        product.stock = int(request.form.get("stock"))
        product.price_per_unit = int(request.form.get("price_per_unit"))
        product.exp = datetime.strptime(request.form.get("exp"), "%Y-%m-%d").date()
        product.mfg = datetime.strptime(request.form.get("mfg"), "%Y-%m-%d").date()
        product.category_id = int(request.form.get("category_id"))

        # Check if a new image is provided and update the image_path accordingly
        if "image" in request.files:
            product_image = request.files["image"]
            if allowed_file(product_image.filename):
                secure_filename_product_image = secure_filename(product_image.filename)
                unique_filename = f"{random_string(10)}_{secure_filename_product_image}"
                image_path = os.path.join(app.config["UPLOAD_FOLDER"], unique_filename)
                product_image.save(image_path)
                product.image_path = unique_filename
            else:
                return jsonify({"message": "Invalid file type"}), 400

        db.session.commit()

        return jsonify({"message": "Product updated successfully"}), 200

    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"}), 500


@app.route('/products/<int:product_id>', methods=['PATCH'])
def toggle_product_status(product_id):
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404

        new_status = request.json.get('status')
        if new_status not in ['Active', 'Inactive']:
            return jsonify({'error': 'Invalid status'}), 400

        product.status = new_status
        db.session.commit()

        return jsonify({'message': f'Product status updated to {new_status}'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route("/manager/add-category", methods=["POST"])
@jwt_required()
@manager_required
def add_category_for_manager():
    try:
        if "name" not in request.form or "image" not in request.files:
            return jsonify({"message": "Missing required data"}), 400

        category_name = request.form["name"]
        category_image = request.files["image"]
        category_status = request.form["status"]

        if not allowed_file(category_image.filename):
            return jsonify({"message": "Invalid file type"}), 400

        secure_filename_category_image = secure_filename(category_image.filename)
        unique_filename = f"{random_string(10)}_{secure_filename_category_image}"
        image_path = os.path.join(app.config["UPLOAD_FOLDER"], unique_filename)
        category_image.save(image_path)

        new_category_change = CategoryChange(
            category_id=None,
            name=category_name,
            image_name=unique_filename,
            action="add",
            category_status=category_status,
            status_change="Pending",
        )

        db.session.add(new_category_change)
        db.session.commit()

        return jsonify({"message": "Category change added successfully"}), 201

    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"}), 500


@app.route("/update-category/<int:category_id>", methods=["PUT"])
@jwt_required()
@manager_required
def update_category(category_id):
    try:
        category = Category.query.get(category_id)
        if not category:
            return jsonify({"message": "Category not found"}), 404

        if "name" not in request.form or "status" not in request.form:
            return jsonify({"message": "Missing required data"}), 400

        category_name = request.form["name"]
        category_status = request.form["status"]

        # Check if a new image is provided
        if "image" in request.files:
            category_image = request.files["image"]

            if not allowed_file(category_image.filename):
                return jsonify({"message": "Invalid file type"}), 400

            secure_filename_category_image = secure_filename(category_image.filename)
            unique_filename = f"{random_string(10)}_{secure_filename_category_image}"
            image_path = os.path.join(app.config["UPLOAD_FOLDER"], unique_filename)
            category_image.save(image_path)
        else:
            unique_filename = category.image_path

        new_category_change = CategoryChange(
            category_id=category_id,
            name=category_name,
            image_name=unique_filename,
            action="update",
            category_status=category_status,
            status_change="Pending",
        )

        db.session.add(new_category_change)
        db.session.commit()

        return jsonify({"message": "Category change updated successfully"}), 200

    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"}), 500



@app.route("/manager/categories", methods=["GET"])
@jwt_required()
@manager_required
def get_all_manager_categories():
    categories = Category.query.all()
    serialized_categories = [
        {"id": category.id, "name": category.name, "image_path": category.image_path, "status": category.status}
        for category in categories
    ]
    return jsonify({"categories": serialized_categories}), 200



@app.route("/manager/delete-category/<int:category_id>", methods=["DELETE"])
@jwt_required()
@manager_required
def manager_delete_category(category_id):
    try:
        category = Category.query.get(category_id)
        if not category:
            return jsonify({"message": "Category not found"}), 404

        db.session.commit()

        new_category_change = CategoryChange(
            category_id=category_id,
            name=category.name,
            image_name=category.image_path,
            action="delete",
            category_status=category.status,
            status_change="Pending",
        )

        db.session.add(new_category_change)
        db.session.commit()

        return jsonify({"message": "Category status changed to Inactive"}), 200

    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"}), 500
    
    
# Admin endpoint to fetch pending category changes
@app.route("/admin/pending-category-changes", methods=["GET"])
@jwt_required()
@admin_required
def get_pending_category_changes():
    try:
        pending_changes = CategoryChange.query.filter_by(status_change="Pending").all()
        pending_changes_list = [
            {
                "id": change.id,
                "name": change.name,
                "image_name": change.image_name,
                "action": change.action,
                "category_status": change.category_status,
                "status_change": change.status_change,
            }
            for change in pending_changes
        ]

        return jsonify({"pendingCategoryChanges": pending_changes_list}), 200

    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"}), 500


@app.route("/admin/approve-category-change/<int:change_id>", methods=["PUT"])
@jwt_required()
@admin_required
def approve_category_change(change_id):
    try:
        category_change = CategoryChange.query.get(change_id)
        if not category_change:
            return jsonify({"message": "Category change request not found"}), 404

        category_change.status_change = "Approved"
        db.session.commit()

        process_category_change(category_change)

        return jsonify({"message": "Category change request approved"}), 200

    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"}), 500


@app.route("/admin/reject-category-change/<int:change_id>", methods=["PUT"])
@jwt_required()
@admin_required
def reject_category_change(change_id):
    try:
        category_change = CategoryChange.query.get(change_id)
        if not category_change:
            return jsonify({"message": "Category change request not found"}), 404

        category_change.status_change = "Rejected"
        db.session.commit()

        return jsonify({"message": "Category change request rejected"}), 200

    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"}), 500


def process_category_change(category_change):
    if category_change.action == "add":
        add_category(category_change)
    elif category_change.action == "update":
        update_category(category_change)
    elif category_change.action == "delete":
        delete_category(category_change)


def add_category(category_change):
    new_category = Category(
        name=category_change.name,
        image_path=category_change.image_name,
        status=category_change.category_status,
    )
    db.session.add(new_category)
    db.session.commit()


def update_category(category_change):
    category = Category.query.get(category_change.category_id)
    if category:
        category.name = category_change.name
        category.image_path = category_change.image_name
        category.status = category_change.category_status
        db.session.commit()


def delete_category(category_change):
    category = Category.query.get(category_change.category_id)
    if category:
        category.status = "Inactive"
        db.session.commit()

# ... your existing imports ...

@app.route("/user-dashboard", methods=["GET"])
@jwt_required()
def user_dashboard():
    try:
        categories = Category.query.filter_by(status="Active").all()
        serialized_categories = [
            {
                "id": category.id,
                "name": category.name,
                "image_path": category.image_path,
                "products": [
                    {
                        "id": product.id,
                        "name": product.name,
                        "stock": product.stock,
                        "price_per_unit": product.price_per_unit,
                        "exp": product.exp.isoformat(),
                        "mfg": product.mfg.isoformat(),
                        "image_path": product.image_path,
                    }
                    for product in category.products if product.status == 'Active'
                ],
            }
            for category in categories
        ]

        search_term = request.args.get("searchTerm", "").lower()

        if search_term:
            matching_products = [
                {
                    "id": product["id"],
                    "name": product["name"],
                    "stock": product["stock"],
                    "price_per_unit": product["price_per_unit"],
                    "exp": product["exp"],
                    "mfg": product["mfg"],
                    "image_path": product["image_path"],
                }
                for category in serialized_categories
                for product in category["products"] 
                if product["name"].lower().find(search_term) != -1
                or category["name"].lower().find(search_term) != -1
            ]

            return jsonify({"products": matching_products}), 200
        else:
            return jsonify({"categories": serialized_categories}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"}), 500


# New endpoint for applying filters
@app.route("/apply-filters", methods=["GET"])
@jwt_required()
def apply_filters():
    try:
        min_price = request.args.get("minPrice")
        max_price = request.args.get("maxPrice")
        mfg_date = request.args.get("mfgDate")
        exp_date = request.args.get("expDate")

        query = (
            db.session.query(Product)
            .join(Category, Product.category_id == Category.id)
            .filter(Category.status == "Active", Product.status == "Active")
        )

        if min_price:
            query = query.filter(Product.price_per_unit >= int(min_price))
        if max_price:
            query = query.filter(Product.price_per_unit <= int(max_price))
        if mfg_date and exp_date:
            mfg_date = parser.parse(mfg_date).date()
            exp_date = parser.parse(exp_date).date()
            query = query.filter(func.DATE(Product.mfg) <= mfg_date, func.DATE(Product.exp) >= exp_date)
        if mfg_date:
            mfg_date = parser.parse(mfg_date).date()
            query = query.filter(func.DATE(Product.mfg) <= mfg_date, func.DATE(Product.exp) >= mfg_date)
        if exp_date:
            exp_date = parser.parse(exp_date).date()
            query = query.filter(func.DATE(Product.mfg) <= exp_date, func.DATE(Product.exp) >= exp_date)
        

        filtered_products = query.all()

        serialized_products = [
            {
                "id": product.id,
                "name": product.name,
                "stock": product.stock,
                "price_per_unit": product.price_per_unit,
                "exp": product.exp.isoformat(),
                "mfg": product.mfg.isoformat(),
                "image_path": product.image_path,
            }
            for product in filtered_products
        ]

        return jsonify({"products": serialized_products}), 200

    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"}), 500


@app.route("/cart", methods=["GET"])
@jwt_required()
def get_cart():
    try:
        current_user = get_current_user()

        # Fetch the user's cart items with product details
        cart_items = (
            db.session.query(Cart, Product)
            .join(Product, Product.id == Cart.product_id)
            .filter(Cart.user_id == current_user.id)
            .all()
        )

        # Serialize the cart items
        serialized_cart = [
            {
                "id": cart.id,
                "product_id": product.id,
                "name": product.name,
                "quantity": cart.quantity,
                "price_per_unit": product.price_per_unit,
                "total_price": cart.quantity * product.price_per_unit,
                "stock": product.stock,
            }
            for cart, product in cart_items
        ]

        return jsonify({"cart": serialized_cart}), 200

    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"}), 500


def get_current_user():
    current_user_identity = get_jwt_identity()
    return User.query.filter_by(username=current_user_identity).first()


@app.route("/add-to-cart", methods=["POST"])
@jwt_required()
def add_to_cart():
    try:
        current_user = get_jwt_identity()
        user = User.query.filter_by(username=current_user).first()
        user_id = user.id
        data = request.get_json()

        product_id = data.get("product_id")
        quantity = data.get("quantity")

        # Validate the input
        if not product_id or not quantity or quantity <= 0:
            return jsonify({"message": "Invalid input."}), 400

        # Check if the item exists and is active
        item = Product.query.filter_by(id=product_id, status="Active").first()
        if not item:
            return jsonify({"message": "Item not found or inactive."}), 404

        # Check if the user already has the item in the cart
        cart_item = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()

        if not cart_item:
            # If the item is not in the cart, add it
            try:
                # Attempt to add the item to the cart
                new_cart_item = Cart(
                    user_id=user_id,
                    product_id=product_id,
                    quantity=quantity,
                    price=quantity * item.price_per_unit,
                )
                db.session.add(new_cart_item)

                # Commit changes to the database
                db.session.commit()

                return jsonify({"message": "Item added to the cart successfully."})

            except Exception as e:
                db.session.rollback()
                return (
                    jsonify({"message": f"Error adding item to the cart: {str(e)}"}),
                    500,
                )
        else:
            # If the item is already in the cart, update the quantity
            cart_item.quantity += quantity
            cart_item.price = cart_item.quantity * item.price_per_unit

            # Commit changes to the database
            db.session.commit()

            return jsonify({"message": "Quantity updated in the cart successfully."})

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error adding to cart: {str(e)}"}), 500


@app.route("/remove-from-cart/<int:product_id>", methods=["DELETE"])
@jwt_required()
def remove_from_cart(product_id):
    try:
        current_user = get_current_user()

        # Check if the product is in the user's cart
        cart_item = Cart.query.filter_by(
            user_id=current_user.id, product_id=product_id
        ).first()

        if not cart_item:
            return jsonify({"message": "Product not found in cart"}), 404

        db.session.delete(cart_item)
        db.session.commit()

        return jsonify({"message": "Product removed from cart successfully"}), 200

    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"}), 500


@app.route("/update-cart-quantity/<int:product_id>", methods=["PUT"])
@jwt_required()
def update_cart_quantity(product_id):
    try:
        # Product = Product.query.get(product_id)
        current_user = get_current_user()
        data = request.get_json()
        new_quantity = data.get("quantity")

        # Check if the product is in the user's cart
        cart_item = Cart.query.filter_by(
            user_id=current_user.id, product_id=product_id
        ).first()

        if not cart_item:
            return jsonify({"message": "Product not found in cart"}), 404

        # Update the quantity and price
        cart_item.quantity = new_quantity
        cart_item.price = new_quantity * cart_item.product.price_per_unit

        # if cart_item.quantity > Product.stock:
        #     return jsonify({"message": "Insufficient stock"}), 400

        db.session.commit()

        return jsonify({"message": "Cart quantity updated successfully"}), 200

    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"}), 500


@app.route("/place-order", methods=["POST"])
@jwt_required()
def place_order():
    try:
        current_user = get_current_user()

        # Fetch the user's cart items
        cart_items = Cart.query.filter_by(user_id=current_user.id).all()

        if not cart_items:
            return jsonify({"message": "Cart is empty"}), 400

        # Check product stock availability before placing the order
        for cart_item in cart_items:
            if cart_item.product.stock < cart_item.quantity:
                return (
                    jsonify(
                        {
                            "message": f"Insufficient stock for product: {cart_item.product.name}"
                        }
                    ),
                    400,
                )

        # Calculate the total price for the order
        total_price = sum(cart_item.price for cart_item in cart_items)

        # Create a new order
        new_order = Order(user_id=current_user.id, total_price=total_price,order_date=datetime.utcnow())

        # Create order items and add to the order
        for cart_item in cart_items:
            order_item = OrderProductAssociation(
                order=new_order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.price,
            )
            new_order.order_items.append(order_item)

            # Update product stock
            cart_item.product.stock -= cart_item.quantity
            cart_item.product.sold += cart_item.quantity

        # Remove products from the cart
        Cart.query.filter_by(user_id=current_user.id).delete()

        # Commit changes to the database
        db.session.add(new_order)
        db.session.commit()

        return jsonify({"message": "Order placed successfully"}), 201

    except NoResultFound:
        return jsonify({"message": "Product not found"}), 404

    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"}), 500


@app.route("/user-orders", methods=["GET"])
@jwt_required()
def get_user_orders():
    try:
        current_user = get_current_user()

        # Fetch the user's orders with product details
        orders = (
            Order.query
            .filter_by(user_id=current_user.id)
            .options(joinedload(Order.order_items).joinedload(OrderProductAssociation.product))
            .all()
        )

        # Serialize the orders
        serialized_orders = [
            {
                "id": order.id,
                "order_date": order.order_date.strftime("%Y-%m-%d"),
                "total_price": order.total_price,
                "order_items": [
                    {
                        "id": getattr(order_item, 'id', None),  # Safely get id attribute
                        "quantity": order_item.quantity,
                        "product": {
                            "id": order_item.product.id,
                            "name": order_item.product.name,
                            "price_per_unit": order_item.product.price_per_unit,
                        },
                    }
                    for order_item in order.order_items
                ],
            }
            for order in orders
        ]

        return jsonify({"orders": serialized_orders}), 200

    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error"}), 500


@celery.task()
def generate_csv():
    try:
        with app.app_context():
            products = Product.query.all()
            filename = 'products.csv'
            with open(filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Name", "Manufacture Date", "Expiry Date", "Rate Per Unit", "Disposed", "Stock Remaining", "Status"])
                for product in products:
                    writer.writerow([product.name, product.mfg, product.exp, product.price_per_unit, product.sold, product.stock, product.status])
            print(f"Task completed successfully. Returning filename: {filename}")
            return filename
    except Exception as e:
        # Log the exception
        print(f"An error occurred in generate_csv: {e}")
    raise e


@app.route('/download/products/csv', methods=['GET'])
@jwt_required()
def download_csv():
    try:
        task = generate_csv.delay()
        # task.wait()
        task.get()
        # Assuming send_file is a function that sends a file as a response
        response = send_file(task.result, as_attachment=True)

        return response

    except Exception as e:
        # Handle exceptions
        error_message = f"An error occurred: {str(e)}"
        return jsonify({'error': error_message}), 500


from sqlalchemy import or_

def get_inactive_users():
    # Get the current time minus 24 hours
    time_24_hours_ago = datetime.now() - timedelta(hours=24)

    # Get all users who have not logged in in the last 24 hours, have not logged in at all, have not made any purchases, and have the 'user' role
    inactive_users = User.query.join(User.roles).filter(
        Role.name == 'user',
        or_(
            User.last_login.is_(None),
            User.last_login < time_24_hours_ago,
            ~User.orders.any()  # 'orders' is the relationship field in User model
        ),
    ).all()

    return inactive_users


@celery.task(name='send_daily_reminder')
def send_daily_reminder():
    users = get_inactive_users()
    with app.app_context():
        for user in users:
            sub = "Nudge 📌" 
            body = "We've been missing your presence! Do drop by our site to explore our newest offerings." 
            send_mail(user.email, sub, body)


def generate_report(user):
    now = datetime.utcnow()
    one_month_ago = now - timedelta(days=30)
    orders = Order.query.filter(Order.user_id == user.id, Order.order_date >= one_month_ago).all()
    total_expenditure = sum(order.total_price for order in orders)
    body = render_template('monthly_report.html', total_expenditure=total_expenditure, user=user, orders=orders)

    return body


from sqlalchemy import text

@celery.task(name = 'send_monthly_report')
def send_monthly_report():
    users = User.query.join(User.roles).filter(Role.name == 'user').all()
    with app.app_context():
        for user in users:
            sub = "Monthly Report"
            body = generate_report(user)
            send_mail(user.email, sub, body)

if __name__ == "__main__":
    add_sample_data()
    app.run(debug=True)
