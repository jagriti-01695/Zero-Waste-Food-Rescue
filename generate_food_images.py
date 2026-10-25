import os
import math
from PIL import Image, ImageDraw, ImageFont

uploads_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static/uploads")
os.makedirs(uploads_dir, exist_ok=True)

# Select best available font
font_title = None
font_dish = None
font_badge = None
font_sub = None

for font_path in ["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf"]:
    if os.path.exists(font_path):
        try:
            font_dish = ImageFont.truetype(font_path, 38)
            font_title = ImageFont.truetype(font_path, 24)
            font_badge = ImageFont.truetype(font_path, 18)
            font_sub = ImageFont.truetype(font_path, 20)
            break
        except Exception:
            pass

if not font_dish:
    font_dish = ImageFont.load_default()
    font_title = ImageFont.load_default()
    font_badge = ImageFont.load_default()
    font_sub = ImageFont.load_default()

items_config = [
    {
        "filename": "food_1.jpg",
        "restaurant": "Kesar Da Dhaba",
        "dish": "Dal Makhani & Lachha Parathas",
        "tag": "12-Hour Slow Cooked · Desi Ghee",
        "badge": "LEGENDARY DHABA",
        "bg1": (120, 25, 10),
        "bg2": (200, 75, 20),
        "dish_accent": (255, 200, 100),
        "icon_type": "dal"
    },
    {
        "filename": "food_2.jpg",
        "restaurant": "Bharawan Da Dhaba",
        "dish": "Amritsari Chole & Stuffed Naan",
        "tag": "Pindi Chole · Tandoori Naan",
        "badge": "SINCE 1912",
        "bg1": (110, 45, 10),
        "bg2": (195, 100, 25),
        "dish_accent": (255, 220, 120),
        "icon_type": "chole"
    },
    {
        "filename": "food_3.jpg",
        "restaurant": "Beera Chicken House",
        "dish": "Tandoori Roasted Chicken & Roti",
        "tag": "Charcoal Roasted · Whole Spices",
        "badge": "SIGNATURE TANDOOR",
        "bg1": (90, 15, 15),
        "bg2": (175, 30, 20),
        "dish_accent": (255, 180, 150),
        "icon_type": "tandoori"
    },
    {
        "filename": "food_4.jpg",
        "restaurant": "Makhan Fish & Chicken",
        "dish": "Crispy Amritsari Fish Fry",
        "tag": "Carom Spiced · Golden Fried",
        "badge": "AMRITSARI SPECIAL",
        "bg1": (130, 60, 10),
        "bg2": (210, 125, 25),
        "dish_accent": (255, 215, 100),
        "icon_type": "fish"
    },
    {
        "filename": "food_5.jpg",
        "restaurant": "Bhai Kulwant Singh",
        "dish": "Crisp Aloo-Pyaaz Amritsari Kulcha",
        "tag": "Tandoor Baked · Butter Topped",
        "badge": "GOLDEN TEMPLE BAZAAR",
        "bg1": (140, 70, 10),
        "bg2": (220, 140, 30),
        "dish_accent": (255, 230, 140),
        "icon_type": "kulcha"
    },
    {
        "filename": "food_6.jpg",
        "restaurant": "Kanha Sweets",
        "dish": "Fluffy Puri Chole & Petha Halwa",
        "tag": "Hot Crispy Puris · Tangy Launji",
        "badge": "HERITAGE BREAKFAST",
        "bg1": (135, 55, 15),
        "bg2": (215, 110, 25),
        "dish_accent": (255, 220, 130),
        "icon_type": "puri"
    },
    {
        "filename": "food_7.jpg",
        "restaurant": "Brothers' Dhaba",
        "dish": "Shahi Paneer Thali & Phulkas",
        "tag": "Cashew Gravy · Tadka Dal",
        "badge": "ROYAL THALI",
        "bg1": (115, 40, 20),
        "bg2": (195, 90, 35),
        "dish_accent": (255, 210, 120),
        "icon_type": "thali"
    },
    {
        "filename": "food_8.jpg",
        "restaurant": "Kulcha Land",
        "dish": "Paneer & Gobhi Chur-Chur Kulchas",
        "tag": "Hand Crushed · Makhan Glazed",
        "badge": "CRISPY CRUST",
        "bg1": (130, 65, 15),
        "bg2": (210, 130, 35),
        "dish_accent": (255, 230, 150),
        "icon_type": "kulcha"
    },
    {
        "filename": "food_9.jpg",
        "restaurant": "Gian Chand Lassi Wale",
        "dish": "Thick Malai Peda Sweet Lassi",
        "tag": "Chilled Curd · Cream Malai Layer",
        "badge": "REFRESHING DRINK",
        "bg1": (20, 70, 60),
        "bg2": (40, 130, 110),
        "dish_accent": (230, 255, 240),
        "icon_type": "lassi"
    },
    {
        "filename": "food_10.jpg",
        "restaurant": "Gurdas Ram Jalebi Wale",
        "dish": "Hot Desi Ghee Jalebi & Rabri",
        "tag": "Crunchy Pretzels · Thick Rabri",
        "badge": "PURE DESI GHEE",
        "bg1": (140, 50, 10),
        "bg2": (225, 110, 20),
        "dish_accent": (255, 225, 110),
        "icon_type": "jalebi"
    },
    {
        "filename": "food_11.jpg",
        "restaurant": "Sharma Sweets",
        "dish": "Khoya Gulab Jamun & Bun Chana",
        "tag": "Cardamom Syrup · Spiced Bun",
        "badge": "SWEET & SAVORY",
        "bg1": (90, 30, 40),
        "bg2": (170, 60, 70),
        "dish_accent": (255, 200, 210),
        "icon_type": "sweet"
    },
    {
        "filename": "food_12.jpg",
        "restaurant": "Ahuja Milk Centre",
        "dish": "Kesar Badam Kheer & Firni Pots",
        "tag": "Kashmiri Kesar · Clay Earthen Pots",
        "badge": "HERITAGE DAIRY",
        "bg1": (120, 75, 15),
        "bg2": (200, 140, 35),
        "dish_accent": (255, 240, 170),
        "icon_type": "kheer"
    },
    {
        "filename": "food_13.jpg",
        "restaurant": "Brijwasi Chat Bhandar",
        "dish": "Crispy Aloo Tikki & Papdi Chaat",
        "tag": "Mint Chutney · Saunth Tamarind",
        "badge": "CRUNCHY CHAAT",
        "bg1": (25, 80, 40),
        "bg2": (50, 140, 75),
        "dish_accent": (230, 255, 200),
        "icon_type": "chaat"
    },
    {
        "filename": "food_14.jpg",
        "restaurant": "Crystal Restaurant",
        "dish": "Royal Mughlai Veg Dum Biryani",
        "tag": "Basmati Long Grain · Dal Bukhara",
        "badge": "MUGHLAI FEAST",
        "bg1": (100, 35, 15),
        "bg2": (185, 80, 25),
        "dish_accent": (255, 215, 130),
        "icon_type": "biryani"
    },
    {
        "filename": "food_15.jpg",
        "restaurant": "Surjit Food Plaza",
        "dish": "Tandoori Chicken Tikka & Kebabs",
        "tag": "Mutton Seekh · Tandoori Parathas",
        "badge": "LAWRENCE ROAD GRILL",
        "bg1": (95, 20, 15),
        "bg2": (180, 45, 25),
        "dish_accent": (255, 190, 140),
        "icon_type": "kebab"
    },
    {
        "filename": "food_16.jpg",
        "restaurant": "Charming Chicken",
        "dish": "Desi Ghee Roast Chicken & Gravy",
        "tag": "Fenugreek Leaves · Tawa Masala",
        "badge": "ROAST SPECIALTY",
        "bg1": (105, 30, 10),
        "bg2": (190, 65, 20),
        "dish_accent": (255, 200, 130),
        "icon_type": "tandoori"
    },
    {
        "filename": "food_17.jpg",
        "restaurant": "Novelty Sweets",
        "dish": "Dal Makhani, Missi Roti & Pinni",
        "tag": "Signature Dal · Whole Wheat Pinni",
        "badge": "TRADITIONAL FEAST",
        "bg1": (115, 50, 20),
        "bg2": (195, 100, 35),
        "dish_accent": (255, 220, 140),
        "icon_type": "thali"
    },
    {
        "filename": "food_18.jpg",
        "restaurant": "Pehalwan Kulcha Shop",
        "dish": "7-Layer Onion & Gobhi Kulchas",
        "tag": "Anardana Chutney · White Butter",
        "badge": "7-LAYER CRUNCH",
        "bg1": (135, 65, 15),
        "bg2": (215, 130, 30),
        "dish_accent": (255, 230, 140),
        "icon_type": "kulcha"
    },
    {
        "filename": "food_19.jpg",
        "restaurant": "Bubby Fish & Chicken",
        "dish": "Tawa Boneless Fish Gravy & Rice",
        "tag": "River Sole Fish · Ginger Juliennes",
        "badge": "CRYSTAL CHOWK",
        "bg1": (125, 55, 15),
        "bg2": (205, 115, 25),
        "dish_accent": (255, 215, 110),
        "icon_type": "fish"
    },
    {
        "filename": "food_20.jpg",
        "restaurant": "Pal Da Dhaba",
        "dish": "Traditional Keema Kaleji & Rotis",
        "tag": "Spiced Minced Mutton · Tandoori Roti",
        "badge": "OLD CITY HERITAGE",
        "bg1": (85, 25, 15),
        "bg2": (165, 50, 25),
        "dish_accent": (255, 185, 135),
        "icon_type": "tandoori"
    },
    {
        "filename": "food_21.jpg",
        "restaurant": "Haveli Amritsar",
        "dish": "Grand Punjabi Royal Thali (Saag)",
        "tag": "Sarson Da Saag · Makki Di Roti",
        "badge": "PUNJABI HERITAGE",
        "bg1": (35, 75, 30),
        "bg2": (70, 135, 55),
        "dish_accent": (245, 255, 190),
        "icon_type": "saag"
    },
    {
        "filename": "food_22.jpg",
        "restaurant": "Giani Tea Stall",
        "dish": "Hot Masala Chai & Spiced Kachoris",
        "tag": "Ginger Cardamom Chai · Flaky Kachori",
        "badge": "COOPER ROAD CHAI",
        "bg1": (120, 60, 25),
        "bg2": (195, 115, 45),
        "dish_accent": (255, 225, 140),
        "icon_type": "chai"
    }
]

