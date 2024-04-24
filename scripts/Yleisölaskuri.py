import re
import requests
from bs4 import BeautifulSoup

url = "https://www.veikkausliiga.com/tilastot/2024/veikkausliiga/ottelut/"
teams = ["HJK", "KuPS", "FC Inter", "SJK", "FC Lahti", "Ilves", "FC Haka", "VPS", "AC Oulu", "Gnistan", "IFK Mariehamn", "EIF"]

team_data = {team: {'Home': {'audiences': [], 'goals': []}, 'Away': {'audiences': [], 'goals': []}} for team in teams}

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
table_rows = soup.find_all('tr')

for row in table_rows:
    cells = row.find_all('td')
    if cells and len(cells) > 6:
        date = cells[1].get_text(strip=True)
        time = cells[2].get_text(strip=True)
        match_teams = cells[3].get_text(strip=True)
        result_text = cells[5].get_text(strip=True)  # Tuloksen sarake oikein, indeksi 5
        audience_text = cells[6].get_text(strip=True)  # Yleisömäärän sarake oikein, indeksi 6

        hour, minute = map(int, time.split(':')) if ':' in time else (0, 0)
        result_match = re.search(r'(\d+) — (\d+)', result_text)
        audience_number = int(re.search(r'(\d+)', audience_text).group(1)) if re.search(r'(\d+)', audience_text) else 0

        if result_match:
            home_goals, away_goals = map(int, result_match.groups())
            home_team, away_team = [team.strip() for team in match_teams.split(' - ')]

            if home_team in teams:
                team_data[home_team]['Home']['audiences'].append(audience_number)
                team_data[home_team]['Home']['goals'].append(home_goals)
            if away_team in teams:
                team_data[away_team]['Away']['audiences'].append(audience_number)
                team_data[away_team]['Away']['goals'].append(away_goals)

# Kirjoitetaan tulokset Markdown-tiedostoon
with open('Yleisö2024.md', 'w') as file:
    file.write("# Veikkausliiga 2024 Yleisömäärät ja Maalit\n\n")
    for team, data in team_data.items():
        home_audiences = data['Home']['audiences']
        home_goals = data['Home']['goals']
        away_audiences = data['Away']['audiences']
        away_goals = data['Away']['goals']

        all_audiences = home_audiences + away_audiences
        all_goals = home_goals + away_goals

        if all_audiences:
            total_average_audience = sum(all_audiences) / len(all_audiences)
            total_average_goals = sum(all_goals) / len(all_goals)
            file.write(f"## {team}\n")
            file.write(f"- Kokonaiskeskiarvo kaikista peleistä (yleisö): {total_average_audience:.2f}\n")
            file.write(f"- Kokonaiskeskiarvo kaikista peleistä (maalit): {total_average_goals:.2f}\n")
            
            if home_audiences:
                home_average_audience = sum(home_audiences) / len(home_audiences)
                home_average_goals = sum(home_goals) / len(home_goals)
                file.write(f"- Kotiotteluiden keskiarvo (yleisö): {home_average_audience:.2f}\n")
                file.write(f"- Kotiotteluiden keskiarvo (maalit): {home_average_goals:.2f}\n")
            
            if away_audiences:
                away_average_audience = sum(away_audiences) / len(away_audiences)
                away_average_goals = sum(away_goals) / len(away_goals)
                file.write(f"- Vierasotteluiden keskiarvo (yleisö): {away_average_audience:.2f}\n")
                file.write(f"- Vierasotteluiden keskiarvo (maalit): {away_average_goals:.2f}\n")
            file.write("\n")
        else:
            file.write(f"## {team}\n")
            file.write("Ei yleisö- tai maalitietoja saatavilla.\n\n")


