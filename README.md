# Zap


Zap is a command-line interface (CLI) tool designed for movie enthusiasts who want to easily browse and find films using fuzzy search over movie data.
With Zap, you can quickly locate movies based on partial titles, genres, or keywords, streamlining your movie discovery process.

## Dev installation

1. Install cargo (for uv):
[https://www.rust-lang.org/tools/install](https://www.rust-lang.org/tools/install)

2. Install uv: 
[https://docs.astral.sh/uv/getting-started/installation/](https://docs.astral.sh/uv/getting-started/installation/)

3. Clone the repository:
```bash
git clone https://github.com/alvarotroya/zap.git
```

4. Navigate to the project directory:
```bash
cd zap
```

5. Set up dev environment:
```bash
uv python install 3.12
uv venv
uv sync
source .venv/bin/activate
```

6. Install pre-commit hooks:
```bash
pre-commit install --hook-type pre-commit --hook-type pre-push
```
7. Install Typer

8. Run the main file:
```bash
python main.py
```
or
```bash
uv run main.py
```

To display display the `help` menu:
```bash
python main.py --help
```

You can learn more about typer here: [https://typer.tiangolo.com/](https://typer.tiangolo.com/)

## WARNING! All of the following text is ChatGPT garbage, this README is still work in progress. This will all be adapted.


## Features

- **Fuzzy Searching**: Find movies even with typos or partial titles.
- **Quick Access**: Fast retrieval of movie data from disk.
- **Simple Interface**: Easy-to-use command-line tool for effortless browsing.
- **Filter Options**: Search by genre, year, or other attributes.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/zap.git
```
2. Navigate to the project directory:
```bash
cd zap
```
3. Install the necessary dependencies:
```bash
pip install -r requirements.txt
```

## Usage

To start using Zap, run the following command in your terminal:

```bash
python zap.py [search_term]
```

### Example

```bash
python zap.py \"inception\"
```

This command will return a list of movies that match the search term \"inception.\"

## Contributing

Contributions are welcome! If you'd like to contribute to Zap, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgments

- Inspired by the need for a more efficient way to browse movies.

For any questions or feedback, please open an issue in the GitHub repository! Enjoy browsing with Zap!

