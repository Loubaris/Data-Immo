################################################################################
################################################################################
####																	   #####
####  Copyright (C) 2023 - 2024, Loubaris								   #####
####																	   #####
####  This program is free software; you can redistribute it and/or modify #####
####  it under the terms of the GNU General Public License as published by #####
####  the Free Software Foundation; either version 2 of the License, or	   #####
####  (at your option) any later version.								   #####
####																	   #####
####  This program is distributed in the hope that it will be useful,	   #####
####  but WITHOUT ANY WARRANTY; without even the implied warranty of	   #####
####  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the		   #####
####  GNU General Public License for more details.						   #####
####																	   #####
####  You must obey the GNU General Public License. If you will modify	   #####
####  this file(s), you may extend this exception to your version		   #####
####  of the file(s), but you are not obligated to do so.  If you do not   #####
####  wish to do so, delete this exception statement from your version.    #####
####  If you delete this exception statement from all source files in the  #####
####  program, then also delete it here.								   #####
####																	   #####
####  Contact:															   #####
#### 																	   #####
####		  Mail: adamou.loubaris@gmail.com							   #####
####																	   #####
################################################################################
################################################################################

print("(SERVER) - Lancement du scraper")

import os
import sys
import time

# IMPORTATIONS DES LIBRAIRIES
try:
	from avito_scraping import scrape_avito
except Exception as e:
	print(f"(SERVER) - Error while importing 'avito scraping file' \nError {e}")

try:
	from avito_annuaire import scrape_annuaire_avito
except Exception as e:
	print(f"(SERVER) - Error while importing 'avito annuaire file' \nError {e}")

try:
	from mubawab_scraping import scrape_mubawab
except Exception as e:
	print(f"(SERVER) - Error while importing 'avito scraping file' \nError {e}")

try:
	import requests
except Exception as e:
	print(f"(SERVER) - Error while importing 'requests' library \nError {e}")
try:
	from bs4 import BeautifulSoup
except Exception as e:
	print(f"(SERVER) - Error while importing 'beautifulsoup' library \nError {e}")
try:
	import html5lib
except Exception as e:
	print(f"(SERVER) - Error while importing 'html5lib' library \nError {e}")
try:
	from datetime import date
except Exception as e:
	print(f"(SERVER) - Error while importing 'datetime' library \nError {e}")

# FONCTIONS

# SITE FONCTIONNEL
def is_up(url):
    r = requests.get(url)
    return r


# TEST DE CONNECTION DES SITES

sites = ["https://www.charika.ma", "https://www.avito.ma", "https://www.mubawab.ma"]
sites_on = []
sites_off = []
for i in range(len(sites)):
	try:
		if is_up(sites[i]):
			sites_on.append(sites[i])
		else: 
			sites_off.append(sites[i])
	except: 
		sites_off.append(sites[i])

print("(SERVER) - Liste des sites fonctionnels")
for i in sites_on:
	print(i)
if sites_off != []:
	print("(SERVER)- Il y'a eu un problèmes avec ces sites:")
	for i in sites_off:
		print(i)

# Début du scraping
	
print("(SERVER) - Début de création de la nouvelle base")

def avito():
	if "https://www.avito.ma" in sites_on:
		print("(SERVER) - Extraction d'Avito")
		scrape_avito()

def annuaire_avito():
	if "https://www.avito.ma" in sites_on:
		print("(SERVER) - Extraction de l'annuaire d'Avito")
		scrape_annuaire_avito()


def mubawab():
	if "https://www.mubawab.ma" in sites_on:
		print("(SERVER) - Extraction de Mubawab")
		scrape_mubawab()

# SCRAPING charika à faire

# Lancement du scraping
avito()
annuaire_avito()
mubawab()



