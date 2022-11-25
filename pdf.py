from fpdf import FPDF # to write PDF
import pdfplumber # to extract PDF text data

def extract_pdf_data(filepath: str):
    with pdfplumber.open(path_or_fp= filepath) as pdf:
        first_page = pdf.pages[0]
        return first_page.extract_text()

def create_new_pdf_content(content: str):
    pdf = FPDF(orientation= "P", unit= "pt") # pt unit is used in many applications
    pdf.add_page()

    pdf.set_font(family= "Times", size= 12)
    pdf.multi_cell(w= 0, h= 15, txt= content)

    desktop_path = "/Users/nirmalkumar/Desktop"
    pdf.output(f"{desktop_path}/corrected.pdf")

if __name__ == "__main__":
    create_new_pdf_content(content= "HIsssad ")