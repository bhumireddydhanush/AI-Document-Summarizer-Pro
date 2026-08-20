import PyPDF2

def extract_text_from_pdf(uploaded_file):
    text = ""

    reader = PyPDF2.PdfReader(uploaded_file)

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text 