import sqlite3, os, csv
from flask import request, flash

def initDB():
    if not os.path.exists('data/databases.db'):
        print "Creating database..."
        db = sqlite3.connect("data/databases.db")
        c = db.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS users (user TEXT, pass TEXT, PRIMARY KEY(user))")
        c.execute("CREATE TABLE IF NOT EXISTS pokemon_by_rarity (id INT, name TEXT, rarity INT)")
        with open("data/pokemon_rarity.csv", "rU") as rarity_csv_file:
            next(rarity_csv_file)
            csvreader = csv.reader(rarity_csv_file)
            for row in csvreader:
                print "INSERT INTO pokemon_by_rarity VALUES(%s,'%s',%s)" % (row[0], row[1], row[2])
                c.execute("INSERT INTO pokemon_by_rarity VALUES(%s,\"%s\",%s)" % (row[0], row[1], row[2]))
        db.commit()
        db.close()
        print "Created database"

#add username and password to database
def addUser(user, pazz ):
    db = sqlite3.connect("data/databases.db")
    c = db.cursor()
    c.execute("INSERT INTO users VALUES(?,?)", (user,pazz))
    db.commit()
    db.close()

def getUsers():
    db = sqlite3.connect("data/databases.db")
    c = db.cursor()
    a = 'SELECT user, pass FROM users'
    x = c.execute(a)
    users = {}
    for line in x:
        users[line[0]] = line[1]
    db.close()
    return users

def getPokemonWithRarity(rarity):
    db = sqlite3.connect("data/databases.db")
    c = db.cursor()
    pokemon_list = c.execute("SELECT id FROM pokemon_by_rarity WHERE rarity = %d ORDER BY RANDOM() LIMIT 1" % rarity)
    return pokemon_list.fetchone()
