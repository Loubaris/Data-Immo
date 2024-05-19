# -*- coding: utf-8 -*-
#################################################################################
#################################################################################
####																		#####
####  Copyright (C) 2023-2024, Loubaris										#####
####																		#####
####  Contact:																##### 																	   #####
####		  Mail: adamou.loubaris@gmail.com								#####
####																		#####
#################################################################################
#################################################################################

from bs4 import BeautifulSoup
import html5lib
import requests
from datetime import date
import threading
today = date.today()

def scrape_annuaire_avito_choix(part1, name):
	nb_boutique = 0
	fin_simple = False
	base_simple = open(f"bases/annuaire/annuaire_client_{name}_{today}.csv", "w", encoding="utf-8")
	i = 0
	# APPARTEMENTS
	for o in range(1,50):
		if fin_simple == True:
			break
		else:
			if o == 1:
				add =""
			else:
				add = "o=" + str(o)
			URL1 = part1 + add
			r = requests.get(URL1)
			page = r.content
			soup1 = BeautifulSoup(page, 'html.parser')
			n = soup1.find_all('a', class_="oan6tk-1 fFOxTQ")
			liens = []
			for k in n:
				k = str(k)
				k = list(k.split('"'))
				liens.append(k[3])
			for u in liens:
				re = requests.get(u)
				soup = BeautifulSoup(re.content, 'html5lib')
				n = soup.find('script', attrs={'id': 'data-layer'})
				n = str(n)
				n = n.replace(":", ",")
				n = n.replace('"', "")
				liste = list(n.split(","))
				
				try:
					if liste[liste.index("seller_type")+1] == 'shop':
						type_vendeur = "Boutique"
					else:
						type_vendeur = "Particulier"
				except:
					type_vendeur = "Privée"
				if type_vendeur == "Particulier" or type_vendeur == "Privée":
					try:
						nom_vendeur = liste[liste.index("seller_name")+1]
						telephone = liste[liste.index("ad_phone_number")+1]
						if fin_simple == False:	
							base_simple.write(f'{telephone},{nom_vendeur},{u}\n')
	
						print(f"(SERVER) - Processing {i}")
						i += 1
					except:
						pass
						i -= 1
					if i == 200:
						fin_simple = True
						base_simple.close()


	
def scrape_annuaire_avito():
	avito_scrape_appart =threading.Thread(target=scrape_annuaire_avito_choix, args=('https://www.avito.ma/fr/maroc/appartements-%C3%A0_vendre?', 'appart'))
	avito_scrape_appart.start()
	avito_scrape_maison =threading.Thread(target=scrape_annuaire_avito_choix, args=('https://www.avito.ma/fr/maroc/maisons_et_villas-%C3%A0_vendre?', 'maison'))
	avito_scrape_maison.start()
	avito_scrape_bureau =threading.Thread(target=scrape_annuaire_avito_choix, args=('https://www.avito.ma/fr/maroc/bureaux_et_plateaux-%C3%A0_vendre?', 'bureau'))
	avito_scrape_bureau.start()
	avito_scrape_commerce =threading.Thread(target=scrape_annuaire_avito_choix, args=('https://www.avito.ma/fr/maroc/magasins_et_commerces-%C3%A0_vendre?', 'commerce'))
	avito_scrape_commerce.start()
	avito_scrape_terrains =threading.Thread(target=scrape_annuaire_avito_choix, args=('https://www.avito.ma/fr/maroc/terrains_et_fermes-%C3%A0_vendre?', 'terrain'))
	avito_scrape_terrains.start()

if __name__ == "__main__":
	scrape_annuaire_avito()