from flask import Flask, jsonify
import PyPDF2
import os
import requests
import shutil
import datetime
from urllib.request import urlopen
from lxml import etree


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def casos():

    # read local html file and set up lxml html parser
    local = "https://covid19.min-saude.pt/relatorio-de-situacao/"
    response = urlopen(local,)
    htmlparser = etree.HTMLParser()
    tree = etree.parse(response, htmlparser)
    url = tree.xpath(
        "//a[contains(text(),'Relatório de Situação nº')]/@href")[0]
    url2 = tree.xpath(
        "//a[contains(text(),'Relatório de Situação nº')]/text()")[0]

    print(bcolors.WARNING + "\nInformação Retirada do", url2, "\n" + bcolors.ENDC)
    datapdf = url2.split(" ")

    # print(datapdf[-1]) #Data retirada do texto do link da pagina
    today = datetime.datetime.now()
    #print (today)

    dia = today.strftime('%j')
    # print(dia do ano - começo do covid)
    year = today.year
    month = int(today.strftime('%m'))
    diad = int(dia)-62

    # devolve o dia da semana da variável
    dt = datapdf[-1]
    day, month, year = (int(x) for x in dt.split('/'))
    ans = datetime.date(year, month, day)
    diaS = ans.strftime("%A")
    # print(diaS)
    ##############################

    if (today.strftime('%d/%m/%Y') == (datapdf[-1])):
        print(bcolors.BOLD + "Dados de Hoje \n" + bcolors.ENDC)
    else:

        print(bcolors.FAIL + "Dados do dia: %s" % (datapdf[-1]) + bcolors.ENDC)

    #testeemsept = datetime.datetime.today() - datetime.timedelta(days=30)
    # print(testeemsept.strftime('%m'))
    #print('https://covid19.min-saude.pt/wp-content/uploads/%d/%d/%d_DGS_boletim_%d.pdf' % (year, month, diad, int(today.strftime("%Y%m%d"))))
    #url = ('https://covid19.min-saude.pt/wp-content/uploads/%d/%d/%d_DGS_boletim_%d.pdf' % (year, month, diad, int(today.strftime("%Y%m%d"))))
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0'}
    r = requests.get(url, stream=True, headers=headers)

    if r.status_code == 200:
        image = r.raw

        if diaS == "Monday":

            with open('./Monday.pdf', 'wb') as _file:
                shutil.copyfileobj(image, _file)
                fich = "Monday.pdf"
        else:
            with open('./teste.pdf', 'wb') as _file:
                shutil.copyfileobj(image, _file)
                fich = "teste.pdf"
            #print('teste.pdf' + ' guardado com sucesso')
    else:
        print('erro ao fazer request')

    f = open(fich, mode="rb")

    # print(f)
    reader = PyPDF2.PdfFileReader(f)
    file_contents = reader.getPage(0).extractText().split('\n')

    # print(file_contents)
    vartotal = 0
    for i in range(len(file_contents)):
        if file_contents[i] == 'CONFIRMADOS':

            print("Novos casos confirmados " + bcolors.UNDERLINE + "%s" %
                  file_contents[i+3] + bcolors.ENDC)
            vartotal = file_contents[i+3]
            break

        if file_contents[i] == 'Dados ':

            print("Confirmados na zona centro " + bcolors.UNDERLINE +
                  "%s\n\n" % file_contents[i+14].split(' ')[-1] + bcolors.ENDC)

    inp2 = 'y'  # input("Mostrar mais (y)")
    if inp2 == 'y':

        # print(concelhos)
        # LE O FICHEIRO MONDAY
        m = open('Monday.pdf', mode="rb")
        reader2 = PyPDF2.PdfFileReader(m)
        concelhos = reader2.getPage(2).extractText().split('\n')
        #print("Entrei em Monday")

        listaViseu = ["Armamar", "Carregal do Sal", "Castro Daire", "Cinfães", "Lamego", "Mangualde", "Moimenta da Beira", "Mortágua", "Nelas", "Oliveira de Frades", "Penalva do Castelo", "Penedono",
                      "Resende", "Santa Comba Dão", "Santa Comba Dão", "São João da Pesqueira", "São Pedro do Sul", "Sátão", "Sernancelhe", "Tabuaço", "Tarouca", "Tondela", "Vila Nova de Paiva", "Viseu", "Vouzela"]
        totalconcelho = 0
        print(*concelhos[-11:-1:])

        arrayconc = []
        for i in range(len(concelhos)):

            if concelhos[i] in listaViseu:

                totalconcelho += int(concelhos[i+1])

                arrayconc.append(
                    {
                        "nome": str(concelhos[i]),
                        "casos": str(concelhos[i+1])
                    }
                )
                print("Casos confirmados em %s " %
                      concelhos[i] + bcolors.UNDERLINE + "%s" % concelhos[i+1] + bcolors.ENDC)

        print("\n\n\nCasos confirmados no distrito de VISEU " +
              bcolors.FAIL + "%d" % totalconcelho + bcolors.ENDC)

        return {
			"data": today,
            "total": str(vartotal),
            "total_viseu": str(totalconcelho),
            "concelhos": arrayconc
        }

    # inp=input("FIM")


app = Flask(__name__)


@app.route('/')
def teste():
    return casos()