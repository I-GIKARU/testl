import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, fields, marshal
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///products.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

CLOUDINARY_FOLDER = os.getenv('CLOUDINARY_FOLDER', 'inventory')

# Models
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    images = db.relationship('ProductImage', backref='product', cascade="all, delete-orphan", lazy=True)


class ProductImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    image_url = db.Column(db.String(255))
    image_public_id = db.Column(db.String(255))


# Response marshalling
product_image_fields = {
    'id': fields.Integer,
    'image_url': fields.String
}

product_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'price': fields.Float,
    'quantity': fields.Integer,
    'images': fields.List(fields.Nested(product_image_fields))
}


# Resource
class ProductResource(Resource):
    def get(self, product_id=None):
        if product_id:
            product = Product.query.get_or_404(product_id)
            return marshal(product, product_fields)
        else:
            products = Product.query.all()
            return [marshal(product, product_fields) for product in products]

    def post(self):
        try:
            if request.is_json:
                data = request.get_json()
                product = Product(
                    name=data.get('name'),
                    description=data.get('description', ''),
                    price=float(data.get('price')),
                    quantity=int(data.get('quantity'))
                )
                db.session.add(product)
                db.session.commit()
                return marshal(product, product_fields), 201

            else:
                form = request.form
                name = form.get('name')
                price = form.get('price')
                quantity = form.get('quantity')
                description = form.get('description', '')

                if not name or not price or not quantity:
                    return {'error': 'Name, price, and quantity are required.'}, 400

                product = Product(
                    name=name,
                    description=description,
                    price=float(price),
                    quantity=int(quantity)
                )
                db.session.add(product)
                db.session.flush()  # To get product.id before committing

                files = request.files.getlist('images') or []
                for file in files:
                    if file:
                        upload_result = cloudinary.uploader.upload(file, folder=CLOUDINARY_FOLDER)
                        db.session.add(ProductImage(
                            product_id=product.id,
                            image_url=upload_result['secure_url'],
                            image_public_id=upload_result['public_id']
                        ))

                db.session.commit()
                return marshal(product, product_fields), 201

        except Exception as e:
            db.session.rollback()
            return {'error': f'Failed to create product: {str(e)}'}, 500

    def put(self, product_id):
        try:
            product = Product.query.get_or_404(product_id)

            if request.is_json:
                data = request.get_json()
                product.name = data.get('name', product.name)
                product.description = data.get('description', product.description)
                product.price = float(data.get('price', product.price))
                product.quantity = int(data.get('quantity', product.quantity))

            else:
                form = request.form
                product.name = form.get('name', product.name)
                product.description = form.get('description', product.description)
                product.price = float(form.get('price', product.price))
                product.quantity = int(form.get('quantity', product.quantity))

                # Handle image deletion
                kept_urls = form.getlist('existing_images')

                for image in product.images[:]:
                    if image.image_url not in kept_urls:
                        cloudinary.uploader.destroy(image.image_public_id)
                        db.session.delete(image)

                # Upload new images
                files = request.files.getlist('images') or []
                for file in files:
                    if file:
                        upload_result = cloudinary.uploader.upload(file, folder=CLOUDINARY_FOLDER)
                        db.session.add(ProductImage(
                            product_id=product.id,
                            image_url=upload_result['secure_url'],
                            image_public_id=upload_result['public_id']
                        ))

            db.session.commit()
            return marshal(product, product_fields)

        except Exception as e:
            db.session.rollback()
            return {'error': f'Failed to update product: {str(e)}'}, 500

    def delete(self, product_id):
        try:
            product = Product.query.get_or_404(product_id)

            # Delete images from Cloudinary
            for image in product.images:
                cloudinary.uploader.destroy(image.image_public_id)

            db.session.delete(product)
            db.session.commit()
            return {'message': 'Product deleted'}, 204

        except Exception as e:
            return {'error': f'Failed to delete product: {str(e)}'}, 500


# API routes
api.add_resource(ProductResource, '/api/products', '/api/products/<int:product_id>')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
