#!/usr/bin/env python3
"""Generate Rider-Waite-inspired placeholder tarot cards for the deck used by the app."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = Path(__file__).resolve().parent / "cards"

# Names and suit assignments match the app's deck metadata.
CARD_NAMES = [
    "Ace Of Cups",
    "Two Of Cups",
    "Three Of Cups",
    "Four Of Cups",
    "Five Of Cups",
    "Six Of Cups",
    "Seven Of Cups",
    "Eight Of Cups",
    "Nine Of Cups",
    "Ten Of Cups",
    "Page Of Cups",
    "Knight Of Cups",
    "Queen Of Cups",
    "King Of Cups",
    "Ace Of Pentacles",
    "Two Of Pentacles",
    "Three Of Pentacles",
    "Four Of Pentacles",
    "Five Of Pentacles",
    "Six Of Pentacles",
    "Seven Of Pentacles",
    "Eight Of Pentacles",
    "Nine Of Pentacles",
    "Ten Of Pentacles",
    "Page Of Pentacles",
    "Knight Of Pentacles",
    "Queen Of Pentacles",
    "King Of Pentacles",
    "Ace Of Swords",
    "Two Of Swords",
    "Three Of Swords",
    "Four Of Swords",
    "Five Of Swords",
    "Six Of Swords",
    "Seven Of Swords",
    "Eight Of Swords",
    "Nine Of Swords",
    "Ten Of Swords",
    "Page Of Swords",
    "Knight Of Swords",
    "Queen Of Swords",
    "King Of Swords",
    "Ace Of Wands",
    "Two Of Wands",
    "Three Of Wands",
    "Four Of Wands",
    "Five Of Wands",
    "Six Of Wands",
    "Seven Of Wands",
    "Eight Of Wands",
    "Nine Of Wands",
    "Ten Of Wands",
    "Page Of Wands",
    "Knight Of Wands",
    "Queen Of Wands",
    "King Of Wands",
    "The Fool",
    "The Magician",
    "The High Priestess",
    "The Empress",
    "The Emperor",
    "The Hierophant",
    "The Lovers",
    "The Chariot",
    "Strength",
    "The Hermit",
    "Wheel Of Fortune",
    "Justice",
    "The Hanged Man",
    "Death",
    "Temperance",
    "The Devil",
    "The Tower",
    "The Star",
    "The Moon",
    "The Sun",
    "Judgement",
    "The World",
]

SUIT_COLORS = {
    "Cups": (41, 93, 122),
    "Pentacles": (49, 104, 80),
    "Swords": (79, 84, 99),
    "Wands": (161, 89, 39),
    "Major": (130, 96, 36),
}

SUIT_SYMBOLS = {
    "Cups": "♥",
    "Pentacles": "◆",
    "Swords": "✦",
    "Wands": "✧",
    "Major": "✦",
}

CARD_LABELS = {
    "The Fool": "Major Arcana",
    "The Magician": "Major Arcana",
    "The High Priestess": "Major Arcana",
    "The Empress": "Major Arcana",
    "The Emperor": "Major Arcana",
    "The Hierophant": "Major Arcana",
    "The Lovers": "Major Arcana",
    "The Chariot": "Major Arcana",
    "Strength": "Major Arcana",
    "The Hermit": "Major Arcana",
    "Wheel Of Fortune": "Major Arcana",
    "Justice": "Major Arcana",
    "The Hanged Man": "Major Arcana",
    "Death": "Major Arcana",
    "Temperance": "Major Arcana",
    "The Devil": "Major Arcana",
    "The Tower": "Major Arcana",
    "The Star": "Major Arcana",
    "The Moon": "Major Arcana",
    "The Sun": "Major Arcana",
    "Judgement": "Major Arcana",
    "The World": "Major Arcana",
}


def slugify(name: str) -> str:
    return name.lower().replace(" ", "-") + ".jpg"


def get_suit(name: str) -> str:
    if name.startswith("The ") or name in CARD_LABELS:
        return "Major"
    for suit in ["Cups", "Pentacles", "Swords", "Wands"]:
        if name.endswith(f" Of {suit}") or name.endswith(f" {suit}"):
            return suit
    return "Major"


def load_font(size: int, bold: bool = True):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSerif-Bold.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


def draw_card(name: str, out_path: Path):
    suit = get_suit(name)
    accent = SUIT_COLORS[suit]
    bg = Image.new("RGB", (600, 1000), "#f7f0e4")
    draw = ImageDraw.Draw(bg)

    # Outer border + inner panel.
    border_color = (32, 28, 24)
    outer = [(22, 22), (578, 978)]
    draw.rounded_rectangle(outer, radius=28, fill=(247, 240, 228), outline=border_color, width=6)
    draw.rounded_rectangle([(42, 42), (558, 958)], radius=24, fill=(250, 247, 239), outline=accent, width=4)

    # Top and bottom band.
    draw.rounded_rectangle([(60, 70), (540, 128)], radius=16, fill=accent)
    draw.rounded_rectangle([(60, 872), (540, 930)], radius=16, fill=accent)

    # Titles.
    serif_bold = load_font(26)
    serif_small = load_font(18)
    symbol_font = load_font(84)
    mono_font = load_font(16, bold=False)

    title = name.upper()
    title_text = title
    if len(title) > 22:
        title_text = " ".join(title.split()[:4])

    draw.text((300, 98), title_text, fill="white", font=serif_bold, anchor="mm")
    draw.text((300, 56), "RIDER-WAITE PLACEHOLDER", fill=accent, font=serif_small, anchor="mm")

    # Central glyph / emblem.
    glyph = SUIT_SYMBOLS[suit]
    if suit == "Major":
        # Different major arcana glyphs based on card name as a subtle placeholder.
        glyph_map = {
            "The Fool": "✦",
            "The Magician": "✧",
            "The High Priestess": "☾",
            "The Empress": "❀",
            "The Emperor": "♛",
            "The Hierophant": "✧",
            "The Lovers": "♥",
            "The Chariot": "✦",
            "Strength": "♞",
            "The Hermit": "☼",
            "Wheel Of Fortune": "☸",
            "Justice": "⚖",
            "The Hanged Man": "◎",
            "Death": "☠",
            "Temperance": "⚚",
            "The Devil": "✹",
            "The Tower": "⚡",
            "The Star": "✦",
            "The Moon": "☾",
            "The Sun": "☀",
            "Judgement": "✺",
            "The World": "◎",
        }
        glyph = glyph_map.get(name, "✦")

    # Central medallion.
    draw.rounded_rectangle([(160, 230), (440, 770)], radius=26, fill=(255, 255, 255), outline=accent, width=3)
    draw.text((300, 500), glyph, fill=accent, font=symbol_font, anchor="mm")

    # Corner marks.
    corner_y = 150
    for x in [102, 498]:
        draw.text((x, 150), glyph, fill=accent, font=load_font(34), anchor="mm")
        draw.text((x, 850), glyph, fill=accent, font=load_font(34), anchor="mm")

    # Additional ornamental frame.
    for o in [0, 14]:
        draw.rounded_rectangle([(80 + o, 150 + o), (520 - o, 850 - o)], radius=18, outline=(170, 149, 117), width=2)

    # Bottom suit label.
    label = CARD_LABELS.get(name, suit.upper())
    draw.text((300, 898), label, fill="white", font=serif_small, anchor="mm")

    # Small footer motif.
    draw.text((300, 922), "Rider-Waite-inspired placeholder", fill=(66, 57, 49), font=mono_font, anchor="mm")

    bg = bg.convert("RGB")
    bg.save(out_path, quality=95, subsampling=0)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for name in CARD_NAMES:
        slug = slugify(name)
        out_path = OUT_DIR / slug
        draw_card(name, out_path)
        print(f"created {out_path.name}")


if __name__ == "__main__":
    main()
