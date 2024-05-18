import requests
from bs4 import BeautifulSoup

# Funktio, joka hakee ja parsii markdown-tiedoston GitHubista
def fetch_and_parse_github_markdown(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    # Hakee markdown-tekstin pre-tagin sisältä
    pre_tag = soup.find('pre')
    if pre_tag:
        return pre_tag.text
    else:
        return soup.get_text()

# URL-osoitteet
tulevat_ottelut_url = 'https://raw.githubusercontent.com/Linux88888/Veikkausliiga2024/main/Tulevatottelut.md'
yleiso_url = 'https://raw.githubusercontent.com/Linux88888/Veikkausliiga2024/main/Yleis%C3%B62024.md'

# Hakee ja parsii datan
tulevat_ottelut_data = fetch_and_parse_github_markdown(tulevat_ottelut_url)
yleiso_data = fetch_and_parse_github_markdown(yleiso_url)

# Funktio, joka parsii tulevat ottelut datan
def parse_tulevat_ottelut(data):
    ottelut = []
    lines = data.splitlines()
    for line in lines:
        if '-' in line:
            parts = line.split(' - ')
            if len(parts) > 4:
                ottelu = {
                    'id': parts[0].strip(),
                    'paiva': parts[1].strip(),
                    'aika': parts[2].strip(),
                    'koti': parts[3].strip(),
                    'vieras': parts[4].strip(),
                }
                ottelut.append(ottelu)
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
ottelut = parse_tulevat_ottelut(tulevat_ottelut_data)
teams_data = parse_yleiso_data(yleiso_data)

# Analysoi ottelut ja laske todennäköisyys yli 2.5 maalia
def analyze_matches(ottelut, teams_data):
    results = []
    for ottelu in ottelut:
        koti = ottelu['koti']
        vieras = ottelu['vieras']
        if koti in teams_data and vieras in teams_data:
            koti_maaleja = teams_data[koti].get('koti_maaleja', 0)
            vieras_maaleja = teams_data[vieras].get('vieras_maaleja', 0)
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
    return results

# Tulostaa analysoidut tulokset markdown-tiedostoon
def save_results_to_markdown(results, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write("# Analysoidut Ottelut\n\n")
        if not results:
            file.write("Ei analysoitavia otteluita.\n")
        for tulos in results:
            file.write(f"## Ottelu: {tulos['ottelu']}\n")
            file.write(f"- Koti joukkueen keskiarvo maalit: {tulos['koti_maaleja']}\n")
            file.write(f"- Vieras joukkueen keskiarvo maalit: {tulos['vieras_maaleja']}\n")
            file.write(f"- Kokonaismaalit: {tulos['total_goals']}\n")
            file.write(f"- Yli 2.5 maalia: {'Kyllä' if tulos['yli_2_5'] else 'Ei'}\n")
            file.write("\n")

# Analysoi ottelut ja tallenna tulokset
analysoidut_tulokset = analyze_matches(ottelut, teams_data)
save_results_to_markdown(analysoidut_tulokset, 'AnalysoidutOttelut.md')

print("Analyysi valmis ja tulokset tallennettu tiedostoon 'AnalysoidutOttelut.md'.")

