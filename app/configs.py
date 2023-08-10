import os

APP_NAME: str = os.getenv("APP_NAME", "myapp")
MYSQL_HOST: str = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT: int = int(os.getenv("MYSQL_PORT", 3306))
MYSQL_USER: str = os.getenv("MYSQL_USER", "guest")
MYSQL_PASS: str = os.getenv("MYSQL_PASSWORD", "guest")
MYSQL_DATABASE: str = os.getenv("MYSQL_DATABASE", "myapp")
DATABASE_URL: str = f"mysql://{MYSQL_USER}:{MYSQL_PASS}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"

print(f"DATABASE_URL={DATABASE_URL}")