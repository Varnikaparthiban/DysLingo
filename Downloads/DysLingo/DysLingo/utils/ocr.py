from PIL import Image
import pytesseract

ALLOWED = {"png", "jpg", "jpeg", "bmp", "tif", "tiff"}

def extract_text_from_image(file_storage):
    filename = (file_storage.filename or "").lower()
    ext = filename.rsplit(".", 1)[-1] if "." in filename else ""
    if ext not in ALLOWED:
        raise ValueError("Upload a PNG, JPG, JPEG, BMP, or TIFF image.")
    try:
        image = Image.open(file_storage.stream)
        return pytesseract.image_to_string(image, lang="eng+tam+hin").strip()
    except pytesseract.TesseractNotFoundError:
        raise RuntimeError("OCR needs the Tesseract application installed on your computer. See README.md for setup instructions.")
    except Exception as exc:
        if "tesseract" in str(exc).lower():
            raise RuntimeError("OCR engine or language data is missing. See README.md for setup instructions.")
        raise
