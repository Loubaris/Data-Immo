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

import requests
from bs4 import BeautifulSoup
from datetime import date
today = date.today()

def scrape_mubawab():
	appart_url = 'https://www.mubawab.ma/fr/cc/immobilier-a-louer-all:o:i:sc:apartment-rent:p:'
	villa_url = 'https://www.mubawab.ma/fr/cc/immobilier-a-louer-all:o:i:sc:villa-rent:p:'
	commercial_url = 'https://www.mubawab.ma/fr/cc/immobilier-a-louer-all:o:i:sc:commercial-rent:p:'
	bureaux_url = 'https://www.mubawab.ma/fr/cc/bureaux-et-commerces-a-louer:p:'
	maison_url = 'https://www.mubawab.ma/fr/cc/immobilier-a-louer-all:o:i:sc:houses-for-rent:p:'

	sites_location = [appart_url, villa_url, maison_url, commercial_url, bureaux_url]

	appart_s_url = 'https://www.mubawab.ma/fr/cc/immobilier-a-vendre-all:o:i:sc:apartment-sale:p:'
	villa_s_url = 'https://www.mubawab.ma/fr/cc/immobilier-a-vendre-all:o:i:sc:villa-sale:p:'
	commercial_s_url = 'https://www.mubawab.ma/fr/cc/immobilier-a-vendre-all:o:i:sc:commercial-sale:p:'
	bureaux_s_url = 'https://www.mubawab.ma/fr/cc/bureaux-et-commerces-a-vendre:p:'
	maison_s_url = 'https://www.mubawab.ma/fr/cc/immobilier-a-vendre-all:o:i:sc:houses-for-sale:p:'

	sites_ventes = [appart_s_url, villa_s_url, maison_s_url, commercial_s_url, bureaux_s_url]

	base_simple = open(f"bases/mubawab/base_simple_mubawab_{today}.csv", "w", encoding="utf-8")
	base_pro = open(f"bases/mubawab/base_pro_mubawab_{today}.csv", "w", encoding="utf-8")
	base_entreprise = open(f"bases/mubawab/base_entreprise_mubawab_{today}.csv", "w", encoding="utf-8")

	for elem in sites_location:
		if sites_location.index(elem) == 0:
			base_simple.write(f"[LISTE-LOC] APPART\n")
			base_pro.write(f"[LISTE-LOC] APPART\n")
			base_entreprise.write(f"[LISTE-LOC] APPART\n")
		elif sites_location.index(elem) == 1:
			base_simple.write(f"[LISTE-LOC] VILLA\n")
			base_pro.write(f"[LISTE-LOC] VILLA\n")
			base_entreprise.write(f"[LISTE-LOC] VILLA\n")
		elif sites_location.index(elem) == 2:
			base_simple.write(f"[LISTE-LOC] MAISON\n")
			base_pro.write(f"[LISTE-LOC] MAISON\n")
			base_entreprise.write(f"[LISTE-LOC] MAISON\n")
		elif sites_location.index(elem) == 3:
			base_simple.write(f"[LISTE-LOC] COMMERCIAL\n")
			base_pro.write(f"[LISTE-LOC] COMMERCIAL\n")
			base_entreprise.write(f"[LISTE-LOC] COMMERCIAL\n")
		elif sites_location.index(elem) == 4:
			base_simple.write(f"[LISTE-LOC] BUREAU\n")
			base_pro.write(f"[LISTE-LOC] BUREAU\n")
			base_entreprise.write(f"[LISTE-LOC] BUREAU\n")
		for nb_page in range(11):
			print(f"(SERVER-Mubawab) - Processing page {nb_page} of section {sites_location[sites_location.index(elem)]}")
			page = requests.get(elem+str(nb_page))
			soup = BeautifulSoup(page.content, 'html.parser')
			lists  = soup.find_all('li', class_='listingBox w100')
			for list in lists:
						try:
							lien = str(list.find('h2', class_='listingTit'))
							lien = (lien.split('href="')[1]).split('">')[0]
						except Exception as e:
							lien = "Lien introuvable"
						try:
							titre = (((getattr(list.find('h2', class_='listingTit'), 'text')).replace("\xa0", "")).replace("\n", "")).replace("\t", "")
						except Exception as e:
							titre = "Titre Indéfini"
						city = list.find('h3', class_='listingH3').text.split()[-1].strip()
						area = list.find('h3', class_='listingH3').text.split("à")[0]
						try:
							estate_pieces = getattr(list.find('p', class_='listingH4 floatR'), 'text').text.split()[0].strip()
						except Exception as e: 
							try:
								estate_pieces = list.find('p', class_='listingH4 floatR').text.split()[0].strip()
							except Exception as e:
								estate_pieces = "Indéfini"
						try:
							estate_surface = str((getattr(list.find('p', class_='listingH4 floatR'),'text')))
							if "," in estate_surface:
								estate_surface = estate_surface.split(",", 1)[1]
								estate_surface = ''.join(i for i in estate_surface if i.isdigit() or i==".")
							else:
								estate_pieces = "Indéfini"
							estate_surface = (((str(estate_surface).replace("\xa0", "")).replace("\n", "")).replace("\t", "")).replace("²", "")
							estate_surface = ''.join(i for i in estate_surface if i.isdigit() or i==".")
						except Exception as e:
							try:
								estate_surface = str(getattr(list.find('h4', class_='listingH4 floatR'),'text')).split(",", 1)[1]
								estate_surface = ((((estate_surface).replace("\xa0", "")).replace("\n", "")).replace("\t", "")).replace("²", "")
								estate_surface = ''.join(i for i in estate_surface if i.isdigit() or i==".")
							except:

								estate_surface = "Indéfini"
						try:
							date_publi = ((str(getattr(list.find('span', class_='listingDetails iconPadR'), "text"))))
							if "y a" in date_publi:
								date_publi = (((date_publi.split("y a", 1)[1]).replace("\xa0", "")).replace("\n", "")).replace("\t", "")
								if "jour" in date_publi:
									date_publi = ''.join(i for i in date_publi if i.isdigit() or i==".")
								elif "semaine" in date_publi:
									date_publi = ''.join(i for i in date_publi if i.isdigit() or i==".")
									date_publi = int(date_publi)*7
									date_publi = str(date_publi)
								elif "mois" in date_publi:
									date_publi = ''.join(i for i in date_publi if i.isdigit() or i==".")
									date_publi = int(date_publi)*30
									date_publi = str(date_publi)
							else:
								date_publi = (((date_publi).replace("\xa0", "")).replace("\n", "")).replace("\t", "")
								if "aujour" in date_publi:
									date_publi = 'today'
						except Exception as e:
							date_publi = "Indéfini"
						try:
							estate_price = ((str(getattr(list.find("span", class_= "priceTag hardShadow float-right floatL yellowBg"),'text')).replace("\xa0", "")).replace("\n", "")).replace("\t", "")
							estate_price = ''.join(i for i in estate_price if i.isdigit() or i==".")
						except:
							try:
								estate_price = ((str(getattr(list.find("span", class_= "priceTag hardShadow float-right floatL"),'text')).replace("\xa0", "")).replace("\n", "")).replace("\t", "")
								estate_price = ''.join(i for i in estate_price if i.isdigit() or i==".")
							except:
								estate_price = 'Indéfini'
						info = str([str(titre), str(city), (str(area).replace("\n", "")).replace("\t", ""), str(estate_surface), str(estate_price), str(date_publi), str(lien)])
						info = ((((info.replace("[", "")).replace("]", "")).replace("'", "")).replace('"', '')).replace("  ", "    ")
		
						if nb_page < 2:
							base_simple.write(f"{info}\n")
						elif nb_page < 4:
							base_pro.write(f"{info}\n")
						elif nb_page < 8:
							base_entreprise.write(f"{info}\n")



if __name__ == "__main__":
	scrape_mubawab()