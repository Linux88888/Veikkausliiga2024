import requests
from bs4 import BeautifulSoup

# Funktio, joka hakee ja parsii markdown-tiedoston GitHubista
def fetch_and_parse_github_markdown(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    pre_tag = soup.find('pre')
    if pre_tag:
        return pre_tag.text
    else:
        return soup.get_text()

# URL-osoitteet
tulevat_ottelut_url = 'https://raw.githubusercontent.com/Linux88888/Veikkausliiga2024/main/Tulevatottelut.md'
yleiso_url = 'https://raw.githubusercontent.com/Linux88888/Veikkausliiga2024/main/Yleis%C3%B62024.md'

# Joukkueiden lista
teams = ["HJK", "KuPS", "FC Inter", "SJK", "FC Lahti", "Ilves", "FC Haka", "VPS", "AC Oulu", "Gnistan", "IFK Mariehamn", "EIF"]

# Hakee ja parsii datan
tulevat_ottelut_data = fetch_and_parse_github_markdown(tulevat_ottelut_url)
yleiso_data = fetch_and_parse_github_markdown(yleiso_url)

# Tulostetaan haettu data debuggausta varten
print("Tulevat ottelut data:\n", tulevat_ottelut_data[:500], "\n")
print("Yleisö data:\n", yleiso_data[:500], "\n")

# Funktio, joka parsii tulevat ottelut datan
def parse_tulevat_ottelut(data, teams):
    ottelut = []
    lines = data.splitlines()
    for line in lines:
        if ' - ' in line and 'Seuranta' not in line:
            parts = line.split(' - ')
            if len(parts) >= 5:
                koti = parts[3].strip()
                vieras = parts[4].strip()
                if koti in teams and vieras in teams:
                    ottelu = {
                        'id': parts[0].strip(),
                        'paiva': parts[1].strip() if len(parts) > 5 else '',
                        'aika': parts[2].strip() if len(parts) > 4 else '',
                        'koti': koti,
                        'vieras': vieras,
                    }
                    print(f"Lisätty ottelu: {ottelu}")  # Debug-tuloste
                    ottelut.append(ottelu)
                else:
                    print(f"Ei kelvollinen joukkue: {koti} vs {vieras}")  # Debug-tuloste
    return ottelut

# Funktio, joka parsii yleisödata
def parse_yleiso_data(data):
    teams_data = {}
    current_team = None
    lines = data.splitlines()
    for line in lines:
        if line.strip() and not line.startswith(' '):
            current_team = line.strip()
            teams_data[current_team] = {}
        elif current_team and 'Kotiotteluiden keskiarvo (maalit tehty):' in line:
            avg_goals = float(line.split(': ')[1])
            teams_data[current_team]['koti_maaleja'] = avg_goals
        elif current_team and 'Vierasotteluiden keskiarvo (maalit tehty):' in line:
            avg_goals = float(line.split(': ')[1])
            teams_data[current_team]['vieras_maaleja'] = avg_goals
    return teams_data

# Parsii datat
ottelut = parse_tulevat_ottelut(tulevat_ottelut_data, teams)
teams_data = parse_yleiso_data(yleiso_data)

# Tulostetaan parsiottu data debuggausta varten
print("Parsitut ottelut:\n", ottelut, "\n")
print("Parsittu yleisödata:\n", teams_data, "\n")

# Yksinkertainen analysointifunktio
def simple_analyze_matches(ottelut, teams_data):
    results = []
    for ottelu in ottelut:
        koti = ottelu['koti']
        vieras = ottelu['vieras']
        koti_maaleja = teams_data.get(koti, {}).get('koti_maaleja', 0)
        vieras_maaleja = teams_data.get(vieras, {}).get('vieras_maaleja', 0)
        total_goals = koti_maaleja + vieras_maaleja
        yli_2_5 = total_goals > 2.5
        result = {
            'ottelu': f"{koti} vs {vieras}",
            'koti_maaleja': koti_maaleja,
            'vieras_maaleja': vieras_maaleja,
            'total_goals': total_goals,
            'yli_2_5': yli_2_5
        }
        results.append(result)
        print(f"Analysoitu ottelu: {result}")  # Debug-tuloste
    return results

# Tulostaa analysoidut tulokset markdown-tiedostoon
def save_results_to_markdown(ottelut, results, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write("# Analysoidut Ottelut\n\n")
        
        # Tulostetaan ottelut
        file.write("## Tulevat Ottelut\n")
        for ottelu in ottelut:
            file.write(f"- {ottelu['koti']} vs {ottelu['vieras']} ({ottelu['paiva']} klo {ottelu['aika']})\n")
        
        file.write("\n## Ennusteet\n")
        if not results:
            file.write("Ei analysoitavia otteluita.\n")
        for tulos in results:
            file.write(f"### Ottelu: {tulos['ottelu']}\n")
            file.write(f"- Koti joukkueen keskiarvo maalit: {tulos['koti_maaleja']}\n")
            file.write(f"- Vieras joukkueen keskiarvo maalit: {tulos['vieras_maaleja']}\n")
            file.write(f"- Kokonaismaalit: {tulos['total_goals']}\n")
            file.write(f"- Yli 2.5 maalia: {'Kyllä' if tulos['yli_2_5'] else 'Ei'}\n")
            file.write("\n")
    print(f"Tulokset tallennettu tiedostoon {filename}")

# Analysoi ottelut ja tallenna tulokset
analysoidut_tulokset = simple_analyze_matches(ottelut, teams_data)
save_results_to_markdown(ottelut, analysoidut_tulokset, 'AnalysoidutOttelut.md')

print("Analyysi valmis ja tulokset tallennettu tiedostoon 'AnalysoidutOttelut.md'.")
