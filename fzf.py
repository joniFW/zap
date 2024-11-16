import sys
import subprocess
import enum


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


def main():
    choice, _ = pipe_into_fzf(list(MainMenuOptions), prompt="Select an option below: ")

    match choice:
        case MainMenuOptions.QUICK_SEARCH:
            # Do a sql search for both movies and series
            print(f"You selected '{choice}'")
        case MainMenuOptions.MOVIES:
            # Do a sql search for movies
            print(f"You selected '{choice}'")
        case MainMenuOptions.SERIES:
            # Do a sql search for series
            print(f"You selected '{choice}'")
        case MainMenuOptions.EXPLORE:
            # This would allow you to browse the database with more control, out of scope for now...
            print(f"You selected '{choice}'")
        case "":
            print("Nothing selected, good bye!")
            sys.exit(0)
        case _:
            raise ValueError(f"'{choice}' is not a valid main menu entry!")


if __name__ == "__main__":
    main()
