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
    
    for rivi in taulukko_rivit:
        solut = rivi.find_all('td')
        if solut and len(solut) > 15:  # Varmistetaan, että rivillä on tarpeeksi soluja
            nimi_solu = solut[1].get_text().strip()  # Nimi on toisessa solussa
            if any(nimi == nimi_solu for nimi in etsittavat_pelaajat):
                maalit = int(solut[5].get_text().strip())  # Maalit ovat kuudennessa solussa
                laukaukset = int(solut[6].get_text().strip())  # Laukaukset seitsemännessä solussa
                maalisyotot = int(float(solut[9].get_text().strip().replace(',', '.')))  # Maalisyötöt yhdeksännessä solussa, muunna desimaaliluvuksi jos tarpeen
                punaiset_kortit = int(solut[15].get_text().strip())  # Punaiset kortit kuudennentoista solussa
                
                # Lasketaan pisteet: 2 pistettä per maali, 0.1 pistettä per laukaus, 0.5 pistettä per maalisyöttö, -1 piste per punainen kortti
                pisteet = (maalit * 2) + (laukaukset * 0.1) + (maalisyotot * 0.5) - (punaiset_kortit * 1)
                print(f'{nimi_solu}: {pisteet:.1f} pistettä (maalit: {maalit}, laukaukset: {laukaukset}, maalisyötöt: {maalisyotot}, punaiset kortit: -{punaiset_kortit})')

hae_pelaajan_pisteet()
