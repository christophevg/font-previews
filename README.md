# Font Previews

> two small scripts to generate font previews

**WARNING** YMMV - these scripts are configured using hardcoded variables and expect the system to be mine 😇

## Step 0: Requirements

```console
% cat requirements.txt
fonttools==4.54.1
Wand==0.6.13
% pip install -r requirements.txt
```

Also ensure that `Wand` finds ImageMagick:

```console
ImportError: MagickWand shared library not found.
You probably had not installed ImageMagick library.
Try to install:
  brew install freetype imagemagick
```

When installed using Homebrew, two environment variables need fine-tuning:

```console
% cat .env 
export MAGICK_HOME=/opt/homebrew/opt/imagemagick/
export PATH="/opt/homebrew/opt/imagemagick/bin:$PATH"                         

% . ./.env
```


## Step 1: Generate previews for known/configured folders on the system

Configured paths:

```python
paths = [
  "/Library/Fonts",
  "/System/Library/Fonts",
  "/System/Library/Fonts/Supplemental",
  "~/Library/Fonts"
]
```

Using the Makefile:

```console
% make fonts
mkdir -p fonts
python gen.py fonts > fonts/index.json
processing /Library/Fonts/NotoSansSC-Regular.otf
processing /Library/Fonts/Inconsolata_Regular.ttf
processing /Library/Fonts/Mukta_Regular.ttf
processing /Library/Fonts/PT_Sans_Web_BoldItalic.ttf
processing /Library/Fonts/NotoSansTC-Regular.otf
processing /Library/Fonts/Inconsolata_Bold.ttf
processing /Library/Fonts/NotoSansArabic_Regular.ttf
...
```

the `fonts/` folder now contains images for alle fonts detected, along with an `index.json` mapping the font's name to the generated preview image:

```json
{
  "Inconsolata Regular": "Inconsolata-Regular.png",
  "Mukta Regular": "Mukta-Regular.png",
  "PT Sans Bold Italic": "PTSans-BoldItalic.png",
  "Noto Sans TC Regular": "NotoSansTC-Regular.png",
  "Inconsolata Bold": "Inconsolata-Bold.png",
  "Open Sans Cond Light Regular": "OpenSans-CondensedLight.png",
  "Mitr Regular": "Mitr-Regular.png",
  "Lora Regular": "Lora-Regular.png",
  "Great Vibes Regular": "GreatVibes-Regular.png",
  ...
```

## Step 2: Inspect image files and remove unwanted ones

Some font files produce no proper preview and you want to prune them. After removing all unwanted previews, the `index.json` file can be updated using the Makefile:

```console
% make prune
python prune.py fonts > fonts/index.pruned.json
[
  "Noto Sans SC Regular",
  "Noto Sans Arabic Regular",
  "Noto Sans Devanagari Regular",
  "DYMO Symbols Regular",
  "Noto Sans SC Light Regular",
  "Noto Sans Thai Regular",
  "Symbol Regular",
  "LastResort Regular",
  "SF Georgian Regular",
  "SF Hebrew Regular",
  "Zapf Dingbats Regular",
  "SF Armenian Regular",
...
```

The script removes all index entries that are no longer available and outputs a JSON list of those pruned entries on stderr. 

Copy those to a `pruned.json` file in the root and next time, the `make fonts` command will skip these pruned fonts.

```console
 % make fonts              
mkdir -p fonts
python gen.py fonts > fonts/index.json
processing /Library/Fonts/NotoSansSC-Regular.otf
   ⚠️ Noto Sans SC Regular was pruned                  👈👈👈👈👈👈👈
processing /Library/Fonts/Inconsolata_Regular.ttf
processing /Library/Fonts/Mukta_Regular.ttf
processing /Library/Fonts/PT_Sans_Web_BoldItalic.ttf
processing /Library/Fonts/NotoSansTC-Regular.otf
processing /Library/Fonts/Inconsolata_Bold.ttf
processing /Library/Fonts/NotoSansArabic_Regular.ttf
...
```
