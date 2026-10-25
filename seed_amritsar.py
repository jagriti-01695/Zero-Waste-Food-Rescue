import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app import app, db, User, Food, Request, Rating, bcrypt

def seed_database():
    with app.app_context():
        print("Clearing old dummy food items and requests...")
        # Clear existing requests, ratings, and foods to replace with clean Amritsar data
        Request.query.delete()
        Rating.query.delete()
        
        # Clear saved food associations
        db.session.execute(db.text("DELETE FROM saved_food"))
        Food.query.delete()
        
        # Keep or update Jagriti (Receiver)
        jagriti = User.query.filter_by(email="jagriti12@gmail.com").first()
        if not jagriti:
            hashed_pwd = bcrypt.generate_password_hash("123456").decode("utf-8")
            jagriti = User(name="Jagriti Sharma", email="jagriti12@gmail.com", password=hashed_pwd, role="receiver")
            db.session.add(jagriti)
        else:
            jagriti.name = "Jagriti Sharma"
            jagriti.role = "receiver"
            
        # Admin account
        admin = User.query.filter_by(email="admin@amritsarescue.org").first()
        if not admin:
            admin = User.query.filter_by(role="admin").first()
            if admin:
                admin.name = "Amritsar Rescue Admin"
                admin.email = "admin@amritsarescue.org"
                admin.password = bcrypt.generate_password_hash("admin123").decode("utf-8")
            else:
                admin = User(name="Amritsar Rescue Admin", email="admin@amritsarescue.org", 
                             password=bcrypt.generate_password_hash("admin123").decode("utf-8"), role="admin")
                db.session.add(admin)

        db.session.commit()

        # Delete any existing donor users that aren't admin or jagriti
        existing_donors = User.query.filter(User.role == "donor").all()
        for d in existing_donors:
            db.session.delete(d)
        db.session.commit()

        now = datetime.now()
        default_pwd = bcrypt.generate_password_hash("password123").decode("utf-8")

        # 22 Amritsar Restaurants Data
        restaurants_data = [
            {
                "name": "Kesar Da Dhaba",
                "email": "kesar@amritsarescue.org",
                "phone_tag": "0183-2552103",
                "title": "Authentic Dal Makhani & Lachha Paratha Pack",
                "description": "15 freshly packed meal boxes of our legendary slow-cooked Dal Makhani (cooked 12+ hours with desi ghee) with crispy hot lachha parathas. Pure vegetarian, hygienically sealed.",
                "location": "Chowk Passian, Near Telephone Exchange, Amritsar, Punjab 143001",
                "cost_type": "Free",
                "hours": 5,
                "rating": 5
            },
            {
                "name": "Bharawan Da Dhaba",
                "email": "bharawan@amritsarescue.org",
                "phone_tag": "0183-2541447",
                "title": "Amritsari Chole & Stuffed Naan Meal Box",
                "description": "20 wholesome meal boxes featuring spiced Amritsari Pindi Chole, tandoori stuffed kulcha naan, and pickled onions. Prepared during afternoon service.",
                "location": "Near Town Hall, Hall Bazar, Golden Temple Road, Amritsar, Punjab 143006",
                "cost_type": "Free",
                "hours": 7,
                "rating": 5
            },
            {
                "name": "Beera Chicken House",
                "email": "beera@amritsarescue.org",
                "phone_tag": "0183-2223849",
                "title": "Tandoori Roasted Chicken & Roomali Roti Combo",
                "description": "12 whole portions of signature whole-spice marinated roasted tandoori chicken, accompanied by soft roomali rotis and fresh mint chutney.",
                "location": "Majitha Road, Opposite Bandari Hospital, Sehaj Avenue, Amritsar, Punjab 143001",
                "cost_type": "Discounted",
                "hours": 4,
                "rating": 5
            },
            {
                "name": "Makhan Fish & Chicken Corner",
                "email": "makhan@amritsarescue.org",
                "phone_tag": "0183-2401662",
                "title": "Crispy Amritsari Fish Fry & Butter Chicken Meal",
                "description": "10 family packs of authentic carom-spiced batter-fried Singhara fish fillets and rich tawa butter chicken gravy with butter naan.",
                "location": "Majitha Road, Near Madan Lal Dhingra Stadium, Amritsar, Punjab 143001",
                "cost_type": "Discounted",
                "hours": 6,
                "rating": 4
            },
            {
                "name": "Bhai Kulwant Singh Kulchian Wale",
                "email": "kulwant@amritsarescue.org",
                "phone_tag": "0183-2550183",
                "title": "Crisp Aloo-Pyaaz Amritsari Kulcha with Chana",
                "description": "25 golden-brown tandoor-baked layered kulchas loaded with potato-onion filling, accompanied by tangy imli-pyaaz chutney and chickpea curry.",
                "location": "Bazar Kathian, Near Golden Temple Main Entrance, Amritsar, Punjab 143006",
                "cost_type": "Free",
                "hours": 3,
                "rating": 5
            },
            {
                "name": "Kanha Sweets",
                "email": "kanha@amritsarescue.org",
                "phone_tag": "0183-2224095",
                "title": "Fluffy Puri Chole & Sweet Petha Halwa Combos",
                "description": "18 breakfast meal sets of piping hot puffed puris, spiced Amritsari chole, sweet pumpkin lauki launji, and rich suji halwa.",
                "location": "Lawrence Road, Joshi Colony, Dayanand Nagar, Amritsar, Punjab 143001",
                "cost_type": "Free",
                "hours": 8,
                "rating": 5
            },
            {
                "name": "Brothers' Dhaba",
                "email": "brothers@amritsarescue.org",
                "phone_tag": "0183-2545905",
                "title": "Shahi Paneer Thali with Jeera Rice & Phulkas",
                "description": "16 wholesome vegetarian thali meals with rich cottage cheese in tomato cashew gravy, yellow tadka dal, fragrant jeera rice, and 4 phulkas.",
                "location": "Town Hall, Katra Ahluwalia, Amritsar, Punjab 143006",
                "cost_type": "Free",
                "hours": 9,
                "rating": 4
            },
            {
                "name": "Kulcha Land",
                "email": "kulchaland@amritsarescue.org",
                "phone_tag": "0183-2500055",
                "title": "Assorted Paneer & Gobhi Chur-Chur Kulchas",
                "description": "14 boxes of hand-crushed crispy tandoori kulchas filled with cottage cheese, spiced cauliflower, and dollops of fresh white butter.",
                "location": "Ranjit Avenue, B-Block, Ground Floor, Amritsar, Punjab 143001",
                "cost_type": "Free",
                "hours": 11,
                "rating": 5
            },
            {
                "name": "Gian Chand Lassi Wale",
                "email": "gianchand@amritsarescue.org",
                "phone_tag": "0183-2540982",
                "title": "Thick Malai Peda Sweet Lassi Pack",
                "description": "30 chilled bottles of thick traditional sweet curd lassi topped with saffron clotted malai and crumbled peda. High nutrition refreshing packs.",
                "location": "Gali Rajpura, Katra Ahluwalia, Near Golden Temple, Amritsar, Punjab 143006",
                "cost_type": "Free",
                "hours": 14,
                "rating": 5
            },
            {
                "name": "Gurdas Ram Jalebi Wale",
                "email": "gurdasram@amritsarescue.org",
                "phone_tag": "0183-2548812",
                "title": "Hot Desi Ghee Jalebi & Rabri Boxes",
                "description": "8 kg of freshly fried thin, crunchy pretzel jalebis soaked in cardamom sugar syrup, paired with containers of thick reduced rabri.",
                "location": "Katra Ahluwalia, Main Bazaar, Amritsar, Punjab 143006",
                "cost_type": "Free",
                "hours": 10,
                "rating": 5
            },
            {
                "name": "Sharma Sweets",
                "email": "sharma@amritsarescue.org",
                "phone_tag": "0183-2223847",
                "title": "Khoya Gulab Jamun & Spiced Bun Chana",
                "description": "20 food packs containing steamed spiced bun chana and 2 large hot khoya gulab jamuns in fragrant rose-cardamom syrup.",
                "location": "Lawrence Road, Opp. BBK DAV College, Amritsar, Punjab 143001",
                "cost_type": "Free",
                "hours": 16,
                "rating": 5
            },
            {
                "name": "Ahuja Milk Centre",
                "email": "ahuja@amritsarescue.org",
                "phone_tag": "0183-2553194",
                "title": "Kesar Badam Kheer & Firni Clay Pots",
                "description": "24 earthenware matkas of chilled slow-simmered basmati rice pudding infused with pure Kashmiri saffron and sliced almonds.",
                "location": "Near Hindu Sabha College, Dhab Khatikan, Amritsar, Punjab 143001",
                "cost_type": "Free",
                "hours": 18,
                "rating": 5
            },
            {
                "name": "Brijwasi Chat Bhandar",
                "email": "brijwasi@amritsarescue.org",
                "phone_tag": "0183-2227183",
                "title": "Crispy Aloo Tikki & Papdi Chaat Boxes",
                "description": "20 platters of crispy pan-fried spiced potato patties topped with sweet tamarind chutney, chilled mint curd, and crunchy sev.",
                "location": "Cooper Road, Sadar Bazaar, Near Bhandari Bridge, Amritsar, Punjab 143001",
                "cost_type": "Free",
                "hours": 5,
                "rating": 4
            },
            {
                "name": "Crystal Restaurant",
                "email": "crystal@amritsarescue.org",
                "phone_tag": "0183-2229999",
                "title": "Royal Mughlai Veg Biryani & Dal Bukhara",
                "description": "12 buffet surplus containers of fragrant long-grain Dum Biryani with vegetable raita, and slow-cooked black lentils in creamy tomato reduction.",
                "location": "Crystal Chowk, Queens Road, INA Colony, Amritsar, Punjab 143001",
                "cost_type": "Discounted",
                "hours": 15,
                "rating": 5
            },
            {
                "name": "Surjit Food Plaza",
                "email": "surjit@amritsarescue.org",
                "phone_tag": "0183-2223845",
                "title": "Tandoori Chicken Tikka & Mutton Seekh Kebabs",
                "description": "15 assorted kebab boxes with charcoal-grilled spiced chicken breast tikka, succulent minced mutton seekh, and flaky tandoori parathas.",
                "location": "Nehru Shopping Complex, Lawrence Road, Amritsar, Punjab 143001",
                "cost_type": "Discounted",
                "hours": 6,
                "rating": 5
            },
            {
                "name": "Charming Chicken",
                "email": "charming@amritsarescue.org",
                "phone_tag": "0183-2401664",
                "title": "Desi Ghee Roast Chicken & Tawa Gravy Boxes",
                "description": "10 full chicken portions roasted in pure desi ghee with crushed coriander seeds, fenugreek leaves, and rich onion-tomato masala gravy.",
                "location": "Majitha Road, Green Avenue, Amritsar, Punjab 143001",
                "cost_type": "Discounted",
                "hours": 8,
                "rating": 4
            },
            {
                "name": "Novelty Sweets & Restaurant",
                "email": "novelty@amritsarescue.org",
                "phone_tag": "0183-2564200",
                "title": "Dal Makhani, Missi Roti & Amritsari Pinni Box",
                "description": "14 dinner sets including signature black dal, gram flour missi rotis, and boxes of nutritional whole wheat & dry-fruit pinni laddoos.",
                "location": "Novelty Chowk, Mall Road, Joshi Colony, Amritsar, Punjab 143001",
                "cost_type": "Free",
                "hours": 24,
                "rating": 5
            },
            {
                "name": "Pehalwan Kulcha Shop",
                "email": "pehalwan@amritsarescue.org",
                "phone_tag": "0183-2551022",
                "title": "Crispy 7-Layer Onion & Cauliflower Kulchas",
                "description": "20 oven-fresh Amritsari layered kulchas made with pure wheat dough, crunchy onions, ajwain spices, and tangy pomegranate seed chutney.",
                "location": "Lakshmansar Road, Chattiwind Gate, Amritsar, Punjab 143001",
                "cost_type": "Free",
                "hours": 4,
                "rating": 5
            },
            {
                "name": "Bubby Fish & Chicken Corner",
                "email": "bubby@amritsarescue.org",
                "phone_tag": "0183-2228833",
                "title": "Tawa Boneless Fish Gravy & Jeera Rice Packs",
                "description": "12 meal boxes of pan-seared river sole fish cooked on a cast iron tawa with ginger juliennes and served alongside steamed jeera rice.",
                "location": "Crystal Chowk, Cooper Road, Court Road, Amritsar, Punjab 143001",
                "cost_type": "Discounted",
                "hours": 7,
                "rating": 4
            },
            {
                "name": "Pal Da Dhaba",
                "email": "paldadhaba@amritsarescue.org",
                "phone_tag": "0183-2541982",
                "title": "Traditional Keema Kaleji & Tandoori Rotis",
                "description": "10 rich servings of slow-braised spiced minced mutton and liver with hot whole wheat tandoori rotis and sliced green chilies.",
                "location": "Hathi Gate, Katra Dulo, Old City, Amritsar, Punjab 143001",
                "cost_type": "Discounted",
                "hours": 5,
                "rating": 5
            },
            {
                "name": "Haveli Amritsar",
                "email": "haveli@amritsarescue.org",
                "phone_tag": "0183-5011111",
                "title": "Grand Punjabi Royal Thali (Saag, Makki Roti & Paneer)",
                "description": "15 banquet meal sets with Sarson Da Saag, golden Makki Di Roti, white butter, Kadai Paneer, and organic Jaggery (Gur).",
                "location": "GT Road, Amritsar Bypass, Near Khalsa College, Amritsar, Punjab 143002",
                "cost_type": "Free",
                "hours": 20,
                "rating": 5
            },
            {
                "name": "Giani Tea Stall",
                "email": "gianitea@amritsarescue.org",
                "phone_tag": "0183-2221234",
                "title": "Hot Masala Chai Thermos & Spiced Kachoris",
                "description": "35 evening snack packs with crisp flaky lentil kachoris, potato subzi, and fresh hot ginger-cardamom tea.",
                "location": "Cooper Road, Near Bhandari Bridge, Sadar Bazaar, Amritsar, Punjab 143001",
                "cost_type": "Free",
                "hours": 12,
                "rating": 5
            }
        ]

        print(f"Adding {len(restaurants_data)} Amritsar restaurants and food listings...")

        added_foods = []
        for index, item in enumerate(restaurants_data):
            # Create or update Donor User
            donor = User.query.filter_by(email=item["email"]).first()
            if not donor:
                donor = User(name=item["name"], email=item["email"], password=default_pwd, role="donor")
                db.session.add(donor)
                db.session.flush()
            else:
                donor.name = item["name"]

            # Compute expiry timestamp
            expiry_dt = now + timedelta(hours=item["hours"], minutes=15)
            expiry_str = expiry_dt.strftime("%Y-%m-%dT%H:%M")

            status = "Available"
            # Set 2 items to "Requested" to showcase the request workflow
            if index in [2, 7]:
                status = "Requested"

            # Assign image file
            image_name = f"food_{index + 1}.jpg"

            food = Food(
                title=item["title"],
                description=item["description"],
                location=item["location"],
                donor_id=donor.id,
                status=status,
                expiry_date=expiry_str,
                cost_type=item["cost_type"],
                image_file=image_name,
                created_at=now - timedelta(hours=2)
            )
            db.session.add(food)
            db.session.flush()
            added_foods.append((food, donor, item["rating"], status))

        db.session.commit()

        # Add ratings & requests
        print("Generating ratings and sample requests...")
        for food, donor, score, status in added_foods:
            # Add rating from Jagriti
            rating = Rating(donor_id=donor.id, receiver_id=jagriti.id, score=score, created_at=now - timedelta(days=1))
            db.session.add(rating)

            # If status is Requested, link a Request from Jagriti
            if status == "Requested":
                req = Request(receiver_id=jagriti.id, food_id=food.id)
                db.session.add(req)

        # Save a few favorites for Jagriti
        for food, donor, score, status in added_foods[:4]:
            jagriti.saved_foods.append(food)

        db.session.commit()
        print(f"Successfully seeded {len(restaurants_data)} restaurants and food listings for Amritsar!")

if __name__ == "__main__":
    seed_database()
