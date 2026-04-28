""" import statements """
import mysql.connector # to connect
from mysql.connector import errorcode

 
import dotenv # to use .env file
from dotenv import dotenv_values
#using our .env file
secrets = dotenv_values(".env")
 
""" database config object """
config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True #not in .env file
}
MySQL: mysql_test.py. Connection
try:
    """ try/catch block for handling potential MySQL database errors """ 
 
    db = mysql.connector.connect(**config) # connect to the movies database 

    # output the connection status
    print("\n  Database user {} connected to MySQL on host {} with database {}".format(config["user"], config["host"], config["database"]))

    def show_films():
        #joins data
        cursor = db.cursor()
        cursor.execute("SELECT film_name AS Name, film_director AS Director, genre_name AS Genre, studio_name AS 'Studio Name' FROM film \
                          INNER JOIN studio ON film.studio_id = studio.studio_id \
                          INNER JOIN genre ON film.genre_id = genre.genre_id")
        rows = cursor.fetchall()

        #changes Alien to a Horror Movie
        update_genre = "UPDATE film \
        SET genre_id = (SELECT genre_id FROM genre WHERE genre_name = 'Drama') \
        WHERE film_name = 'Alien';"
        cursor.execute(update_genre)
        db.commit()

        #Deletes Gladiator from the database
        delete_query = "DELETE FROM film \
        WHERE film_name = 'Gladiator';"
        cursor.execute(delete_query)
        db.commit()

        #adds Pitch Black to the database
        add_pitch = "INSERT INTO film(film_name, film_releaseDate, film_runtime, film_director, studio_id, genre_id) \
                                VALUES('Pitch Black', '2000', '108', 'David Twohy', (SELECT studio_id FROM studio WHERE studio_name = 'Universal Pictures'),(SELECT genre_id FROM genre WHERE genre_name = 'SciFi') );"
        cursor.execute(add_pitch)
        db.commit()
        db.close()
        #displays updated list
        print("-- DISPLAYING FILMS --")
        for row in rows:
            name, director, genre, studio = row
            print(f"Film Name: {name}")
            print(f"Director: {director}")
            print(f"Genre: {genre}")
            print(f"Studio: {studio}")
            print()
    show_films()
 
except mysql.connector.Error as err:
    """ on error code """
 
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("  The supplied username or password are invalid")
 
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("  The specified database does not exist")
 
    else:
        print(err)
 
finally:
    """ close the connection to MySQL """
 
