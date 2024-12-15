import requests
from behave import given

HTTP_OK = 200
HTTP_CREATED = 201
HTTP_NO_CONTENT = 204

@given('the following products')
def load_products(context):
    endpoint = f"{context.base_url}/products"
    context.response = requests.get(endpoint)
    assert context.response.status_code == HTTP_OK
    for product in context.response.json():
        context.response = requests.delete(f"{endpoint}/{product['id']}")
        assert context.response.status_code == HTTP_NO_CONTENT

    for row in context.table:
        data = {
            "name": row['name'],
            "description": row['description'],
            "price": row['price'],
            "available": row['available'] in ['True', 'true', '1'],
            "category": row['category']
        }
        context.response = requests.post(endpoint, json=data)
        assert context.response.status_code == HTTP_CREATED
