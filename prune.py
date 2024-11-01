import sys
import json
from pathlib import Path

def log(*args, **kwargs):
  print(*args, file=sys.stderr, **kwargs)

FOLDER = sys.argv[1]

with open(f"{FOLDER}/index.json") as fp:
  index = json.load(fp)

pruned = []

new_index = {}

fonts = Path(FOLDER)

for name, image in index.items():
  if (fonts / image).is_file():
    new_index[name] = image
  else:
    pruned.append(name)

print(json.dumps(new_index, indent=2))

log(json.dumps(pruned, indent=2))
