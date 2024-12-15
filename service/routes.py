from flask import jsonify, request, abort
from flask import url_for
from service.models import Product, Category
from service.common import status
from . import app

@app.route("/health")
def healthcheck():
    return jsonify(status=200, message="OK"), status.HTTP_200_OK

@app.route("/")
def index():
    return app.send_static_file("index.html")

def validate_content_type(expected_type):
    if "Content-Type" not in request.headers:
        abort(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, f"Content-Type must be {expected_type}")
    if request.headers["Content-Type"] != expected_type:
        abort(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, f"Content-Type must be {expected_type}")

@app.route("/products", methods=["POST"])
def create_product():
    validate_content_type("application/json")
    data = request.get_json()
    product = Product()
    product.deserialize(data)
    product.create()
    response_data = product.serialize()
    location = url_for("retrieve_product", product_id=product.id, _external=True)
    return jsonify(response_data), status.HTTP_201_CREATED, {"Location": location}

@app.route("/products/<int:product_id>", methods=["GET"])
def retrieve_product(product_id):
    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found.")
    return product.serialize(), status.HTTP_200_OK

@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    validate_content_type("application/json")
    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found.")
    product.deserialize(request.get_json())
    product.id = product_id
    product.update()
    return product.serialize(), status.HTTP_200_OK

@app.route("/products", methods=["GET"])
def get_products():
    products = []
    name_filter = request.args.get("name")
    category_filter = request.args.get("category")
    availability_filter = request.args.get("available")

    if name_filter:
        products = Product.find_by_name(name_filter)
    elif category_filter:
        category_value = getattr(Category, category_filter.upper())
        products = Product.find_by_category(category_value)
    elif availability_filter:
        available_value = availability_filter.lower() in ["true", "yes", "1"]
        products = Product.find_by_availability(available_value)
    else:
        products = Product.all()

    results = [product.serialize() for product in products]
    return results, status.HTTP_200_OK

@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    product = Product.find(product_id)
    if product:
        product.delete()
    return "", status.HTTP_204_NO_CONTENT