def draw_dish_graphic(draw, width, height, icon_type, accent):
    cx = width - 180
    cy = height // 2 + 10
    
    # Outer plate
    draw.ellipse([cx - 130, cy - 130, cx + 130, cy + 130], fill=(255, 255, 255, 30), outline=(255, 255, 255, 80), width=4)
    draw.ellipse([cx - 110, cy - 110, cx + 110, cy + 110], fill=(20, 15, 10, 160), outline=accent, width=3)
    
    # Bowl / food details
    if icon_type in ["dal", "chole", "saag"]:
        draw.ellipse([cx - 85, cy - 85, cx + 85, cy + 85], fill=(50, 20, 10, 240), outline=(255, 200, 100), width=2)
        # Butter dollop
        draw.ellipse([cx - 20, cy - 25, cx + 25, cy + 15], fill=(255, 245, 180))
        # Garnish cream swirls
        draw.arc([cx - 55, cy - 55, cx + 55, cy + 55], 30, 200, fill=(255, 255, 255), width=3)
    elif icon_type == "kulcha":
        # Golden baked bread with spots
        draw.ellipse([cx - 85, cy - 85, cx + 85, cy + 85], fill=(220, 160, 50), outline=(150, 90, 20), width=3)
        draw.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], fill=(255, 240, 180)) # White butter
        # Sesame / coriander specks
        for dx, dy in [(-40, -20), (30, -35), (-25, 40), (45, 25), (-50, 20)]:
            draw.ellipse([cx + dx, cy + dy, cx + dx + 6, cy + dy + 6], fill=(40, 20, 10))
    elif icon_type in ["tandoori", "kebab"]:
        draw.ellipse([cx - 85, cy - 85, cx + 85, cy + 85], fill=(160, 30, 20), outline=(230, 80, 50), width=3)
        draw.rectangle([cx - 40, cy - 15, cx + 40, cy + 15], fill=(120, 20, 15))
        # Lemon slice
        draw.pieslice([cx + 25, cy - 65, cx + 75, cy - 15], 180, 360, fill=(240, 220, 50), outline=(180, 160, 30), width=2)
    elif icon_type == "fish":
        draw.ellipse([cx - 90, cy - 70, cx + 90, cy + 70], fill=(200, 110, 30), outline=(255, 180, 60), width=3)
        # Lemon & onion rings
        draw.ellipse([cx - 60, cy - 40, cx - 10, cy + 10], outline=(255, 255, 255), width=4)
        draw.ellipse([cx - 40, cy - 20, cx + 10, cy + 30], outline=(255, 255, 255), width=4)
    elif icon_type in ["jalebi", "sweet"]:
        draw.ellipse([cx - 85, cy - 85, cx + 85, cy + 85], fill=(230, 110, 20), outline=(255, 200, 50), width=4)
        # Spirals
        draw.arc([cx - 50, cy - 50, cx + 50, cy + 50], 0, 360, fill=(255, 230, 80), width=6)
        draw.arc([cx - 30, cy - 30, cx + 30, cy + 30], 45, 300, fill=(255, 255, 180), width=5)
    elif icon_type in ["lassi", "chai", "kheer"]:
        # Chilled glass / earthenware pot
        draw.rounded_rectangle([cx - 55, cy - 85, cx + 55, cy + 85], radius=25, fill=(245, 240, 220), outline=accent, width=4)
        draw.ellipse([cx - 45, cy - 80, cx + 45, cy - 40], fill=(255, 210, 120)) # Saffron malai top
        # Pistachio sprinkle
        draw.ellipse([cx - 10, cy - 65, cx + 10, cy - 50], fill=(40, 140, 60))
    else: # thali / general
        draw.ellipse([cx - 90, cy - 90, cx + 90, cy + 90], fill=(210, 150, 40), outline=(255, 255, 255), width=3)
        draw.ellipse([cx - 70, cy - 70, cx - 15, cy - 15], fill=(140, 30, 20))
        draw.ellipse([cx + 15, cy - 70, cx + 70, cy - 15], fill=(50, 120, 40))
        draw.ellipse([cx - 40, cy + 15, cx + 40, cy + 70], fill=(220, 180, 90))

