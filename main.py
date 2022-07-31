import sys

from bs4 import BeautifulSoup
import requests
from rich.panel import Panel
from rich.console import Console

console = Console()
url = "https://www.citilink.ru/catalog/videokarty/"
page = requests.get(url)
soup = BeautifulSoup(page.text, "html.parser")


def get_name(obj: any):
	return obj.find('a', class_='ProductCardHorizontal__title').text


def get_properties(obj: any):
	properties = obj.find('ul', class_='ProductCardHorizontal__properties')
	items = properties.findAll('li', class_='ProductCardHorizontal__properties_item')
	pairs = ""
	for item in items:
		pairs += f"{item.find('span', class_='ProductCardHorizontal__properties_name').text.strip()}: {item.find('span', class_='ProductCardHorizontal__properties_value').text.strip()}\n"
	return pairs


def get_price(obj: any):
	price = (
		obj
		.find('div', class_='ProductCardHorizontal__buy-block')
		.find('div', class_='ProductCardHorizontal__price-block')
		.find('div', class_='ProductPrice ProductPrice_default ProductPrice_size_m ProductCardHorizontal__price')
		.find('span', class_='ProductPrice__price')
	).text.strip()
	return price[:-1].strip()


def get_link(obj: any):
	return "https://citilink.ru" + obj.find('a', class_='ProductCardHorizontal__title')['href']


def main(mode: int):
	gpus = soup.findAll('div', class_='product_data__gtm-js')
	for gpu in gpus:
		if mode == 2:
			print(f"{get_name(gpu)}\n{get_properties(gpu)}\n{get_price(gpu)}\n{get_link(gpu)} \n")
		else:
			console.print(Panel(f"[yellow bold]{get_name(gpu)}[/] \n{get_properties(gpu)}\n[green]{get_price(gpu)} Руб.[/]\n {get_link(gpu)}"), justify='center')


def launch():
	console.print('Выбери режим работы:\n1.[green]Console[/] - будет выводить всё в консоль\n2.File - будет выводить всё в [yellow]output.txt[/]')
	mode = int(console.input('Режим:'))
	if mode == 1:
		main(mode=1)
	if mode == 2:
		sys.stdout = open('output.txt', 'w', encoding='utf-8')
		main(mode=mode)
		sys.stdout.close()


launch()
