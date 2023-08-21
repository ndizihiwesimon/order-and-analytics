import json
from typing import List
from .product import Product


class Stock:
    """Represents the catalog of products

    Attributes:
        products: the list of products
    """

    def __init__(self, products: List[Product]) -> None:
        self.products = products

    def update(self, id: str, change: int):
        """Update the quantity of a product by adding or removing

        Args:
            id: identifier of the product
            change: the value by which the quantity should be update (+1 adds 1, -2 removes 2 for example)
        """

        # Updating the quantity of a product and writing back the updated quantity to the file
        product = self.getProductByID(id)
        new_quantity = product.quantity + (change)
        if new_quantity >= 0:
            product.quantity = new_quantity
            self.dump(outfile="data/products.json")
        else:
            print("Quantity cannot be negative")
            return

    def getProductByID(self, id: int) -> Product:
        """Gets a product by its ID

        Args:
            id: identifier of the product

        Returns: the product's object
        """
        # Returns a specific product depending on the product code/ID
        for product in self.products:
            if product.code == id:
                return product
        raise Exception("Product not found")

    def dump(self, outfile: str):
        """Saves the stock to a JSON file"""

        # Writing back to the original Stock JSON file (sales)
        product_list = []
        for product in self.products:
            product_dict = {
                "code": product.code,
                "name": product.name,
                "brand": product.brand,
                "description": product.description,
                "quantity": product.quantity,
                "price": product.price,
                "dosage_instruction": product.dosage_instruction,
                "requires_prescription": product.requires_prescription,
                "category": product.category,
            }
            product_list.append(product_dict)

        with open(outfile, "w") as f:
            json.dump(product_list, f, indent=4)

    @staticmethod
    def load(inFile: str):
        """Loads the stock from an existing file

        Args:
            inFile: input file to the function
        """

        # Loading data from the file
        try:
            with open(inFile, "r") as f:
                stock_data = json.load(f)
            products = [Product(**p) for p in stock_data]
            return Stock(products)
        except FileNotFoundError:
            raise Exception("Stock file not found")

    def __str__(self) -> str:
        """Returns a string representation of the stock"""

        # A string that shows the description of the stock with a nice output showing the ID, Name, Brand, Description, Quantity, Price, and the requires_prescription field
        stock_str = ""
        for product in self.products:
            stock_str += (
                f"ID: {product.code}\n"
                f"Name: {product.name}\n"
                f"Brand: {product.brand}\n"
                f"Description: {product.description}\n"
                f"Quantity: {product.quantity}\n"
                f"Price: ${product.price:.2f}\n"
                f"Requires Prescription: {product.requires_prescription}\n"
                f"Category: {product.category}\n"
                "----------------------\n"
            )
        return stock_str
