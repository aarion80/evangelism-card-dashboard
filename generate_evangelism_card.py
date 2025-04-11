from PIL import Image, ImageDraw, ImageFont
import os
import random

# === CONFIGURATION ===
BACKGROUND_FOLDER = "backgrounds"  # Folder containing your 36 backgrounds
OUTPUT_FOLDER = "output_cards"
FONT_PATH = "fonts/Roboto-Bold.ttf"  # Ensure this font file exists or replace it
FONT_SIZE_MAIN = 48
FONT_SIZE_VERSE = 32
TEXT_COLOR = (255, 255, 255)
SHADOW_COLOR = (0, 0, 0)
IMAGE_SIZE = (1024, 1024)

# === SAMPLE MESSAGES ===
CARDS = [
    {
        "quote": "\"Start with a story, not a sermon.\"",
        "verse": "— Colossians 1:28"
    },
    {
        "quote": "\"Grace opens the door even when we close it.\"",
        "verse": "— Ephesians 2:8"
    }
]

# === RENDER FUNCTION ===
def draw_centered_text(draw, text, position, font, max_width):
    lines = []
    words = text.split()
    line = ""
    for word in words:
        test_line = f"{line} {word}".strip()
        w, h = draw.textsize(test_line, font=font)
        if w <= max_width:
            line = test_line
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)

    y_offset = position[1] - (len(lines) * font.size) // 2
    for line in lines:
        w, h = draw.textsize(line, font=font)
        x = (IMAGE_SIZE[0] - w) // 2
        draw.text((x+2, y_offset+2), line, font=font, fill=SHADOW_COLOR)
        draw.text((x, y_offset), line, font=font, fill=TEXT_COLOR)
        y_offset += font.size + 10

# === MAIN GENERATOR ===
def generate_cards():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    background_files = sorted([f for f in os.listdir(BACKGROUND_FOLDER) if f.lower().endswith(('jpg', 'jpeg', 'png'))])
    font_main = ImageFont.truetype(FONT_PATH, FONT_SIZE_MAIN)
    font_verse = ImageFont.truetype(FONT_PATH, FONT_SIZE_VERSE)

    for i, card in enumerate(CARDS):
        bg_filename = background_files[i % len(background_files)]
        bg_path = os.path.join(BACKGROUND_FOLDER, bg_filename)
        bg = Image.open(bg_path).resize(IMAGE_SIZE).convert("RGB")

        img = bg.copy()
        draw = ImageDraw.Draw(img)

        draw_centered_text(draw, card["quote"], (IMAGE_SIZE[0]//2, IMAGE_SIZE[1]//2 - 50), font_main, IMAGE_SIZE[0] - 100)
        draw_centered_text(draw, card["verse"], (IMAGE_SIZE[0]//2, IMAGE_SIZE[1]//2 + 100), font_verse, IMAGE_SIZE[0] - 100)

        filename = f"card_{i+1:02}.png"
        img.save(os.path.join(OUTPUT_FOLDER, filename))
        print(f"Saved: {filename}")

if __name__ == "__main__":
    generate_cards()

