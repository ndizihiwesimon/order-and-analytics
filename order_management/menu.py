from . import (
    Stock,
    Cart,
    User,
    UserManagement,
    BookRecords,
    Wrapper,
    Wishlist,
    Prescription,
)

MSG_WRONG_INPUT = "Wrong input. Try again!"


class Menu:
    """Represents the menu class for the project

    Attributes:
        stock: stock variable
        profiles: user management module
        pharmacist: account of the salesperson
        records_file: path to the file containing the sales
        prescriptions_file: path to the file containing the prescriptions.
        stock_file: path to the file containing the stock data
    """

    def __init__(
        self,
        stock: Stock,
        profiles: UserManagement,
        pharmacist: User,
        wrap: Wrapper,
        wishlist: Wishlist,
        records_file: str,
        prescriptions_file: str,
        stock_file: str,
    ) -> None:
        self.stock = stock
        self.profiles = profiles
        self.pharmacist = pharmacist
        self.cart = Cart(stock=stock)
        self.wrap = wrap
        self.wishlist = wishlist
        self.books = BookRecords.load(records_file)
        # use the file instead of the object so that we can keep track
        self.records_file = records_file
        self.prescriptions_file = prescriptions_file
        self.stock_file = stock_file

    """
    1. Order management
        1.1. Adding to a cart (you need to show the list of products and ask the user to select one with ID. Bonus: Can you display with numbers and ask user to choose a number instead?
                Also ask for quantity.)
        1.2. Remove from a cart (display the cart and ask the user to select the element to remove. Remove by ID or by index (bonus))
        1.3. Clear the cart (self explanatory)
        1.4. Checkout (displays the cart with the total and ask for a prescription element. Proceed to checkout and show a message is successful or not).
    2. Analytics
        2.1. Total income from purchases
        2.2. Prescription statistics
        2.3. Purchases for a user
        2.4. Sales by an agent
        2.5. Top sales

    * For each of the menu items, when necessary, display a success or error message to guide the user.
    """

    # **CHALLENGE** (BONUS): Can you implement the menu to work as a USSD application? Implement and show your design

    # MENU ALLOWS USER TO NAVIGATE THROUGH THE APP BACK AND FORTH

    def show_main_menu(self):
        while True:
            print("\nMain Menu:")
            print("1. Order management")
            print("2. Analytics")
            print("3. Exit")
            choice = input("\nChoose an option: ")

            if choice == "1":
                self.order_management_menu()
            elif choice == "2":
                self.books = BookRecords.load("data/sales.json")
                self.analytics_menu()
            elif choice == "3":
                print("\nExiting the program...")
                break
            else:
                print(MSG_WRONG_INPUT)

    def order_management_menu(self):
        while True:
            print("\nOrder Management Menu:")
            print("1. Adding to cart")
            print("2. Remove from cart")
            print("3. Clear the cart")
            print("4. Checkout")
            print("5. Add to Wishlist")
            print("6. Display Wishlist")
            print("7. Back to main menu")
            choice = input("\nChoose an option: ")

            if choice == "1":
                print("\n Select from Product List:")
                # listing products list for the user to be able to select from it before adding them to cart
                for i, product in enumerate(self.stock.products):
                    print(
                        f"\t {i+1}. ID: {product.code}, Name: {product.name}, Price: ${product.price:.2f}, Quantity: {product.quantity}"
                    )
                print()

                #  Prompt user to input the selected product until it is correct number
                while True:
                    product_no = int(input("Enter the # product to add to your cart: "))
                    if 1 <= product_no <= len(self.stock.products):
                        break
                    print(
                        "Invalid input. Please enter a number from 1 to",
                        len(self.stock.products),
                    )
                product_id = self.stock.products[product_no - 1].code
                quantity = int(input("Enter Quantity: "))
                self.cart.add(productCode=product_id, quantity=quantity)

            elif choice == "2":
                if bool(self.cart.products):
                    # Displaying the content of the cart before removing items
                    print(self.cart.__str__())
                    product_id = input("Enter the Product ID you want to remove: ")
                    self.cart.remove(code=product_id)
                else:
                    print("\nYour cart is empty!")

            elif choice == "3":
                self.cart.clear()
                print("Cart cleared.")

            elif choice == "4":
                try:
                    self.wrap.checkout(
                        cart=self.cart,
                        customerID=self.profiles.get_logged_in_user().username,
                    )
                except:
                    print("Something went wrong! Can't checkout")
            elif choice == "5":
                print("\n Available medications: \n")
                # listing products list for the user to be able to select from it before adding them to cart
                for i, product in enumerate(self.stock.products):
                    print(
                        f"\t {i+1}. ID: {product.code}, Name: {product.name}, Price: ${product.price:.2f}, Quantity: {product.quantity}"
                    )
                print()

                #  Prompt user to input the selected product until it is correct number
                while True:
                    product_no = int(
                        input("Enter the # product to add to your wishlist: ")
                    )
                    if 1 <= product_no <= len(self.stock.products):
                        break
                    print(
                        "Invalid input. Please enter a number from 1 to",
                        len(self.stock.products),
                    )
                product_id = self.stock.products[product_no - 1].code
                medicine = self.stock.getProductByID(id=product_id)
                self.wishlist.add_to_wishlist(medicine)

            elif choice == "6":
                self.wishlist.show_wishlist()

            elif choice == "7":
                break
            else:
                print(MSG_WRONG_INPUT)

    def analytics_menu(self):
        while True:
            print("\nAnalytics Menu:")
            print("1. Total income from purchases")
            print("2. Prescription statistics")
            print("3. Purchases for a user")
            print("4. Sales by an agent")
            print("5. Top sales")
            print("6. Back to main menu")

            choice = input("\nChoose an option: ")

            if choice == "1":
                total_income = self.books.totalTransactions()
                print(f"\nTotal income from purchases: {total_income:.2f} Rwf")
            elif choice == "2":
                print(f"\nPrescription Statistics\n")
                print(self.books.reportOnPrescriptions())
            elif choice == "3":
                customer_id = input("\nEnter customer ID: ")
                print(self.books.purchasesByUser(customerID=customer_id))

            elif choice == "4":
                agent_username = input("\nEnter agent's username: ")
                print(self.books.salesByAgent(salesperson=agent_username))
            elif choice == "5":
                print("\nTop 10 Sales from 2017\n")
                print(self.books.topNSales())
            elif choice == "6":
                break
            else:
                print(MSG_WRONG_INPUT)
