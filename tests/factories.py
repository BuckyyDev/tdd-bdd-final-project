# Copyright 2016, 2022 John J. Rofrano. All Rights Reserved.
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

# pylint: disable=too-few-public-methods

"""
Test Factory to make fake objects for testing
"""
import factory
from factory.fuzzy import FuzzyChoice, FuzzyDecimal
from service.models import Product, Category


class ProductFactory(factory.Factory):
    """Creates fake products for testing"""

    class Meta:
        """Maps factory to data model"""

        model = Product

    id = factory.Sequence(lambda n: n)

    name = Faker('word')
    description = Faker('sentence')
    price = FuzzyDecimal(10.0, 1000.0, 2)
    category = FuzzyChoice([category.name for category in Category.query.all()])
    availability = FuzzyChoice([True, False])
    image_url = Faker('image_url')

    @classmethod
    def create_fake_product(cls):
        """Helper method to create a single fake product"""
        return cls.create()


    fake_product = ProductFactory.create_fake_product()
    print(fake_product.name, fake_product.price, fake_product.category)