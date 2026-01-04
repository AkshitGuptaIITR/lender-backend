from paddleocr import PaddleOCR


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extracts text from a PDF file using PaddleOCR.
    It renders each page as an image and performs OCR on it.
    """
    ocr = PaddleOCR(lang="en", use_angle_cls=True)

    try:
        extracted_text = []
        for i, res in enumerate(ocr.predict_iter(file_path)):
            extracted_text.append("\n".join(res["rec_texts"]))
        return "\n".join(extracted_text)

    except Exception as e:
        print(f"Error processing PDF {file_path}: {e}")
        return ""
