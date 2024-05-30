import pandas as pd
import requests
from bs4 import BeautifulSoup

url = "https://www.iplt20.com/auction/2024"
r = requests.get(url)
soup = BeautifulSoup(r.text, "lxml")

# Find the section containing team data (adjust selectors based on inspection)
team_data = soup.find_all("div", class_="agv-main")  # Replace with appropriate class

# Step 3: Initialize lists to store the data
teams = []
funds_remaining = []
overseas_players = []
total_players = []

# Step 4: Find and iterate through each team's data container and extract the relevant information
team_data_containers = soup.find_all("div", class_="agv-main")

for container in team_data_containers:
    # Extract team name
    try:
        team_name_element = container.find("div", class_="agv-team-name")
        team_name = team_name_element.text.strip() if team_name_element else ""
    except:
        team_name = ""
    teams.append(team_name)

    # Extract funds remaining
    try:
        fund_remaining_element = container.find("div", class_="avg-fund-remaining").find("span", class_="fr-fund")
        fund_remaining = fund_remaining_element.text.strip() if fund_remaining_element else ""
    except:
        fund_remaining = ""
    funds_remaining.append(fund_remaining)

    # Extract player info
    try:
        player_info = container.find("ul", class_="mb-0 px-1").find_all("li", class_="m-0")

        # Overseas players
        try:
            overseas_player_count = ""
            for li in player_info:
                if li.find("span", class_="fr-name").text.strip() == "Overseas Players":
                    overseas_player_count = li.find("span", class_="fr-fund").text.strip()
                    break
        except:
            overseas_player_count = ""
        overseas_players.append(overseas_player_count)

        # Total players
        try:
            total_player_count = ""
            for li in player_info:
                if li.find("span", class_="fr-name").text.strip() == "Total Players":
                    total_player_count = li.find("span", class_="fr-fund").text.strip()
                    break
        except:
            total_player_count = ""
        total_players.append(total_player_count)
    except:
        overseas_players.append("")
        total_players.append("")

# Step 5: Create a DataFrame using the extracted data
data = {
    "Team": teams,
    "Funds Remaining": funds_remaining,
    "Overseas Players": overseas_players,
    "Total Players": total_players
}

df = pd.DataFrame(data)
print(df)

# Step 6: Write the DataFrame to an Excel file
df.to_excel("IPL_2024_Data.xlsx")

print("Data successfully written to IPL_Auction_Data.xlsx")

