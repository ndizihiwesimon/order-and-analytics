import uuid
from .cart import Cart
from .stock import Stock
from .product import Product
from .prescription import Prescription
import time
import json


## would need to create a new object for each new order
class Wrapper:
    """
    Main class used to manage orders and carts.

    Attributes:
        sales: A list of the sales done during the program's execution
        stock: The stock used in the execution
        agentID: the username of the pharmacist running the program
    """

    def __init__(self, stock: Stock, agentID: str) -> None:
        self.sales = []
        self.stock = stock
        self.agentID = agentID

    def checkout(self, cart: Cart, customerID: str, prescription: Prescription = None):
        """Handles the checkout procedure of the program.

        Args:
            cart: The cart to pay for
            prescription: the prescription that accompanies the order (default: None)
        """

        # First check that all the products that require a prescription have all the criteria met
        try:
            if cart.products.items():
                for product_id, quantity in cart.products.items():
                    product = self.stock.getProductByID(product_id)
                    if product.requires_prescription:
                        if prescription is None:
                            print(
                                f"\nProduct '{product.name}' requires a prescription."
                            )
                            return
                        if not prescription.medicineInPrescription(product, quantity):
                            print(
                                f"Prescription does not contain '{product.name}' in the required quantity."
                            )
                            return

                # Get the current datetime
                timestamp = time.time()

                # Generate sale information for each product sold
                sale_entries = []
                for product_id, quantity in cart.products.items():
                    product = self.stock.getProductByID(product_id)
                    if prescription is None:
                        pres_id = None
                    else:
                        pres_id = prescription.PrescriptionID
                    sale_entry = {
                        "id": uuid.uuid4().hex[:4],
                        "name": product.name,
                        "quantity": quantity,
                        "price": product.price,
                        "purchase_price": product.price * quantity,
                        "timestamp": timestamp,
                        "customerID": customerID,
                        "salesperson": self.agentID,
                        "prescriptionID": pres_id,
                    }
                    sale_entries.append(sale_entry)
                    change = -quantity
                    self.stock.update(product.code, change)

                    # Mark the product as complete in the prescription
                    if prescription is not None:
                        prescription.markComplete(product)

                # Append the sales entries to the current sales list
                self.sales.extend(sale_entries)
                self.dump("data/sales.json")
                cart.clear()
                print(
                    "\n Checkout completed successfully!\n Thank you for shopping with us!"
                )
            else:
                print("Your cart is empty!")
        except:
            print("Something went wrong! Could not complete checkout!")

    def dump(self, outfile: str):
        """Dumps the current sales data to a file

        Args:
            outfile: the path to the output file
        """

        # Writing the current sales to the sales.json file
        try:
            with open(outfile, "r") as f:
                existing_sales = json.load(f)
        except FileNotFoundError:
            existing_sales = []

        with open(outfile, "w") as f:
            all_sales = existing_sales + self.sales
            json.dump(all_sales, f, indent=4)
