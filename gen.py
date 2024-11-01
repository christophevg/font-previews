from pathlib import Path

from wand.image import Image
from wand.drawing import Drawing
from wand.color import Color

from fontTools import ttLib

import json

import sys

FOLDER = sys.argv[1]
BACKGROUND = None
if len(sys.argv) > 2:
  BACKGROUND = sys.argv[2]

try:
  with open("pruned.json") as fp:
    pruned = json.load(fp)
except FileNotFoundError:
  pruned = []

def log(*args, **kwargs):
  print(*args, file=sys.stderr, **kwargs)

def generate_preview(fontfile):
  log(f"processing {fontfile}")

  fontname = None
  try:
    font = ttLib.TTFont(fontfile)
    # for i in range(6):
    #   log(i+1, font["name"].getDebugName(i+1))
    fontname  = font["name"].getDebugName(4)
    fontstyle = font["name"].getDebugName(2)
    if not fontname.endswith(fontstyle):
      fontname = fontname + " " + fontstyle
    output    = font["name"].getDebugName(6) + ".png"

    while fontname.startswith("."):
      fontname = fontname[1:]
    while output.startswith("."):
      output = output[1:]

    if fontname in pruned:
      log(f"   ⚠️ {fontname} was pruned")
      output = None
    else:
      left, top, width, height = 0, 0, 1440, 87
      with Image(width=width, height=height) as canvas:
        with Drawing() as context:
          if BACKGROUND:
            context.fill_color = BACKGROUND
            context.rectangle(left=left, top=top, width=width, height=height)

          context.font = fontfile
          context.font_size = 60
          context.fill_color = Color("BLACK")
          context.text(10, canvas.height-20, f"{fontname} AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz 0123456789")
          context(canvas)
          canvas.save(filename=f"{FOLDER}/{output}")
  except Exception as ex:
    log(f"   🚨 {ex}")
    output = None

  return (fontname, output)

paths = [
  "/Library/Fonts",
  "/System/Library/Fonts",
  "/System/Library/Fonts/Supplemental",
  "~/Library/Fonts"
]

skip = []

index = {}

for path in paths:
  for filename in Path(path).expanduser().glob("*.*"):
    if filename.is_file():
      if not filename.stem in skip:
        name, output = generate_preview(str(filename))
        if output:
          index[name] = output

print(json.dumps(index, indent=2))
