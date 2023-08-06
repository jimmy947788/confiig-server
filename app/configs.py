import os


DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./potatoes.db")

print(f"DATABASE_URL={DATABASE_URL}")