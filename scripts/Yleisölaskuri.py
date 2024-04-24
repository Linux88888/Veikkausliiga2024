import re
import requests
from bs4 import BeautifulSoup

url = "https://www.veikkausliiga.com/tilastot/2024/veikkausliiga/ottelut/"

teams = ["HJK", "KuPS", "FC Inter", "SJK", "FC Lahti", "Ilves", "FC Haka", "VPS", "AC Oulu", "Gnistan", "IFK Mariehamn", "EIF"]

team_data = {team: {'Home': [], 'Away': []} for team in teams}

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

table_rows = soup.find_all('tr')

for row in table_rows:
    cells = row.find_all('td')
    if cells and len(cells) > 6:
        date = cells[1].get_text(strip=True)
        time = cells[2].get_text(strip=True)
        date_time = f"{date} {time}"
        match_teams = cells[3].get_text(strip=True)
        audience_text = cells[6].get_text(strip=True)
        audience_match = re.search(r'(\d+)', audience_text)

        if audience_match:
            audience_number = int(audience_match.group(1))
            try:
                home_team, away_team = match_teams.split(' - ')
                home_team = home_team.strip()
                away_team = away_team.strip()

                if home_team in teams:
                    team_data[home_team]['Home'].append(audience_number)
                if away_team in teams:
                    team_data[away_team]['Away'].append(audience_number)
            except ValueError:
                continue  # Ohita virheellisesti muotoillut rivit

# Kirjoitetaan tulokset Markdown-tiedostoon
with open('Yleisö2024.md', 'w') as file:
    file.write("# Veikkausliiga 2024 Yleisömäärät\n\n")
    for team in teams:
        home_games = team_data[team]['Home']
        away_games = team_data[team]['Away']
        all_games = home_games + away_games
        
        if all_games:
            total_average = sum(all_games) / len(all_games)
            file.write(f"## {team}\n")
            file.write(f"- Kokonaiskeskiarvo kaikista peleistä: {total_average:.2f}\n")
            
            if home_games:
                home_average = sum(home_games) / len(home_games)
                file.write(f"- Kotiotteluiden keskiarvo: {home_average:.2f}\n")
            
            if away_games:
                away_average = sum(away_games) / len(away_games)
                file.write(f"- Vierasotteluiden keskiarvo: {away_average:.2f}\n")
            file.write("\n")
        else:
            file.write(f"## {team}\n")
            file.write("Ei yleisötietoja saatavilla.\n\n")
