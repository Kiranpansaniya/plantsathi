from database import SessionLocal, Plant

db = SessionLocal()

existing = db.query(Plant).count()

if existing == 0:
    Plants = [
        Plant(name = "Aloe Vera", category = "Succulent", price = 149.0, stock = 20, description = "Easy to grow,medicinal plant", image_url =""),
        Plant(name = "Tulsi", category = "Herb", price = 99.0, stock = 30, description = "Holy basil, used in pooja and health remedies", image_url = ""),
        Plant(name = "Money Plant", category = "Indoor", price = 199.0, stock = 15, description = "Believed to bring good luck ", image_url = ""),
        Plant(name = "Snake Plant", category = "Indoor", price = 249.0, stock = 10, description = "Low maintenance, purifies air ", image_url = ""),
    ]

    db.add_all(Plants)
    db.commit()

    print(f"{len (Plants)} plants added")
else:
    print("Data already exists.")

db.close()