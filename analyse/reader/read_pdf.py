import ocrmypdf, fitz

def make_pdf_readable(path):
    try:
        ocrmypdf.ocr(path, path, deskew=True, language='fra', skip_text=True)
    except Exception as e:
        print(f"Error while making pdf readable : {e}")


def get_text_pdf_fitz(path):
    doc = fitz.open(path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

def process_pdf(path):
    make_pdf_readable(path)
    text = get_text_pdf_fitz(path)
    return text