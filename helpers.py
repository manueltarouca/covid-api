from urllib.request import urlopen
from lxml import etree
import requests
import shutil

import io
import pdfminer.high_level

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
		"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0"
	}

	r = requests.get(url, stream=True, headers=headers)
	if r.status_code == 200:
		lst_text = pdfminer.high_level.extract_text(
			io.BytesIO(r.content), codec="utf-8").split("\n")
		lst_text = list(filter(str.strip, lst_text))
		return lst_text
	else:
		print("erro ao fazer request")
		return


def main():
	di = get_urls()
	#arr_valid = valid_urls(di.get("titles")[0], di.get("urls"))
	# for i in arr_valid:
	# 	get_data(i)
	latest = get_data(di.get("urls")[0])
	latest = latest[latest.index("CONFIRMADOS")-1].split("+")[-1].strip()
	print("Casos hoje: %s" % (latest))


if __name__ == "__main__":
	main()
