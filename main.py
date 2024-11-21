import enum
import pathlib
import sqlite3
import subprocess
import sys
from typing import Literal

# TODO: print nice errors instead of python exceptions (do this when we're 40)

# TODO: make assets dir configurable via env var
# TODO: replace CWD later by some configurable localtion (probably in HOME by default)
ASSETS_DIR = pathlib.Path.cwd() / "assets"
DB_FILE = pathlib.Path.cwd() / ".zap.db"
TSV_TITLES = ASSETS_DIR / "title.basics.tsv"
TSV_RATINGS = ASSETS_DIR / "title.ratings.tsv"


# TODO: look at type hints in newer python versions
def log(msg: str, level: Literal["info", "debug"] = "info") -> None:
    # TODO: Add rich logging and different logging levels in the future
    if level not in ["info", "debug"]:
        raise ValueError(f"Unsupported logging level: {level}")

    print(msg)


def bootstrap_database():
    if not all([TSV_TITLES.exists(), TSV_RATINGS.exists()]):
        raise FileNotFoundError(
            f"Couldn't find TSV files ['{TSV_TITLES}', '{TSV_RATINGS}'] in '{ASSETS_DIR}'."
        )

    if not DB_FILE.exists():
        log("Setting up DB...")
        # TODO: Add some user logging or print some jokes...
        subprocess.run(
            [
                "sqlite3",
                f"{DB_FILE}",
                ".mode ascii",
                ".separator '\t' '\n'",
                f".import {TSV_TITLES} titles",
                f".import {TSV_RATINGS} ratings",
            ],
            check=True,
            stdout=sys.stdout,
            stderr=sys.stderr,
        )
        # TODO: add error handling for failed DB creation

        log("Created DB successfully...")

    log(f"Found DB at {DB_FILE}")
    create_titles_with_rating_table()


def create_titles_with_rating_table():
    # TODO: create table definition with correct column types
    table_sql_create = """
            CREATE TABLE titles_with_rating AS
            SELECT titles.tconst, titleType, primaryTitle, startYear,
                   runtimeMinutes, genres,
                   CAST(averageRating AS DECIMAL(3,1)) AS averageRating,
                   CAST(numVotes AS INT) AS numVotes
            FROM titles
            JOIN ratings ON ratings.tconst = titles.tconst
            WHERE isAdult = 0 AND titleType = 'movie';"""
    # TODO: consider filtering for smaller database (can happen later, let's use all for now)
    # AND averageRating > 5 AND numVotes > 100;"""
    # TODO: at some point consider what originalTitle and primaryTitle mean (we
    # would like the english version)

    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        # check if filtered table exists in the database, else create it
        if not cursor.execute(
            """SELECT name FROM sqlite_master
            WHERE type='table' AND name='titles_with_rating';"""
        ).fetchall():
            log("Creating some DB tables..")
            cursor.execute(table_sql_create)
        else:
            log("Database tables exist!", "debug")

        conn.commit()


def quick_search() -> None:
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        sql_query = "SELECT primaryTitle FROM titles_with_rating;"
        cursor.execute(sql_query)
        rows = [row[0] for row in cursor.fetchall()]

        name, _ = pipe_into_fzf(rows)

        title_query = f"SELECT * FROM titles_with_rating WHERE primaryTitle='{name}';"
        cursor.execute(title_query)
        _, _, title, year, mins, genre, rating, votes = cursor.fetchone()
        # TODO: figure out if line wrap is possible in fzf
        out = (
            f"{title} ({year}), {mins} minutes; "
            f"Rating: {rating}/10 with {votes} votes; "
            f"Genre(s): {genre.replace(',', ', ')}"
        )
        pipe_into_fzf([out])


class MainMenuOptions(str, enum.Enum):
    QUICK_SEARCH = "Quick Search"
    MOVIES = "Movies"
    SERIES = "Series"
    EXPLORE = "Explore"


def pipe_into_fzf(lines: list[str], prompt: str = "") -> tuple[str, str]:
    fzf_proc = subprocess.Popen(
        ["fzf", "--reverse", "--prompt", prompt],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    stdout, stderr = fzf_proc.communicate(input="\n".join(lines))

    return stdout.rstrip(), stderr.rstrip()


def main_menu():
    choice, _ = pipe_into_fzf(list(MainMenuOptions), prompt="Select an option below: ")

    match choice:
        case MainMenuOptions.QUICK_SEARCH:
            quick_search()
            log(f"You selected '{choice}'")
        case MainMenuOptions.MOVIES:
            # Do a sql search for movies
            log(f"You selected '{choice}'")
        case MainMenuOptions.SERIES:
            # Do a sql search for series
            log(f"You selected '{choice}'")
        case MainMenuOptions.EXPLORE:
            # This would allow you to browse the database with more control, out of scope for now...
            log(f"You selected '{choice}'")
        case "":
            log("Nothing selected, good bye!")
            sys.exit(0)
        case _:
            raise ValueError(f"'{choice}' is not a valid main menu entry!")


def main():
    bootstrap_database()
    main_menu()


if __name__ == "__main__":
    main()
