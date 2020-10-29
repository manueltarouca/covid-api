from urllib.request import urlopen
from lxml import etree
import requests
import shutil

from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

_url = "https://covid19.min-saude.pt/relatorio-de-situacao/"
_valid = 168


def get_urls():
    response = urlopen(_url)
    htmlparser = etree.HTMLParser()
    tree = etree.parse(response, htmlparser)
    arr_url = tree.xpath(
        "//a[contains(text(),'Relatório de Situação nº')]/@href")
    arr_titles = tree.xpath(
        "//a[contains(text(),'Relatório de Situação nº')]/text()")

    return {
        "urls": arr_url,
        "titles": arr_titles,
    }


def valid_urls(last_title, arr_urls):
    n_valid = int(last_title.split(" ")[4]) - _valid
    return arr_urls[0:n_valid]


def get_data(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0'
    }

    r = requests.get(url, stream=True, headers=headers)

    if r.status_code == 200:
        image = r.raw

        with open('./teste.pdf', 'wb') as _file:
            shutil.copyfileobj(image, _file)
            fich = "teste.pdf"
    else:
        print('erro ao fazer request')

    print(url.split("/")[-1] + " - " + read_casos(fich))


def read_casos(path):
    output_string = StringIO()
    with open(path, 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)

    arr = output_string.getvalue().split("\n")
    arr = list(filter(str.strip, arr))
    return arr[arr.index("CONFIRMADOS")-1].split("+")[-1].strip()

def main():
    di = get_urls()
    arr_valid = valid_urls(di.get("titles")[0], di.get("urls"))
    # get_data("https://covid19.min-saude.pt/wp-content/uploads/2020/09/206_DGS_boletim_20200924.pdf")
    for i in arr_valid:
        get_data(i)
    # print(di.get("titles"))


if __name__ == "__main__":
    main()
