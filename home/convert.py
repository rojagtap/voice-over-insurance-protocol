from fpdf import FPDF
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from string import punctuation
from summarize import get_tokens
from cStringIO import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from PyPDF2 import PdfFileWriter
from pylatex import Document, Section, VerticalSpace, HorizontalSpace, Center, Command


def tokenize_content(content):
    stop_words = set(stopwords.words('english') + list(punctuation))
    words = word_tokenize(content.lower())

    return [
        sent_tokenize(content),
        [word for word in words if word not in stop_words]
    ]


def sanitize_input(data):
    data.replace('\f', ' ')
    data.replace('\n', ' ')
    data.replace('\t', ' ')
    data.replace('\r', '')
    return data


# converts pdf, returns its text content as a string
# noinspection PyShadowingNames
def convert(fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = file(fname, 'rb')
    count = 0
    for page in PDFPage.get_pages(infile, pagenums):
        count += 1

    if count <= 10:
        pagenums = (range(2, count - 2))
    else:
        pagenums = (range(5, count - 5))
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close()
    return text


def section(text):
    nText = ""
    for line in text.readlines():
        line = sanitize_input(line.decode('utf-8'))
        nText = nText + line

    sentence_tokens, word_tokens = tokenize_content(nText)
    text = open('input_file.txt', 'w')
    text.write(get_tokens(sentence_tokens, word_tokens).encode('utf-8'))


"""
text = convert("files/input/MotorSecure-Add-on-Covers-PolicyWordings.pdf", (3, 4, 5, 6, 7, 8, 9, 10, 11)).decode(
    'utf-8')
# text = open('files/input/input.txt').read().decode('utf-8')           # for text file testing
text = sanitize_input(text)
print(text)
"""
"""
sentence_tokens, word_tokens = tokenize_content(text)
output_file = open('files/output/output.txt', 'wb')
text = get_tokens(sentence_tokens, word_tokens).encode('utf-8')
# output_file.write(text)

output_file_pdf = open('files/output/output_pdf.pdf', 'wb')

doc = Document('summary')
doc.documentclass = Command(
    'documentclass',
    options=['conference'],
    arguments=['IEEEtran'],
)
with doc.create(Section('Summary:')):
    doc.append(text.decode('utf-8'))

doc.generate_pdf()
"""
