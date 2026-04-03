from model import Animal

def create_animal(db, path, contact, status):
    animal = Animal(path=path,
              contact=contact,
              status=status
    )
    db.add(animal)
    db.commit()
    db.refresh(animal)
    return animal

def get_animal(db, animal_id):
    return db.query(Animal).filter(Animal.id == animal_id).first()

def update_status(db, dog_id, new_status):
    animal = get_animal(db, animal_id)
    if animal:
        animal.status = new_status
        db.commit()
        return animal

