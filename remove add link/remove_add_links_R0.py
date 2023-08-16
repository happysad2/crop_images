from pdfrw import PdfReader, PdfWriter

def remove_links(pdf):
    # Iterate through pages and remove all annotations
    for page in pdf.pages:
        page.Annots = []

def add_invisible_link(pdf, link_url):
    # Define the link annotation with the URL
    link_annotation = '''<<
        /Type /Annot
        /Subtype /Link
        /Rect [0 0 1000 1000]
        /Border [0 0 0]
        /A << /S /URI /URI ({link}) >>
        /C [1 1 1] % White color for invisible effect
    >>'''.format(link=link_url)

    # Add the link annotation to each page
    for page in pdf.pages:
        if '/Annots' not in page:
            page.Annots = []
        page.Annots.append(link_annotation)

def main():
    # Path to the existing PDF
    input_pdf = '/Users/jackperry/Downloads/Barbie_Fantasy_Land_Room_Prints_Set_6.pdf'

    # URL to be added as a link
    link_url = 'https://drive.google.com/drive/folders/1fJrukoZGmaSSWb01AkPsNKZgmlDCshuZ?usp=sharing'

    # Read the PDF
    pdf = PdfReader(fdata=open(input_pdf, 'rb').read())

    # Remove existing links
    remove_links(pdf)

    # Add invisible link
    add_invisible_link(pdf, link_url)

    # Write the modified PDF to the same file
    PdfWriter().write(input_pdf, pdf)

    print(f"PDF processed. Invisible link to {link_url} added.")

if __name__ == '__main__':
    main()
