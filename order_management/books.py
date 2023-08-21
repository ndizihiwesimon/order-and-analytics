from __future__ import annotations

import json
from datetime import datetime

from typing import List
from .sale import Sale


class BookRecords:
    """A record of all the sales made through the application.

    Attributes:
        transactions: a list of the transactions
    """

    def __init__(self, transactions: List[Sale]) -> None:
        self.transactions = transactions

    def __str__(self) -> str:
        """Returns a string representation of a record.

        Args:

        Returns: A string
        """

        # Code to return a representation of the records in following format
        # |      # | Date                | Customer   | Medication | Quantity | Purchase Price | Prescription |
        # |      1 | 2023-06-03 21:23:25 | doe        | Quinine    |        3 |       1400 RWF | PHA1         |

        record_str = (
            "|    # | Date                | Customer   | Medication | Quantity | Purchase Price | Prescription |\n"
            "|------|---------------------|------------|------------|----------|----------------|--------------|\n"
        )

        for idx, transaction in enumerate(self.transactions, start=1):
            timestamp = datetime.fromtimestamp(transaction.timestamp).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            if transaction.prescriptionID is None:
                transaction.prescriptionID = "None"
            record_str += (
                f"| {idx:4} | {timestamp} | {transaction.customerID:10} | {transaction.name:10} |"
                f" {transaction.quantity:8} | {transaction.purchase_price:10.2f} Rwf | {transaction.prescriptionID:12} |\n"
            )

        return record_str

    def reportOnPrescriptions(self) -> str:
        """Reports on prescription sales.

        Args:

        Returns: A string report of the prescriptions processed
        """
        # Retrieving for each prescription, the actual medications that were processed
        # and aggregating for each, the corresponding total price.

        # TThe format for the output:
        # |    # | Prescription ID | Total Price |

        prescription_report = {}
        for transaction in self.transactions:
            # Check if prescriptionID is not None
            if transaction.prescriptionID is not None:
                prescription_id = transaction.prescriptionID
                if prescription_id in prescription_report:
                    prescription_report[prescription_id] += transaction.purchase_price
                else:
                    prescription_report[prescription_id] = transaction.purchase_price

        report_str = (
            "|    # | Prescription ID |  Total Price  |\n"
            "|------|-----------------|---------------|\n"
        )

        for idx, (prescription_id, total_price) in enumerate(
            prescription_report.items(), start=1
        ):
            report_str += (
                f"| {idx:4} | {prescription_id:15} | {total_price:9.2f} Rwf |\n"
            )

        return report_str

    def purchasesByUser(self, customerID: str):
        """Reports on the sales performed by a customer.

        Args:
            customerID: Username of the customer.

        Returns: A string representation of the corresponding transactions

        """
        # TODO: Query the transactions to the `transactions` list below
        transactions = [
            transaction
            for transaction in self.transactions
            if transaction.customerID == customerID
        ]
        return BookRecords(transactions).__str__()

    def salesByAgent(self, salesperson: str):
        """Reports on the sales performed by a pharmacist.

        Args:
            salesperson: Username of the pharmacist.

        Returns: A string representation of the corresponding transactions

        """
        # TODO: Query the transactions to the `transactions` list below
        transactions = [
            transaction
            for transaction in self.transactions
            if transaction.salesperson == salesperson
        ]

        # return the string representation
        return BookRecords(transactions).__str__()

    def topNSales(
        self,
        start: datetime = datetime.strptime("2023-01-02", "%Y-%m-%d"),
        end: datetime = datetime.now(),
        n=10,
    ) -> str:
        """Return the top n sales ordered by the total price of purchases.

        Args:
            start: a datetime representing the start period to consider (datetime, default to 01 Jan 1970)
            end: a datetime representing the end period to consider (datetime, default to current timestamp)
            n: number of records to consider (int, default to 10)

        Returns:
        A string representation of the top n
        """
        # Codes to Query the top transactions and save them to the variable `transactions`
        transactions = sorted(
            [
                transaction
                for transaction in self.transactions
                if start <= datetime.fromtimestamp(transaction.timestamp) <= end
            ],
            key=lambda transaction: transaction.purchase_price,
            reverse=True,
        )[:n]

        # return the string representation of the transactions.
        return BookRecords(transactions).__str__()

    def totalTransactions(self) -> float:
        """Returns the total cost of the transactions considered.

        Args:

        Returns: A floating number representing the total price
        """
        return sum([transaction.purchase_price for transaction in self.transactions])

    @classmethod
    def load(cls, inFile: str) -> BookRecords:
        """Loads a JSON file containing a number of sales object

        Args:
            inFile: path to the file to be read
        Returns: A new object with the transactions in the file
        """
        # Loading JSON file that has sales objects
        try:
            with open(inFile, "r") as f:
                transactions_data = json.load(f)
                transactions = [
                    Sale(**transaction) for transaction in transactions_data
                ]
                return cls(transactions)
        except FileNotFoundError:
            raise Exception("Records file not found")
