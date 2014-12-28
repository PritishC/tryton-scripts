# A script to generate a shit-ton of products with attributes.
# Made to test filtering and faceting.
# Note: To be used only from within tryton_shell.
# Made By: Pritish Chakraborty
# License: Whatever Openlabs deems fit

from collections import defaultdict
from random import choice
from decimal import Decimal

from trytond.pool import Pool


class ProductGenerator:
    """
    Use to generate products with attributes.
    """

    def __init__(self, *args, **kwargs):
        """
        Get shit from the pool.
        """
        self.ProductTemplate = Pool().get('product.template')
        self.Product = Pool().get('product.product')
        self.ProductAttribute = Pool().get('product.attribute')
        self.ProductAttributeSet = Pool().get('product.attribute.set')
        self.Uom = Pool().get('product.uom')

        self.attr_collection = defaultdict(list)

    def create_attributes_structure(self):
        """
        Creates a viable data structure for easy random selection.
        Called only once.
        """
        attributes = self.ProductAttribute.search([('filterable', '=', True)])

        for attribute in attributes:
            attr_mappings = attribute.selection.split('\n')
            for mapping in attr_mappings:
                self.attr_collection[attribute.name].append(
                    mapping.split(':')[0]
                )

    def generate_random_attr_selection(self):
        """
        Generates a random attribute selection. Returns as a dictionary.
        """
        attr_selection = {}

        for attribute in self.attr_collection:
            attr_selection.update(
                {
                    attribute: choice(self.attr_collection[attribute])
                }
            )
        print "attr_selection is : %s" % attr_selection
        return attr_selection

    def generate_attributes(self):
        """
        Generates the attributes and attribute set. Called only once.
        """
        # Create attributes
        # By default, `filterable` is True.
        attribute1, = self.ProductAttribute.create([{
            'name': 'size',
            'type_': 'selection',
            'string': 'Size',
            'selection': 'm: M\nl:L\nxl:XL'
        }])
        attribute2, = self.ProductAttribute.create([{
            'name': 'color',
            'type_': 'selection',
            'string': 'Color',
            'selection': 'blue: Blue\nblack:Black\ngreen:Green\nyellow:Yellow'
        }])
        attribute3, = self.ProductAttribute.create([{
            'name': 'medium',
            'type_': 'selection',
            'string': 'Medium',
            'selection': 'digital: Digital\nphysical:Physical\nkindle:Kindle'
        }])

        # Create attribute set
        self.attrib_set, = self.ProductAttributeSet.create([{
            'name': 'attrSet',
            'attributes': [
                ('add', [attribute1.id, attribute2.id, attribute3.id])
            ]
        }])

        # While we're at it, create the data structure for easy random manip.
        self.create_attributes_structure()

    def generate_product_template(self, counter=1):
        """
        This method generates a product template, to be used to make variants.
        It then returns the template object for further manipulation.
        """
        uom, = self.Uom.search([], limit=1)

        template, = self.ProductTemplate.create([{
            'name': 'ProductTemplate' + '_' +str(counter),
            'type': 'goods',
            'list_price': Decimal('10'),
            'cost_price': Decimal('5'),
            'default_uom': uom.id,
            'attribute_set': self.attrib_set.id,
        }])
        return template

    def generate_variants(self, template):
        """
        This method creates three variants for the template with random
        attribute selections.
        """
        product1, = self.Product.create([{
            'template': template.id,
            'displayed_on_eshop': True,
            'uri': template.name + '_' + 'uri1',
            'code': template.name + '_' + 'code1',
            'attributes': self.generate_random_attr_selection(),
        }])

        product2, = self.Product.create([{
            'template': template.id,
            'displayed_on_eshop': True,
            'uri': template.name + '_' + 'uri2',
            'code': template.name + '_' + 'code2',
            'attributes': self.generate_random_attr_selection(),
        }])

        product3, = self.Product.create([{
            'template': template.id,
            'displayed_on_eshop': True,
            'uri': template.name + '_' + 'uri3',
            'code': template.name + '_' + 'code3',
            'attributes': self.generate_random_attr_selection(),
        }])

    def generate_all_products(self):
        """
        If shit goes right, generates a thousand products.
        Good luck.
        """
        self.generate_attributes()

        for i in range(1, 1001):
            template = self.generate_product_template(i)
            self.generate_variants(template)

