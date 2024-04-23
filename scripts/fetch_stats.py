import requests
from bs4 import BeautifulSoup

def hae_veikattu_lista():
    return ["Hjk", "Kups", "Inter", "Sjk", "FC Lahti", "Ilves", "FC Haka", "Vps", "AC Oulu", "Gnistan", "Ifk Mariehamn", "Eif"]

def hae_sarjataulukko(file):
    sarjataulukko_url = 'https://www.veikkausliiga.com/tilastot/2024/veikkausliiga/joukkueet/'
    response = requests.get(sarjataulukko_url)
    
    if not response.ok:
        print("Sarjataulukon lataus epäonnistui")
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')
    taulukko_rivit = soup.find_all('tr')
    
    file.write("\nSarjataulukko:\n")
    for rivi in taulukko_rivit[1:]:
        solut = rivi.find_all('td')
        if solut:
            sijoitus = solut[0].get_text().strip()
            joukkue = solut[1].get_text().strip()
            ottelut = solut[2].get_text().strip()
            voitot = solut[3].get_text().strip()
            tasapelit = solut[4].get_text().strip()
            tappiot = solut[5].get_text().strip()
            tehty = solut[6].get_text().strip()
            paastetty = solut[7].get_text().strip()
            erotus = solut[8].get_text().strip()
            pisteet = solut[9].get_text().strip()
            if joukkue == "FC Haka":
                file.write('<tr style="background-color: lightgreen;">')
            else:
                file.write('<tr>')
            file.write(f"<td>{sijoitus}</td><td>{joukkue} ({ottelut} ottelua) - Voitot: {voitot}, Tasapelit: {tasapelit}, Tappiot: {tappiot}, Tehdyt maalit: {tehty}, Päästetyt maalit: {paastetty}, Maaliero: {erotus}, Pisteet: {pisteet}</td></tr>\n")

def hae_pelaajan_pisteet(file):
    url = 'https://www.veikkausliiga.com/tilastot/2024/veikkausliiga/pelaajat/'
    response = requests.get(url)
    if not response.ok:
        print("Sivun lataus epäonnistui")
        return 0

    soup = BeautifulSoup(response.text, 'html.parser')
    taulukko_rivit = soup.find_all('tr')

    etsittavat_pelaajat = ["Coffey, Ashley Mark", "Moreno Ciorciari, Jaime Jose", "Karjalainen, Rasmus", "Plange, Luke Elliot", "Odutayo, Colin"]
    kokonaispisteet = 0

    file.write("\nPelaajien pisteet:\n")
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
                file.write(f'{nimi_solu}: {pisteet:.1f} pistettä (maalit: {maalit}, laukaukset: {laukaukset}, maalisyötöt: {maalisyotot}, punaiset kortit: -{punaiset_kortit})\n')
    
    file.write(f'\nKokonaispisteet pelaajille: {kokonaispisteet:.1f}\n')
    return kokonaispisteet

def laske_joukkueiden_pisteet(file):
    veikatut_joukkueet = hae_veikattu_lista()
    sarjataulukko_url = 'https://www.veikkausliiga.com/tilastot/2024/veikkausliiga/joukkueet/'
    response = requests.get(sarjataulukko_url)
    kokonaispisteet = 0
    
    if not response.ok:
        print("Sarjataulukon lataus epäonnistui")
        return kokonaispisteet

    soup = BeautifulSoup(response.text, 'html.parser')
    taulukko_rivit = soup.find_all('tr')

    file.write("\nSarjataulukon joukkueiden pisteet:\n")
    for rivi in taulukko_rivit[1:]:
        solut = rivi.find_all('td')
        if solut:
            joukkue = solut[1].get_text().strip()
            sijoitus = solut[0].get_text().strip().rstrip('.')  # Poista piste
            if joukkue in veikatut_joukkueet and int(sijoitus) == veikatut_joukkueet.index(joukkue) + 1:
                kokonaispisteet += 1
                file.write(f'{joukkue}: 1 piste\n')
    
    file.write(f'\nKokonaispisteet joukkueille: {kokonaispisteet}\n')
    return kokonaispisteet

def main():
    with open('Tilastot.txt', 'w') as file:
        file.write("<!DOCTYPE html>\n<html>\n<head>\n<title>Veikkausliiga Tilastot</title>\n<style>table, th, td {border: 1px solid black; border-collapse: collapse; padding: 8px;} th {background-color: lightgray;}</style>\n</head>\n<body>\n")
        hae_sarjataulukko(file)
        pelaajien_pisteet = hae_pelaajan_pisteet(file)
        joukkueiden_pisteet = laske_joukkueiden_pisteet(file)
        kokonaispisteet = pelaajien_pisteet + joukkueiden_pisteet
        file.write(f'\n<p>Kokonaispisteet: {kokonaispisteet}</p>\n')
        file.write("</body>\n</html>")

if __name__ == "__main__":
    main()
