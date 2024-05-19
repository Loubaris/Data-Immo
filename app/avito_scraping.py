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
today = date.today()
import threading

def scrape_avito_choix(part1, name):
	nb_boutique = 0
	fin_simple = False
	fin_pro = False
	fin_entreprise = False
	base_simple = open(f"bases/avito/{name}/base_simple_avito_{name}_{today}.csv", "w", encoding="utf-8")
	base_pro = open(f"bases/avito/{name}/base_pro_avito_{name}_{today}.csv", "w", encoding="utf-8")
	base_entreprise = open(f"bases/avito/{name}/base_entreprise_avito_{name}_{today}.csv", "w", encoding="utf-8")
	i = 0
	for o in range(1,50):
		if fin_entreprise == True:
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
						nb_boutique+=1
					else:
						type_vendeur = "Particulier"
				except:
					type_vendeur = "Privée"
				if nb_boutique <= 10 or type_vendeur == "Particulier" or type_vendeur == "Privée":
					
					try:
						nom_vendeur = liste[liste.index("seller_name")+1]
						nom_annonce = liste[liste.index("ad_name")+1]
						prix_annonce = liste[liste.index("ad_price")+1]
						nb_photo = liste[liste.index("picture_count")+1]
						telephone = liste[liste.index("ad_phone_number")+1]
						city = liste[liste.index("city")+1]
						area = liste[liste.index("area")+1]
						if fin_simple == False:	
							base_simple.write(f'{type_vendeur},{nom_vendeur},{nom_annonce},{prix_annonce},{telephone},{city},{area},{u}\n')
						if fin_pro == False:
							base_pro.write(f'{type_vendeur},{nom_vendeur},{nom_annonce},{prix_annonce},{telephone},{city},{area},{u}\n')
						if fin_entreprise == False:
							base_entreprise.write(f'{type_vendeur},{nom_vendeur},{nom_annonce},{prix_annonce},{telephone},{city},{area},{u}\n')
						print(f"(Taddart) - Processing {i}")
						i += 1
					except:
						pass
						i -= 1
					if i == 21:
						fin_simple = True
						base_simple.close()

					elif i == 51:
						fin_pro = True
						base_pro.close()
					elif i == 101:
				   		fin_entreprise = True
				   		base_entreprise.close()
				elif nb_boutique > 10:
					nb_boutique = 11



	base_simple.close()
	base_pro.close()
	base_entreprise.close()

def scrape_avito():
	avito_scrape_appart =threading.Thread(target=scrape_avito_choix, args=('https://www.avito.ma/fr/maroc/appartements-%C3%A0_vendre?', 'appart'))
	avito_scrape_appart.start()
	avito_scrape_maison =threading.Thread(target=scrape_avito_choix, args=('https://www.avito.ma/fr/maroc/maisons_et_villas-%C3%A0_vendre?', 'maison'))
	avito_scrape_maison.start()
	avito_scrape_bureau =threading.Thread(target=scrape_avito_choix, args=('https://www.avito.ma/fr/maroc/bureaux_et_plateaux-%C3%A0_vendre?', 'bureau'))
	avito_scrape_bureau.start()
	avito_scrape_commerce =threading.Thread(target=scrape_avito_choix, args=('https://www.avito.ma/fr/maroc/magasins_et_commerces-%C3%A0_vendre?', 'commerce'))
	avito_scrape_commerce.start()
	avito_scrape_terrains =threading.Thread(target=scrape_avito_choix, args=('https://www.avito.ma/fr/maroc/terrains_et_fermes-%C3%A0_vendre?', 'terrain'))
	avito_scrape_terrains.start()

if __name__ == "__main__":
	scrape_avito()