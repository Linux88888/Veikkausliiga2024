import requests
from bs4 import BeautifulSoup

def hae_veikattu_lista():
    return ["Hjk", "Kups", "Inter", "Sjk", "FC Lahti", "Ilves", "FC Haka", "Vps", "AC Oulu", "Gnistan", "Ifk Mariehamn", "Eif"]

def hae_sarjataulukko():
    try:
        sarjataulukko_url = 'https://www.veikkausliiga.com/tilastot/2024/veikkausliiga/joukkueet/'
        response = requests.get(sarjataulukko_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        taulukko_rivit = soup.find_all('tr')
        taulukko = []
        
        for rivi in taulukko_rivit[1:]:
            solut = rivi.find_all('td')
            if solut:
                taulukko.append([s.get_text().strip() for s in solut])
        return taulukko
    except Exception as e:
        print("Sarjataulukon lataus epäonnistui:", e)
        return None

def hae_pelaajan_pisteet():
    try:
        url = 'https://www.veikkausliiga.com/tilastot/2024/veikkausliiga/pelaajat/'
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        taulukko_rivit = soup.find_all('tr')

        etsittavat_pelaajat = ["Coffey, Ashley Mark", "Moreno Ciorciari, Jaime Jose", "Karjalainen, Rasmus", "Plange, Luke Elliot", "Odutayo, Colin"]
        pelaajat_pisteet = []

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
                    pelaajat_pisteet.append((nimi_solu, pisteet))
        return pelaajat_pisteet
    except Exception as e:
        print("Pelaajatietojen haku epäonnistui:", e)
        return []

def laske_joukkueiden_pisteet(sarjataulukko, veikatut_joukkueet):
    kokonaispisteet = 0
    for rivi in sarjataulukko:
        joukkue = rivi[1]
        sijoitus = rivi[0].rstrip('.')
        if joukkue in veikatut_joukkueet and int(sijoitus) == veikatut_joukkueet.index(joukkue) + 1:
            kokonaispisteet += 1
    return kokonaispisteet

def tallenna_tulokset(sarjataulukko, pelaajat_pisteet, joukkuepisteet):
    with open('Tilastot.md', 'w') as file:
        file.write("# Sarjataulukko\n")
        file.write("| Sijoitus | Joukkue | Ottelut | Voitot | Tasapelit | Tappiot | Tehdyt maalit | Päästetyt maalit | Maaliero | Pisteet |\n")
        file.write("|----------|---------|---------|--------|-----------|---------|----------------|-------------------|----------|---------|\n")
        for rivi in sarjataulukko:
            file.write("|" + " | ".join(rivi) + "|\n")
        file.write("\n# Pelaajien pisteet\n")
        for nimi, pisteet in pelaajat_pisteet:
            file.write(f'* {nimi}: {pisteet:.1f} pistettä\n')
        file.write(f'\n**Kokonaispisteet joukkueille: {joukkuepisteet}**\n')

def main():
    veikatut_joukkueet = hae_veikattu_lista()
    sarjataulukko = hae_sarjataulukko()
    pelaajat_pisteet = hae_pelaajan_pisteet()
    if sarjataulukko:
        joukkuepisteet = laske_joukkueiden_pisteet(sarjataulukko, veikatut_joukkueet)
        tallenna_tulokset(sarjataulukko, pelaajat_pisteet, joukkuepisteet)

if __name__ == "__main__":
    main()
