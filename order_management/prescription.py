import json

from typing import List, Dict, Union
from .product import Product


class Prescription:
    """Represents a prescription object

    Attributes:
        DoctorName: the name of the doctor who gave the prescription
        PrescriptionID: ID of the prescription
        Medications: list of the medications, this is the quantity, the ID, the name, and whether it was processed or not
        # see format in prescriptions.json
        CustomerID: ID of the customer
    """

    def __init__(
        self,
        DoctorName: str,
        PrescriptionID: str,
        Medications: List[Dict[str, Union[int, str, bool]]],
        CustomerID: str,
        Date: str,
    ) -> None:
        self.DoctorName = DoctorName
        self.PrescriptionID = PrescriptionID
        self.Medications = Medications
        self.CustomerID = CustomerID

    def medicineInPrescription(self, product: Product, quantity: int) -> bool:
        """Verifies if a medicine with the specified quantity is included in a prescription

        Args:
            product: the product to verify
            quantity: the quantity to be added

        Returns: A boolean denoting whether the value was found
        """
        # Check if the quantity is within the specified prescription
        #
        for med in self.Medications:
            if med["ID"] == product.code and med["Quantity"] <= quantity:
                return True
        return False

    def markComplete(self, product: Product):
        """Mark a product's sale complete in the prescriptions file

        Args:
            product: the product sold

        Returns: None
        """
        # Changing the value "ProcessedStatus" of the relevant product to True
        for med in self.Medications:
            if med["ID"] == product.code:
                med["ProcessedStatus"] = True

    def dump(self, outfile: str):
        """Dumps the updated prescription to the specified file

        Args:
            outfile: path to the file where the output should be written

        Returns: None
        """

        #  Writing changes back to the original file
        try:
            with open(outfile, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = []

        for idx, prescription in enumerate(data):
            if prescription["PrescriptionID"] == self.PrescriptionID:
                data[idx] = self.__dict__  # Update the prescription object

        with open(outfile, "w") as f:
            json.dump(data, f, indent=4)

    @classmethod
    def get(cls, inFile: str, id: str):
        """Retrieves a specific prescription from a file

        Args:
            inFile: path to the input file
            id: identifier of the prescription to add

        Returns: A prescription object as a dictionary
        """

        #  Reading the file and returning relevant prescriptions depending on ID
        try:
            with open(inFile, "r") as f:
                data = json.load(f)
                for prescription in data:
                    if prescription["PrescriptionID"] == id:
                        return cls(**prescription)
        except FileNotFoundError:
            raise Exception("Prescriptions file not found")
