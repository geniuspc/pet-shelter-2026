from src.database import engine, Base
from src.model import Animal, Location, Match

print("Створюємо таблиці в базі даних...")
Base.metadata.create_all(bind=engine)
print("Готово! Таблиці створені успішно. 🚀")