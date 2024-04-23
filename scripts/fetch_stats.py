import requests
from bs4 import BeautifulSoup

url = 'https://www.veikkausliiga.com/tilastot/2024/veikkausliiga/pelaajat/'

def hae_pelaajan_pisteet():
    response = requests.get(url)
    if not response.ok:
        print("Sivun lataus epäonnistui")
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')
    taulukko_rivit = soup.find_all('tr')
    
    etsittavat_pelaajat = ["Coffey, Ashley Mark", "Moreno Ciorciari, Jaime Jose", "Karjalainen, Rasmus", "Plange, Luke Elliot", "Odutayo, Colin"]
    kokonaispisteet = 0  # Alustetaan kokonaispisteiden laskuri

    with open('results.txt', 'w') as file:
        for rivi in taulukko_rivit:
            solut = rivi.find_all('td')
            if solut and len(solut) > 15:
                nimi_solu = solut[1].get_text().strip()
                if any(nimi == nimi_solu for nimi in etsittavat_pelaajat):
                    maalit = int(solut[5].get_text().strip())
                    laukaukset = int(solut[6].get_text().strip())
                    maalisyotot = int(float(solut[9].get_text().strip().replace(',', '.')))
                    punaiset_kortit = int(solut[15].get_text().strip())
                    pisteet = (maalit * 2) + (laukaukset * 0.1) + (maalisyotot * 0.5) - (punaiset_kortit * 1)
                    kokonaispisteet += pisteet  # Lisätään pelaajan pisteet kokonaispisteisiin
                    file.write(f'{nimi_solu}: {pisteet:.1f} pistettä (maalit: {maalit}, laukaukset: {laukaukset}, maalisyötöt: {maalisyotot}, punaiset kortit: -{punaiset_kortit})\n')
        
        # Kirjoitetaan kokonaispisteet tiedoston loppuun
        file.write(f'\nKokonaispisteet: {kokonaispisteet:.1f}')

hae_pelaajan_pisteet()

