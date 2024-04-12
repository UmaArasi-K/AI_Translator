from fpdf import FPDF
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from PyPDF2 import PdfReader

# Initialize the model and tokenizer for translation
tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M")
translator = pipeline('translation', model=model, tokenizer=tokenizer, max_length=400)

# Function to extract sentences from text
def extract_sentences(text):
    sentences = text.split('.')
    return [sentence.strip() for sentence in sentences if sentence.strip()]

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = " "
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

def write_translated_text_to_pdf(translated_text):
    pdf = FPDF()
    pdf.add_page()
    try:
        pdf.add_font('NotoSansTamil-Black', '', 'C:/Users/umaar/NotoSansTamil-Black.ttf', uni=True)
        pdf.set_font('NotoSansTamil-Black', size=12)
    except Exception as pdfer:
        print("exception",pdfer)
    print("add and set font done")
    for line in translated_text:
        words = line.split()
        current_line = ''
        for word in words:
            if pdf.get_string_width(current_line + ' ' + word) <= 2700:
                current_line += ' ' + word
            else:
                # Add the line to PDF
                pdf.cell(0, 10, current_line.strip(), 0, 1, 'J')
                current_line = word
        if current_line:
            # Add the remaining line to PDF
            pdf.cell(0, 10, current_line.strip(), 0, 1, 'J')

        # Check if the current line has filled the page width
        if pdf.get_y() > 270:  # Adjust the value based on your PDF margins
            pdf.add_page()  # Add a new page if the current page is filled
    print("printing output")
    # Output the PDF to the specified path
    pdf.output('C:/Users/umaar/1.pdf')

def main(pdf_path, source_language, target_language):
    # Extract text from PDF
    print("extracting text")

    pdf_text = extract_text_from_pdf(pdf_path)
    # Extract sentences from PDF text
    print("extracted,split sentences")
    sentences = extract_sentences(pdf_text)
    print("starting translation")
    # Translate each sentence and store the translations
    translated_text = []
    for sentence in sentences:
        translated_sentence = translator(sentence, src_lang=source_language, tgt_lang=target_language)[0]['translation_text']
        translated_text.append(translated_sentence)
    print("pdf write")
    # Write translated text to PDF
    write_translated_text_to_pdf(translated_text)
