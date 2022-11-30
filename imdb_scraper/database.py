"""
Database file for running non-pipeline queries.
"""
import mysql.connector as connector


def insert_genres(connection, cursor):
    """
    Insert listed genres into the genres table.
    """
    genres = [
        ['action', 0],
        ['adventure',1],
        ['animation', 2],
        ['biography', 3],
        ['comedy', 4],
        ['crime', 5],
        ['documentary', 6],
        ['drama', 7],
        ['family', 8],
        ['fantasy', 9],
        ['film-noir', 10],
        ['game-show', 11],
        ['history', 12],
        ['horror', 13],
        ['music', 14],
        ['musical', 15],
        ['mystery', 16],
        ['news', 17],
        ['reality-tv', 18],
        ['romance', 19],
        ['sci-fi', 20],
        ['sport', 21],
        ['talk-show', 22],
        ['thriller', 23],
        ['war', 24],
        ['western', 25]
    ]

    for genre in genres:
        if cursor.execute("""
            SELECT COUNT(*) FROM `genres` WHERE `name` = %s
        """, (
            genre[0],
        )) == 0:
            print("Inserting genre: %s" % genre[0])
            cursor.execute("""
                INSERT INTO `genres` (`name`, `ordering`) VALUES (%s, %s)
            """, (
                genre[0],
                genre[1],
            ))

            connection.commit()


def get_genres():
    """
    Get all genres from the database by name in order.
    :return:
    """
    # Create connection to the database.
    conn = connector.connect(
        host='127.0.0.1',
        user='root',
        password='',
        database='imdb_scraper'
    )

    # Create a cursor for executing commands.
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM `genres` ORDER BY `ordering`
    """)

    genres = cursor.fetchall()
    cursor.close()
    conn.close()

    return genres


def get_default_genre():
    """
    Get the default genre: 'sci-fi'.
    :return:
    """
    # Create connection to the database.
    conn = connector.connect(
        host='127.0.0.1',
        user='root',
        password='',
        database='imdb_scraper'
    )

    # Create a cursor for executing commands.
    cursor = conn.cursor()

    default = 'sci-fi'
    cursor.execute("""
            SELECT * FROM `genres` WHERE `name` = %s
        """, (
        default,
    ))

    genre = cursor.fetchone()
    cursor.close()
    conn.close()

    return genre
