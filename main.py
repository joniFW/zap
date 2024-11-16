import os
import sqlite3
import subprocess
import sys


def log(msg: str) -> None:
    # TODO: Add rich logging in the future
    print(msg)


def bootstrap_database():
    # TODO: Check that directory structure is provided
    # TODO: Check that TSV files exist
    # TODO: Use pathlib for this

    if not os.path.isfile("assets/database/movies.db"):
        log("Setting up DB...")
        subprocess.run(
            [
                "sqlite3",
                "assets/database/movies.db",
                ".mode ascii",
                ".separator '\t' '\n'",
                ".import assets/dataset/title.basics.tsv titles",
                ".import assets/dataset/title.ratings.tsv ratings",
            ],
            check=True,
            stdout=sys.stdout,
            stderr=sys.stderr,
        )

    create_filtered_table()


def create_filtered_table():
    create_filtered_table_sql = """
            CREATE TABLE filtered AS 
            SELECT titles.tconst, titleType, primaryTitle, startYear,
                   runtimeMinutes, genres, averageRating, numVotes
            FROM titles
            JOIN ratings ON ratings.tconst = titles.tconst
            WHERE isAdult = 0 AND titleType = 'movie'
                  AND averageRating > 5 AND numVotes > 100;"""

    log("Connecting to DB...")
    with sqlite3.connect("assets/database/movies.db") as conn:
        cursor = conn.cursor()
        # check if filtered table exists in the database, else create it
        if not cursor.execute(
            """SELECT name FROM sqlite_master
               WHERE type='table' AND name='filtered';"""
        ).fetchall():
            cursor.execute(create_filtered_table_sql)
        conn.commit()


if __name__ == "__main__":
    bootstrap_database()
