from flask import Flask, render_template, request
import PyPDF2
import os

app = Flask(__name__)


def extractPDFText(path):
    file_obj = open(path, 'rb')
    pdf = PyPDF2.PdfFileReader(file_obj)

    text = ''
    for i in range(pdf.numPages):
        page = pdf.getPage(i)
        text = text + page.extractText()

    file_obj.close()
    return text


@app.route('/', methods=['GET', 'POST'])
def index():
    extracted_text = ''
    if request.method == 'POST':
        try:
            uploaded_file = request.files['file']
            uploaded_file.save('./mypdf.pdf')
            extracted_text = extractPDFText('mypdf.pdf')
            os.remove('mypdf.pdf')
        except Exception as ex:
            return render_template('index.html', extracted_text=ex)
    return render_template('index.html', extracted_text=extracted_text)


if __name__ == '__main__':
    app.run(debug=True)
