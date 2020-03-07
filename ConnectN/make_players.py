#!/usr/bin/env python3

from pathlib import Path
from tokenize import tokenize

imports = []
players = []

# Go through the directories
for d in Path("unzipped").iterdir():
    # Get the player name
    pname = d.name.split('/')[0]
    imports.append("from unzipped.{0}.alpha_beta_agent import THE_AGENT as {0}".format(pname))
    players.append("    \"{0}\" : {0},".format(pname))

# Print the file
for i in imports:
    print(i)

print("PLAYERS = {")
for p in players:
    print(p)
print("}")
