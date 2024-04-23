import requests
from bs4 import BeautifulSoup

def hae_veikattu_lista():
    return ["Hjk", "Kups", "Inter", "Sjk", "FC Lahti", "Ilves", "FC Haka", "Vps", "AC Oulu", "Gnistan", "Ifk Mariehamn", "Eif"]

def hae_sarjataulukko():
    sarjataulukko_url = 'https://www.veikkausliiga.com/tilastot/2024/veikkausliiga/joukkueet/'
    response = requests.get(sarjataulukko_url)
    
    if not response.ok:
        print("Sarjataulukon lataus epäonnistui")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    taulukko_rivit = soup.find_all('tr')
    
    with open('Tilastot.md', 'w') as file:
        file.write("# Sarjataulukko\n")
        file.write("| Sijoitus | Joukkue | Ottelut | Voitot | Tasapelit | Tappiot | Tehdyt maalit | Päästetyt maalit | Maaliero | Pisteet |\n")
        file.write("|----------|---------|---------|--------|-----------|---------|----------------|-------------------|----------|---------|\n")
        for rivi in taulukko_rivit[1:]:
            solut = rivi.find_all('td')
            if solut:
                joukkue = solut[1].get_text().strip()
                sijoitus = solut[0].get_text().strip().rstrip('.')
                if joukkue == "FC Haka":
                    file.write(f"| <font color='green'>{sijoitus}.</font> | <font color='green'>{joukkue}</font> |")
                else:
                    file.write(f"| {sijoitus}. | {joukkue} |")
                for i in range(2, len(solut)):
                    file.write(f" {solut[i].get_text().strip()} |")
                file.write("\n")

def hae_pelaajan_pisteet():
    url = 'https://www.veikkausliiga.com/tilastot/2024/veikkausliiga/pelaajat/'
    response = requests.get(url)
    if not response.ok:
        print("Sivun lataus epäonnistui")
        return 0

    soup = BeautifulSoup(response.text, 'html.parser')
    taulukko_rivit = soup.find_all('tr')

    etsittavat_pelaajat = ["Coffey, Ashley Mark", "Moreno Ciorciari, Jaime Jose", "Karjalainen, Rasmus", "Plange, Luke Elliot", "Odutayo, Colin"]
    kokonaispisteet = 0

    with open('Tilastot.md', 'a') as file:
        file.write("\n# Pelaajien pisteet\n")
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
                    kokonaispisteet += pisteet
                    file.write(f'* {nimi_solu}: {pisteet:.1f} pistettä (maalit: {maalit}, laukaukset: {laukaukset}, maalisyötöt: {maalisyotot}, punaiset kortit: -{punaiset_kortit})\n')
        
        file.write(f'\n**Kokonaispisteet pelaajille: {kokonaispisteet:.1f} pistettä**\n')

def laske_joukkueiden_pisteet():
    veikatut_joukkueet = hae_veikattu_lista()
    sarjataulukko_url = 'https://www.veikkausliiga.com/tilastot/2024/veikkausliiga/joukkueet/'
    response = requests.get(sarjataulukko_url)
    kokonaispisteet = 0
    
    if not response.ok:
        print("Sarjataulukon lataus epäonnistui")
        return kokonaispisteet

    soup = BeautifulSoup(response.text, 'html.parser')
    taulukko_rivit = soup.find_all('tr')

    with open('Tilastot.md', 'a') as file:
        file.write("\n# Sarjataulukon joukkueiden pisteet\n")
        for rivi in taulukko_rivit[1:]:
            solut = rivi.find_all('td')
            if solut:
                joukkue = solut[1].get_text().strip()
                sijoitus = solut[0].get_text().strip().rstrip('.')
                if joukkue in veikatut_joukkueet and int(sijoitus) == veikatut_joukkueet.index(joukkue) + 1:
                    kokonaispisteet += 1
                    file.write(f'* {joukkue}: 1 piste\n')
        
        file.write(f'\n**Kokonaispisteet joukkueille: {kokonaispisteet}**\n')
    
    return kokonaispisteet

def main():
    hae_pelaajan_pisteet()
    pisteet_pelaajille = laske_joukkueiden_pisteet()
    hae_sarjataulukko()

    with open('Tilastot.md', 'a') as file:
        file.write(f'\n**Yhteispisteet: {pisteet_pelaajille}**\n')

if __name__ == "__main__":
    main()
