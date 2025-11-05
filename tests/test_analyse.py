import pytest
from unittest.mock import patch
from analyse.reader.read_pdf import process_pdf
from analyse.reader.read_txt import read_txt
from analyse.reader.read_classeur import read_classeur
from analyse.reader.read_docx import read_docx
from analyse.analyse import (
    find_extension, luhn_check, credit_card,
    find_phone_number, find_word_in_text, parse_dates
)

def test_find_extension():
    assert find_extension("document.pdf") == "pdf"
    assert find_extension("data.xlsx") == "xlsx"
    assert find_extension("file.txt") == "txt"
    assert find_extension("report.docx") == "docx"
    assert find_extension("unknownfile") == "unknownfile"


def test_luhn_check():
    assert luhn_check("4532015112830366")
    assert not luhn_check("1234567812345655")

def test_credit_card():
    text = "Here are some cards: 4532 0151 1283 0366 and 1234 5678 1234 5670."
    result = credit_card(text, "credit_card")
    assert result == {"credit_card": ["4532 0151 1283 0366", "1234 5678 1234 5670"]}

def test_find_phone_number():
    text = "Call me at +33 6 12 34 56 78"
    result = find_phone_number(text, "phone_number")
    assert result == {"phone_number": ["+33612345678"]}

def test_find_word_in_text():
    text = "This is a test text for finding words."
    assert find_word_in_text(text, "test")
    assert not find_word_in_text(text, "absent")

def test_parse_dates():
    input_dates = {"Date": ["12/01/2025", "2025-01-15", "12/31/2025"]}
    expected = {"Date": ["2025-01-12", "2025-01-15", "2025-12-31"]}
    result = parse_dates(input_dates)
    assert result == expected