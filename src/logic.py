from model import Dog

def create_dog(db, path, contact, status):
    dog = Dog(path=path,
              contact=contact,
              status=status
    )
    db.add(dog)
    db.commit()
    db.refresh(dog)
    return dog

def get_dog(db, dog_id):
    return db.query(Dog).filter(Dog.id == dog_id).first()

def update_status(db, dog_id, new_status):
    dog = get_dog(db, dog_id)
    if dog:
        dog.status = new_status
        db.commit()
        return dog