def create_food_image(item):
    w, h = 800, 500
    img = Image.new("RGB", (w, h))
    
    # Create smooth horizontal gradient background
    base_draw = ImageDraw.Draw(img)
    r1, g1, b1 = item["bg1"]
    r2, g2, b2 = item["bg2"]
    
    for x in range(w):
        factor = x / w
        r = int(r1 + (r2 - r1) * factor)
        g = int(g1 + (g2 - g1) * factor)
        b = int(b1 + (b2 - b1) * factor)
        base_draw.line([(x, 0), (x, h)], fill=(r, g, b))
        
    # Draw dark overlay on left for sharp text contrast
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)
    
    # Radial glow & left shadow
    for x in range(0, 500):
        alpha = int(180 * (1 - x / 500))
        ov_draw.line([(x, 0), (x, h)], fill=(10, 10, 15, alpha))
        
    # Vignette borders
    ov_draw.rectangle([0, 0, w, 15], fill=(0, 0, 0, 90))
    ov_draw.rectangle([0, h - 15, w, h], fill=(0, 0, 0, 140))
    
    # Dish illustration on the right
    draw_dish_graphic(ov_draw, w, h, item["icon_type"], item["dish_accent"])
    
    # Combine
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)
    
    # Top Badge (Pill)
    badge_text = item["badge"]
    badge_w = len(badge_text) * 12 + 28
    draw.rounded_rectangle([45, 45, 45 + badge_w, 85], radius=20, fill=(255, 255, 255, 40), outline=(255, 255, 255, 120), width=2)
    draw.text((60, 53), badge_text, font=font_badge, fill=(255, 255, 255))
    
    # Restaurant Name (Subheader with gold star)
    rest_text = "★  " + item["restaurant"]
    draw.text((45, 115), rest_text, font=font_title, fill=item["dish_accent"])
    
    # Main Dish Title (Wrap if needed)
    dish_words = item["dish"].split()
    if len(dish_words) > 3:
        line1 = " ".join(dish_words[:3])
        line2 = " ".join(dish_words[3:])
        draw.text((45, 175), line1, font=font_dish, fill=(255, 255, 255))
        draw.text((45, 225), line2, font=font_dish, fill=(255, 255, 255))
        tag_y = 310
    else:
        draw.text((45, 185), item["dish"], font=font_dish, fill=(255, 255, 255))
        tag_y = 265
        
    # Specialty Tag Pill
    tag_text = item["tag"]
    draw.text((45, tag_y), tag_text, font=font_sub, fill=(230, 230, 230))
    
    # Bottom Verified Strip
    draw.line([(45, h - 75), (w - 45, h - 75)], fill=(255, 255, 255, 50), width=1)
    draw.text((45, h - 55), "AMRITSAR FOOD RESCUE INITIATIVE  ·  VERIFIED FRESH LISTING", font=font_badge, fill=(255, 255, 255, 180))
    
    # Save Image
    out_path = os.path.join(uploads_dir, item["filename"])
    img.save(out_path, quality=92)
    print(f"Generated {item['filename']} for {item['restaurant']}")

# Generate all 22 images
for it in items_config:
    create_food_image(it)

# Also create default.jpg
default_item = {
    "filename": "default.jpg",
    "restaurant": "Zero Waste Amritsar",
    "dish": "Fresh Community Meal Rescue",
    "tag": "Hygienically Packed · Quality Inspected",
    "badge": "COMMUNITY DONATION",
    "bg1": (25, 90, 50),
    "bg2": (40, 160, 90),
    "dish_accent": (255, 230, 120),
    "icon_type": "thali"
}
create_food_image(default_item)
print("Finished generating all food card images!")
