# commands: match show, match #, rankings, stats

import configparser
import datetime
import json
import shutil

import matplotlib.font_manager as mfm
import matplotlib.pyplot as plt
import pytz
import requests
from fontTools.ttLib import TTFont


def char_in_font(uc_char, font):
    """See if a given unicode character is in a given font"""
    try:
        for cmap in font["cmap"].tables:
            if cmap.isUnicode():
                if ord(uc_char) in cmap.cmap:
                    return True
        return False
    except AssertionError:
        return False


# Config parameters
cp = configparser.RawConfigParser()
cp_path = "config.ini"
cp.read(cp_path)

work_dir = cp.get("config", "install_path")
api_url = cp.get("config", "api_url")
contest_id = cp.get("config", "contest_id")

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
    shutil.copy(
        f"{work_dir}MJSL OBS TOOLS/Source Images/{selected_teams[i]['_id']}.png",
        f"{work_dir}/MJSL OBS TOOLS/Script Images/Schedule/Schedule-{i+1:02d}.png",
    )

# Generate Script Text files
utc = pytz.utc
match_time = datetime.datetime.fromtimestamp(closest["scheduledTime"] / 1000)
with open(f"{work_dir}/MJSL OBS TOOLS/Script Text/General/Time.txt", "w") as f:
    time_formatted = match_time.astimezone(utc).strftime("%H:%M UTC")
    f.write(time_formatted)

with open(f"{work_dir}/MJSL OBS TOOLS/Script Text/General/Session.txt", "w") as f:
    session_name = closest["name"]
    f.write(session_name)

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
            f"{work_dir}/MJSL OBS TOOLS/Source Images/{selected_teams[i+4]['_id']}.png",
            f"{work_dir}/MJSL OBS TOOLS/Script Images/Match/Match-{i+1:02d}.png",
        )
    else:
        shutil.copy(
            f"{work_dir}/MJSL OBS TOOLS/Source Images/{selected_teams[i]['_id']}.png",
            f"{work_dir}/MJSL OBS TOOLS/Script Images/Match/Match-{i+1:02d}.png",
        )

# Graph
matches_axis = ["Start"]
matches_passed = 0

for session in sessions:
    if session["scheduledTime"] < now:
        matches_axis.append(session["name"])
        matches_passed += 1

font_info = [(f.fname, f.name) for f in mfm.fontManager.ttflist]
font_path = None

# Sort teams score table from closest match
sorted_teams = sorted(
    closest["aggregateTotals"].items(), key=lambda x: x[1], reverse=True
)

for sorted_team in sorted_teams:
    scores = [0]
    for i in range(0, matches_passed):
        scores.append(sessions[i]["aggregateTotals"][sorted_team[0]] / 1000)

    # Get team info from contest
    contest_team = next(
        (cteam for cteam in contest["teams"] if cteam["_id"] == sorted_team[0])
    )

    # Check for unicode team names because why god why
    for x in contest_team["name"]:
        if ord(x) > 127:
            while not font_path:
                for i, font in enumerate(font_info):
                    # Find a font on user's machine that supports the team name
                    if char_in_font(x, TTFont(font[0], fontNumber=0)):
                        font_path = font[0]

    plt.plot(
        matches_axis,
        scores,
        label=f"{contest_team['name']}: {scores[len(scores) - 1]:.1f}",
        color=f"#{contest_team['color']}",
    )

prop = mfm.FontProperties(fname=font_path)

plt.legend(bbox_to_anchor=(1, 1), loc="upper left", prop=prop)
plt.savefig(
    f"{work_dir}\\MJSL OBS TOOLS\\Script Images\\Ranking\\rankings.png",
    bbox_inches="tight",
    transparent=True,
)
