import re
import requests
from bs4 import BeautifulSoup

# URL-osoitteet mestaruussarjalle ja haastajasarjalle
url = "https://www.veikkausliiga.com/tilastot/2024/veikkausliiga/ottelut/"
url_championship = "https://www.veikkausliiga.com/tilastot/2024/veikkausliiga/ottelut/?group=2&team=#stats-wrapper"
url_challenger = "https://www.veikkausliiga.com/tilastot/2024/veikkausliiga/ottelut/?group=3&team=#stats-wrapper"

teams = ["HJK", "KuPS", "FC Inter", "SJK", "FC Lahti", "Ilves", "FC Haka", "VPS", "AC Oulu", "Gnistan", "IFK Mariehamn", "EIF"]

team_data = {
    team: {
        'Home': {'audiences': [], 'goals_scored': [], 'goals_conceded': [], 'over_2_5': 0},
        'Away': {'audiences': [], 'goals_scored': [], 'goals_conceded': [], 'over_2_5': 0}
    } for team in teams
}

def get_league_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table_rows = soup.find_all('tr')

    audiences = []
    goals = 0
    over_2_5_games = 0

    for row in table_rows:
        cells = row.find_all('td')
        if cells and len(cells) > 6:
            result_text = cells[5].get_text(strip=True)
            audience_text = cells[6].get_text(strip=True)

            result_match = re.search(r'(\d+) — (\d+)', result_text)
            audience_number = int(re.search(r'(\d+)', audience_text).group(1)) if re.search(r'(\d+)', audience_text) else 0

            if result_match:
                home_goals, away_goals = map(int, result_match.groups())
                goals += home_goals + away_goals
                audiences.append(audience_number)
                if home_goals + away_goals > 2.5:
                    over_2_5_games += 1

    total_games = len(audiences)
    average_audience = sum(audiences) / total_games if total_games else 0
    average_goals = goals / total_games if total_games else 0
    over_2_5_percent = (over_2_5_games / total_games * 100) if total_games else 0

    return {
        'total_audience': sum(audiences),
        'average_audience': average_audience,
        'total_goals': goals,
        'average_goals': average_goals,
        'over_2_5_percent': over_2_5_percent,
        'total_games': total_games
    }

# Haetaan alkuperäisen sarjan tiedot
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
table_rows = soup.find_all('tr')

total_audiences = []
total_goals = 0
total_over_2_5_games = 0

for row in table_rows:
    cells = row.find_all('td')
    if cells and len(cells) > 6:
        match_teams = cells[3].get_text(strip=True)
        result_text = cells[5].get_text(strip=True)
        audience_text = cells[6].get_text(strip=True)

        result_match = re.search(r'(\d+) — (\d+)', result_text)
        audience_number = int(re.search(r'(\d+)', audience_text).group(1)) if re.search(r'(\d+)', audience_text) else 0

        if result_match:
            home_goals, away_goals = map(int, result_match.groups())
            total_goals += home_goals + away_goals
            total_audiences.append(audience_number)
            if home_goals + away_goals > 2.5:
                total_over_2_5_games += 1

            home_team, away_team = [team.strip() for team in match_teams.split(' - ')]

            if home_team in teams:
                team_data[home_team]['Home']['audiences'].append(audience_number)
                team_data[home_team]['Home']['goals_scored'].append(home_goals)
                team_data[home_team]['Home']['goals_conceded'].append(away_goals)
                if home_goals + away_goals > 2.5:
                    team_data[home_team]['Home']['over_2_5'] += 1

            if away_team in teams:
                team_data[away_team]['Away']['audiences'].append(audience_number)
                team_data[away_team]['Away']['goals_scored'].append(away_goals)
                team_data[away_team]['Away']['goals_conceded'].append(home_goals)
                if home_goals + away_goals > 2.5:
                    team_data[away_team]['Away']['over_2_5'] += 1

total_games = len(total_audiences)
total_average_audience = sum(total_audiences) / total_games if total_games else 0
total_average_goals = total_goals / total_games if total_games else 0
total_over_2_5_percent = (total_over_2_5_games / total_games * 100) if total_games else 0

# Haetaan mestaruussarjan ja haastajasarjan tiedot
championship_data = get_league_data(url_championship)
challenger_data = get_league_data(url_challenger)

# Kirjoitetaan tulokset Markdown-tiedostoon
with open('Yleisö2024.md', 'w', encoding='utf-8') as file:
    # Mestaruus- ja haastajasarjan keskiarvot yleisömäärän perusteella
    file.write("# Mestaruussarjan ja Haastajasarjan Yleisömäärät\n\n")
    file.write(f"## Mestaruussarjan keskiarvoyleisömäärä: {championship_data['average_audience']:.2f}\n")
    file.write(f"## Haastajasarjan keskiarvoyleisömäärä: {challenger_data['average_audience']:.2f}\n\n")
    
    # Kokonaistiedot alkuperäisestä sarjasta
    file.write("# Veikkausliiga 2024 - Yleisömäärät, Maalit ja Yli 2.5 Maalia Pelissä\n\n")
    file.write(f"### Veikkausliigan kokonaisyleisömäärä: {sum(total_audiences)}\n")
    file.write(f"### Veikkausliigan keskiarvoyleisömäärä per peli: {total_average_audience:.2f}\n")
    file.write(f"### Veikkausliigan yli 2.5 maalia pelissä: {total_over_2_5_percent:.2f}% ({total_over_2_5_games} / {total_games})\n")
    file.write(f"### Veikkausliigan kokonaismäärä tehdyt maalit: {total_goals}\n")
    file.write(f"### Veikkausliigan keskiarvo maalit per peli: {total_average_goals:.2f}\n\n")

    # Mestaruussarjan tiedot
    file.write("## Mestaruussarja\n")
    file.write(f"### Kokonaisyleisömäärä: {championship_data['total_audience']}\n")
    file.write(f"### Keskiarvoyleisömäärä per peli: {championship_data['average_audience']:.2f}\n")
    file.write(f"### Kokonaismaalimäärä: {championship_data['total_goals']}\n")
    file.write(f"### Keskiarvo maalit per peli: {championship_data['average_goals']:.2f}\n")
    file.write(f"### Yli 2.5 maalia pelissä: {championship_data['over_2_5_percent']:.2f}% ({championship_data['total_games']} peliä)\n\n")

    # Haastajasarjan tiedot
    file.write("## Haastajasarja\n")
    file.write(f"### Kokonaisyleisömäärä: {challenger_data['total_audience']}\n")
    file.write(f"### Keskiarvoyleisömäärä per peli: {challenger_data['average_audience']:.2f}\n")
    file.write(f"### Kokonaismaalimäärä: {challenger_data['total_goals']}\n")
    file.write(f"### Keskiarvo maalit per peli: {challenger_data['average_goals']:.2f}\n")
    file.write(f"### Yli 2.5 maalia pelissä: {challenger_data['over_2_5_percent']:.2f}% ({challenger_data['total_games']} peliä)\n")

# Tulostetaan onnistumisviesti
print("Data written to Yleisö2024.md successfully.")
