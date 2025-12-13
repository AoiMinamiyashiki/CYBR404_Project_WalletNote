import pytesseract
from PIL import Image
import re

from InputInformation import InputInformation


class OCR_System:
    """
    OCR system to extract text from images
    and convert it into structured input data.
    """

    def __init__(self, tesseract_cmd=None):
        """
        Optionally specify tesseract executable path (Windows support).
        """
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    def extract_text(self, image_path):
        """
        Extract raw text from image using Tesseract OCR.
        """
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text

    def parse_price(self, text):
        """
        Extract price value from OCR text.
        """
        matches = re.findall(r"\d+(?:,\d{3})*(?:\.\d+)?", text)
        if not matches:
            return None

        # Convert last detected number as price (common for receipts)
        price = matches[-1].replace(",", "")
        return float(price)

    def parse_date(self, text):
        """
        Extract date from OCR text (YYYY-MM-DD or similar).
        """
        match = re.search(r"\d{4}[-/]\d{2}[-/]\d{2}", text)
        if match:
            return match.group().replace("/", "-")
        return None

    def parse_service(self, text):
        """
        Extract service or product name.
        Uses the first non-numeric line as fallback.
        """
        lines = text.splitlines()
        for line in lines:
            if not re.search(r"\d", line) and len(line.strip()) > 3:
                return line.strip()
        return "Unknown"

    def image_to_input_information(self, image_path):
        """
        Convert image directly into InputInformation object.
        """
        text = self.extract_text(image_path)

        price = self.parse_price(text)
        date = self.parse_date(text)
        service = self.parse_service(text)

        if price is None or date is None:
            raise ValueError("OCR failed to extract required fields.")

        return InputInformation(
            price=price,
            date=date,
            service_or_product=service
        )
