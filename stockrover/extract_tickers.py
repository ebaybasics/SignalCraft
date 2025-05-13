import fitz  # PyMuPDF
import re


def extract_tickers_from_pdf(pdf_path):
    """
    Extracts a sorted list of unique stock tickers from a PDF file.
    Tickers are assumed to be uppercase strings (with optional .V/.TO suffixes) found in tabular data.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        List[str]: Sorted list of unique tickers.
    """


    # Load the PDF
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()

    # Extract ticker-like patterns
    tickers = re.findall(r'\b[A-Z]{1,5}(?:\.[A-Z]{1,3})?\b', full_text)
    ticker_set = set(t for t in tickers if len(t) >= 2 and not t.isdigit())

    return sorted(ticker_set)