from .product import Product
from .stock import Stock


class Cart:
    """Represents a cart with a list of products and quantity

    Attributes:
        products: a dictionary with the key being the ID of the products, and the value being the quantity
        added
    """

    def __init__(self, stock: Stock) -> None:
        self.products = {}
        self.stock = stock

    def add(self, productCode: str, quantity: int):
        """Adds a product to the cart with the specified quantity

        Args:
            productCode: the identifier of the product
            quantity: quantity to add

        Returns: None
        """

        # Make sure the quantity is valid (> 0 and <= the quantity in the stock)
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")

        product = self.stock.getProductByID(productCode)

        if quantity > product.quantity:
            print("Not enough stock available")
            return

        # If the product was already in the cart, increment the quantity
        if productCode in self.products:
            self.products[productCode] += quantity
            print("Quantity increase by " + str(quantity))
        else:
            self.products[productCode] = quantity
            print("Product added to cart successfully")

    def __str__(self) -> str:
        """String representation of the cart"""
        # Returns a string representation of a cart that shows the products, their quantity, unit price, total price. And also the total price of the cart
        cart_str = ""
        total_cart_cost = 0

        for product_code, quantity in self.products.items():
            product = self.stock.getProductByID(product_code)
            total_price = quantity * product.price
            cart_str += (
                f"\nID: {product.code}\n"
                f"Name: {product.name}\n"
                f"Quantity: {quantity}\n"
                f"Unit Price: ${product.price:.2f}\n"
                f"Total Price: ${total_price:.2f}\n"
                "----------------------\n"
            )
            total_cart_cost += total_price

        cart_str += f"Total Cart Cost: ${total_cart_cost:.2f}\n"
        return cart_str

    def remove(self, code):
        """
        Removes a specific product from the cart"""
        # Removes a product from the cart. safely fail if the product code is not found
        try:
            if code in self.products:
                del self.products[code]
                print("Product removed successfully!")
        except:
            print("Product not found")

    def clear(self):
        """Clears up the cart."""
        self.products.clear()

    @property
    def cost(self):
        """Returns the total cost of the cart"""
        # Function that returns the total cost of the cart
        total_cost = 0
        for product_code, quantity in self.products.items():
            product = self.stock.getProductByID(product_code)
            total_cost += product.price * quantity
        return total_cost
