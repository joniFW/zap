import typer
import sqlite3

# import sqlalchemy as sa
import subprocess
import os

app = typer.Typer()


@app.command()
def hello(name: str):
    print(f"Hello {name} from zap!")


@app.command()
def goodbye(name: str, formal: bool = False):
    if formal:
        print(f"Goodbye Ms. {name}. Have a good day.")
    else:
        print(f"Bye {name}")


create_filtered_table = """
            CREATE TABLE filtered AS
            SELECT titles.tconst, titleType, primaryTitle, startYear,
                   runtimeMinutes, genres, averageRating, numVotes
            FROM titles
            JOIN ratings ON ratings.tconst = titles.tconst
            WHERE isAdult = 0 AND titleType = 'movie'
                  AND averageRating > 5 AND numVotes > 100;"""

sql_code = []

if __name__ == "__main__":
    if not os.path.isfile("assets/database/movies.db"):
        subprocess.call(
            [
                "sqlite3",
                "assets/database/movies.db",
                ".mode ascii",
                ".separator '\t' '\n'",
                ".import assets/dataset/title.basics.tsv titles",
                ".import assets/dataset/title.ratings.tsv ratings",
            ]
        )
    with sqlite3.connect("assets/database/movies.db") as conn:
        cursor = conn.cursor()
        # check if filtered table exists in the database, else create it
        if not cursor.execute(
            """SELECT name FROM sqlite_master
                    WHERE type='table' AND name='filtered';"""
        ).fetchall():
            cursor.execute(create_filtered_table)
        for command in sql_code:
            cursor.execute(command)
        conn.commit()
