import json


class Wish:
    """Class representing a medication in wishlist

    Attributes:
        code: unique identifier of the product (string)
        name: name of the product (string)
        brand: the brand of the product (string)
        description: a textual description of the project (string)
        quantity: the quantity of products available in the stock (int)
        price: unit price of the project (float)
        dosage_instruction: instructions to take the medicine (string, optional)
        requires_prescription: whether the medication requires a prescription (bool)
        username: the username of the user

    """

    def __init__(
        self,
        code: str,
        name: str,
        brand: str,
        description: str,
        quantity: int,
        price: float,
        dosage_instruction: str,
        requires_prescription: bool,
        category: str,
        user: str,
    ) -> None:
        self.code = code
        self.name = name
        self.brand = brand
        self.quantity = quantity
        self.category = category
        self.description = description
        self.price = price
        self.dosage_instruction = dosage_instruction
        self.requires_prescription = requires_prescription != 0
        self.username = user

    def to_json(self) -> str:
        """Returns a valid JSON representation of the object

        Arguments:

        Returns: A JSON string.
        """

        data = {
            "code": self.code,
            "name": self.name,
            "brand": self.brand,
            "quantity": self.quantity,
            "category": self.category,
            "description": self.description,
            "price": self.price,
            "dosage_instruction": self.dosage_instruction,
            "requires_prescription": self.requires_prescription,
            "user": self.username,
        }

        json_data = json.dumps(data, indent=4)
        return json_data

    def __str__(self) -> str:
        return self.name
