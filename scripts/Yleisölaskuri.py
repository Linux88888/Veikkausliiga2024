import re
import requests
from bs4 import BeautifulSoup

url = "https://www.veikkausliiga.com/tilastot/2024/veikkausliiga/ottelut/"
teams = ["HJK", "KuPS", "FC Inter", "SJK", "FC Lahti", "Ilves", "FC Haka", "VPS", "AC Oulu", "Gnistan", "IFK Mariehamn", "EIF"]

team_data = {
    team: {
        'Home': {'audiences': [], 'goals_scored': [], 'goals_conceded': [], 'over_2_5': 0},
        'Away': {'audiences': [], 'goals_scored': [], 'goals_conceded': [], 'over_2_5': 0}
    } for team in teams
}

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
table_rows = soup.find_all('tr')

for row in table_rows:
    cells = row.find_all('td')
    if cells and len(cells) > 6:
        date = cells[1].get_text(strip=True)
        time = cells[2].get_text(strip=True)
        match_teams = cells[3].get_text(strip=True)
        result_text = cells[5].get_text(strip=True)
        audience_text = cells[6].get_text(strip=True)

        result_match = re.search(r'(\d+) — (\d+)', result_text)
        audience_number = int(re.search(r'(\d+)', audience_text).group(1)) if re.search(r'(\d+)', audience_text) else 0

        if result_match:
            home_goals, away_goals = map(int, result_match.groups())
            total_goals = home_goals + away_goals
            home_team, away_team = [team.strip() for team in match_teams.split(' - ')]

            if home_team in teams:
                team_data[home_team]['Home']['audiences'].append(audience_number)
                team_data[home_team]['Home']['goals_scored'].append(home_goals)
                team_data[home_team]['Home']['goals_conceded'].append(away_goals)
                if total_goals > 2.5:
                    team_data[home_team]['Home']['over_2_5'] += 1

            if away_team in teams:
                team_data[away_team]['Away']['audiences'].append(audience_number)
                team_data[away_team]['Away']['goals_scored'].append(away_goals)
                team_data[away_team]['Away']['goals_conceded'].append(home_goals)
                if total_goals > 2.5:
                    team_data[away_team]['Away']['over_2_5'] += 1

# Kirjoitetaan tulokset Markdown-tiedostoon
with open('Yleisö2024.md', 'w') as file:
    file.write("# Veikkausliiga 2024 Yleisömäärät, Maalit ja Yli 2.5 Maalia Pelissä\n\n")
    for team, data in team_data.items():
        home_audiences = data['Home']['audiences']
        home_goals_scored = data['Home']['goals_scored']
        home_goals_conceded = data['Home']['goals_conceded']
        home_games = len(home_audiences)
        
        away_audiences = data['Away']['audiences']
        away_goals_scored = data['Away']['goals_scored']
        away_goals_conceded = data['Away']['goals_conceded']
        away_games = len(away_audiences)

        file.write(f"## {team}\n")
        if home_games > 0:
            file.write(f"- Kotiotteluiden keskiarvo (yleisö): {sum(home_audiences) / home_games:.2f}\n")
            file.write(f"- Kotiotteluiden keskiarvo (maalit tehty): {sum(home_goals_scored) / home_games:.2f}\n")
            file.write(f"- Kotiotteluiden keskiarvo (maalit päästetty): {sum(home_goals_conceded) / home_games:.2f}\n")
            file.write(f"- Kotiotteluiden yli 2.5 maalia pelissä: {data['Home']['over_2_5'] / home_games * 100:.2f}%\n")
        if away_games > 0:
            file.write(f"- Vierasotteluiden keskiarvo (yleisö): {sum(away_audiences) / away_games:.2f}\n")
            file.write(f"- Vierasotteluiden keskiarvo (maalit tehty): {sum(away_goals_scored) / away_games:.2f}\n")
            file.write(f"- Vierasotteluiden keskiarvo (maalit päästetty): {sum(away_goals_conceded) / away_games:.2f}\n")
            file.write(f"- Vierasotteluiden yli 2.5 maalia pelissä: {data['Away']['over_2_5'] / away_games * 100:.2f}%\n")
        file.write("\n")

