import json

from .wish import Wish


class Wishlist:
    def __init__(self, user: str):
        self.username = user
        self.filename = "data/wishlist.json"
        self.items = self.load(self.filename)

    def add_to_wishlist(self, product):
        if product in self.items and self.items["user"] == self.username:
            print("Oops! This product is already on wishlist")
        else:
            self.items.append(product)
            self.dump()
            print("Product added to your wishlist")

    def remove_from_wishlist(self, product):
        if product in self.items:
            self.items.remove(product)
            self.dump()
            print("Product removed from wishlist")
        else:
            print("Oops! This product is not on wishlist")

    def show_wishlist(self):
        if not self.items:
            print("No items in your wishlist")
            return

        print("\n\t===== My wishlist =====")
        for i, product in enumerate(self.items):
            print(
                f"{i+1}. ID: {product.code}, Name: {product.name}, Price: ${product.price:.2f}, Quantity: {product.quantity}"
            )
        print()

    def dump(self):
        """Saves the stock to a JSON file"""

        # Writing back to the original Stock JSON file (sales)
        wish_list = []
        for item in self.items:
            product_dict = {
                "code": item.code,
                "name": item.name,
                "brand": item.brand,
                "description": item.description,
                "quantity": item.quantity,
                "price": item.price,
                "dosage_instruction": item.dosage_instruction,
                "requires_prescription": item.requires_prescription,
                "category": item.category,
                "user": self.username,
            }
            wish_list.append(product_dict)

        with open(self.filename, "w") as f:
            json.dump(wish_list, f, indent=4)

    def load(self, filename):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                user_data = [
                    Wish(**record) for record in data if record["user"] == self.username
                ]
                if user_data is None:
                    return []
                else:
                    return user_data
        except (FileNotFoundError, json.JSONDecodeError):
            return []
