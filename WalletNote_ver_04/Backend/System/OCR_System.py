import pytesseract
import cv2
import re
from datetime import datetime

class OCR_System:
    def __init__(self, tesseract_path=None):
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path

    def scan_receipt(self, image_path: str) -> dict:
        image = self._preprocess(image_path)
        text = pytesseract.image_to_string(image, lang="eng")

        return {
            "date": self._extract_date(text),
            "amount": self._extract_amount(text),
            "category": self._guess_category(text),
            "raw_text": text.strip()
        }

    #/* ---------- Preprocess ---------- */
    def _preprocess(self, path):
        img = cv2.imread(path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5,5), 0)
        thresh = cv2.adaptiveThreshold(
            blur, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2
        )
        return thresh

    #/* ---------- Amount ---------- */
    def _extract_amount(self, text):
        matches = re.findall(r'(\$?\d+\.\d{2})', text)
        if matches:
            return float(matches[-1].replace("$", ""))
        return None

    #/* ---------- Date ---------- */
    def _extract_date(self, text):
        patterns = [
            r'(\d{4}[-/]\d{2}[-/]\d{2})',
            r'(\d{2}[-/]\d{2}[-/]\d{4})'
        ]
        for p in patterns:
            m = re.search(p, text)
            if m:
                return self._normalize_date(m.group(1))
        return None

    def _normalize_date(self, s):
        for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%m/%d/%Y", "%d/%m/%Y"):
            try:
                return datetime.strptime(s, fmt).strftime("%Y-%m-%d")
            except:
                pass
        return None

    #/* ---------- Category ---------- */
    def _guess_category(self, text):
        text = text.lower()
        categories = {
            "Food": ["restaurant", "cafe", "coffee", "food"],
            "Transport": ["uber", "taxi", "train"],
            "Shopping": ["store", "shop", "market"],
            "Entertainment": ["movie", "cinema", "netflix"]
        }
        for cat, keys in categories.items():
            if any(k in text for k in keys):
                return cat
        return "Other"
