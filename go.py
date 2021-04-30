# commands: match show, match #, rankings, stats

import datetime
import json
import shutil

import matplotlib.pyplot as plt
import pytz
import requests
import configparser

# Config parameters
cp = configparser.RawConfigParser()
cp_path = 'config.ini'
cp.read(cp_path)

work_dir = cp.get('config', 'install_path')
api_url = cp.get('config', 'api_url')
contest_id = cp.get('config', 'contest_id')

# Get league matches to find closest
url = f"{api_url}/contests/{contest_id}/sessions"
r = requests.get(url)
sessions = json.loads(r.content)
now = int(datetime.datetime.now().timestamp()) * 1000

closest = min(sessions, key=lambda x: abs(int(x["scheduledTime"]) - now))

# Get info about teams from contest
url = f"{api_url}/contests/{contest_id}"
r = requests.get(url)
contest = json.loads(r.content)
teams = contest["teams"]
selected_teams = []

for side in closest["plannedMatches"]:
    for pm_team in side["teams"]:
        selected = next(team for team in teams if team["_id"] == pm_team["_id"])
        selected_teams.append(selected)

# Copy team logos for selected teams from Source Images to Schedule Images
for i in range(0, len(selected_teams)):
    shutil.copy(f"{work_dir}MJSL OBS TOOLS/Source Images/{selected_teams[i]['name']}.png", f"{work_dir}/MJSL OBS TOOLS/Script Images/Schedule/Schedule-{i+1:02d}.png")

# Generate Script Text files
utc = pytz.utc
match_time = datetime.datetime.fromtimestamp(closest["scheduledTime"] / 1000)
with open(f"{work_dir}/MJSL OBS TOOLS/Script Text/General/Time.txt", "w") as f:
    time_formatted = match_time.astimezone(utc).strftime("%H:%M UTC")
    f.write(time_formatted)

print(
    f"Match 1: {selected_teams[0]['name']}, {selected_teams[1]['name']}, {selected_teams[2]['name']}, {selected_teams[3]['name']}"
)
print(
    f"Match 2: {selected_teams[4]['name']}, {selected_teams[5]['name']}, {selected_teams[6]['name']}, {selected_teams[7]['name']}"
)
print(
    f"Match 3: {selected_teams[0]['name']}, {selected_teams[1]['name']}, {selected_teams[2]['name']}, {selected_teams[3]['name']}"
)
print(
    f"Match 4: {selected_teams[4]['name']}, {selected_teams[5]['name']}, {selected_teams[6]['name']}, {selected_teams[7]['name']}"
)

selected_match = int(input("Select your match: "))
for i in range(0, int(len(selected_teams) / 2)):
    if selected_match % 2 == 0:
        shutil.copy(
            f"{work_dir}/MJSL OBS TOOLS/Source Images/{selected_teams[i+4]['name']}.png",
            f"{work_dir}/MJSL OBS TOOLS/Script Images/Match/Match-{i+1:02d}.png",
        )
    else:
        shutil.copy(
            f"{work_dir}/MJSL OBS TOOLS/Source Images/{selected_teams[i]['name']}.png",
            f"{work_dir}/MJSL OBS TOOLS/Script Images/Match/Match-{i+1:02d}.png",
        )

# Graph
matches_axis = []
matches_passed = 0

for session in sessions:
    if session["scheduledTime"] < now:
        matches_passed += 1

matches_axis.extend(range(0, matches_passed + 1))

for team in teams:
    scores = [0]
    for i in range(0, matches_passed):
        scores.append(sessions[i]["aggregateTotals"][team["_id"]] / 1000)
    plt.plot(
        matches_axis, scores, label=f"{team['name']}: {scores[len(scores) - 1]:.1f}"
    )

plt.legend(bbox_to_anchor=(1, 1), loc="upper left")
plt.savefig(
    f"{work_dir}\\MJSL OBS TOOLS\\Script Images\\Ranking\\rankings.png",
    bbox_inches="tight",
    transparent=True,
)