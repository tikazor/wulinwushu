import psycopg2
conn = psycopg2.connect(
    dbname="wulin",
    user="wulinuser",
    password="TestWushu2025",
    host="localhost"
)
print("Connexion OK")
