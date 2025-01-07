# Copyright 2016, 2023 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test cases for Product Model

Test cases can be run with:
    nosetests
    coverage report -m

While debugging just these tests it's convenient to use this:
    nosetests --stop tests/test_models.py:TestProductModel

"""
import os
import logging
import unittest
from decimal import Decimal
from service.models import Product, Category, db
from service import app
from tests.factories import ProductFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)


######################################################################
#  P R O D U C T   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestProductModel(unittest.TestCase):
    """Test Cases for Product Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Product.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Product).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_a_product(self):
        """It should Create a product and assert that it exists"""
        product = Product(name="Fedora", description="A red hat", price=12.50, available=True, category=Category.CLOTHS)
        self.assertEqual(str(product), "<Product Fedora id=[None]>")
        self.assertTrue(product is not None)
        self.assertEqual(product.id, None)
        self.assertEqual(product.name, "Fedora")
        self.assertEqual(product.description, "A red hat")
        self.assertEqual(product.available, True)
        self.assertEqual(product.price, 12.50)
        self.assertEqual(product.category, Category.CLOTHS)

    def test_add_a_product(self):
        """It should Create a product and add it to the database"""
        products = Product.all()
        self.assertEqual(products, [])
        product = ProductFactory()
        product.id = None
        product.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(product.id)
        products = Product.all()
        self.assertEqual(len(products), 1)
        # Check that it matches the original product
        new_product = products[0]
        self.assertEqual(new_product.name, product.name)
        self.assertEqual(new_product.description, product.description)
        self.assertEqual(Decimal(new_product.price), product.price)
        self.assertEqual(new_product.available, product.available)
        self.assertEqual(new_product.category, product.category)

    #
    # ADD YOUR TEST CASES HERE
    #

    def test_read_product(self):
        """It should Read a product from the database"""
        product = ProductFactory.create()
        read_product = Product.find_by_id(product.id)
        self.assertEqual(read_product.id, product.id)
        self.assertEqual(read_product.name, product.name)
        self.assertEqual(read_product.description, product.description)
        self.assertEqual(read_product.price, product.price)
        self.assertEqual(read_product.available, product.available)
        self.assertEqual(read_product.category, product.category)

    def test_update_product(self):
        """It should Update a product in the database"""
        product = ProductFactory.create()
        product.name = "Updated Fedora"
        product.description = "A red updated hat"
        product.price = 15.00
        product.available = False
        product.update()
        updated_product = Product.find_by_id(product.id)
        self.assertEqual(updated_product.name, "Updated Fedora")
        self.assertEqual(updated_product.description, "A red updated hat")
        self.assertEqual(updated_product.price, 15.00)
        self.assertEqual(updated_product.available, False)

    def test_delete_product(self):
        """It should Delete a product from the database"""
        product = ProductFactory.create()
        product_id = product.id
        product.delete()
        deleted_product = Product.find_by_id(product_id)
        self.assertIsNone(deleted_product)

    def test_list_all_products(self):
        """It should List all products in the database"""
        ProductFactory.create()
        ProductFactory.create()
        products = Product.all()
        self.assertEqual(len(products), 2)

    def test_find_by_name(self):
        """It should Find products by their name"""
        product = ProductFactory.create(name="Fedora")
        products = Product.find_by_name("Fedora")
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].name, "Fedora")

    def test_find_by_category(self):
        """It should Find products by their category"""
        category = Category.CLOTHS
        product = ProductFactory.create(category=category)
        products = Product.find_by_category(category)
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].category, category)

    def test_find_by_availability(self):
        """It should Find products by availability status"""
        product_available = ProductFactory.create(available=True)
        product_unavailable = ProductFactory.create(available=False)
        available_products = Product.find_by_availability(True)
        unavailable_products = Product.find_by_availability(False)
        self.assertEqual(len(available_products), 1)
        self.assertEqual(len(unavailable_products), 1)
        self.assertEqual(available_products[0].available, True)
        self.assertEqual(unavailable_products[0].available, False)

