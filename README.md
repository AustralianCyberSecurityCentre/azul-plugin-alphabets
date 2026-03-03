# Azul Plugin Alphabets

Finds alphabet character runs for possible encoding schemes.
Handles non-standard ordering of characters, as seen in some malware families.

Supported encodings:

- base32
- base64
- base85

## Development Installation

To install azul-plugin-alphabets for development run the command
(from the root directory of this project):

```bash
pip install -e .
```

## Usage: azul-alphabet-finder

Features found alphabets.

Usage on local files:

```
azul-alphabets test.exe
```

Example Output:

```
----- Alphabets results -----
OK

Output features:
        b64_alphabet: ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/
  b64_alphabet_count: 1

Feature key:
  b64_alphabet:  Possible base64 alphabet
  b64_alphabet_count:  Count of possible base64 alphabets
```

Automated usage in system:

```
azul-alphabet-finder --server http://azul-dispatcher.localnet/
```

## Python Package management

This python package is managed using a `pyproject.toml` file.

Standardisation of installing and testing the python package is handled through tox.
Tox commands include:

```bash
# Run all standard tox actions
tox
# Run linting only
tox -e style
# Run tests only
tox -e test
```

## Dependency management

Dependencies are managed in the pyproject.toml and debian.txt file.

Version pinning is achieved using the `uv.lock` file.

To add new dependencies it's recommended to use uv with the command `uv add <new-package>`
    or for a dev package `uv add --dev <new-dev-package>`

The tool used for linting and managing styling is `ruff` and it is configured via `pyproject.toml`

The debian.txt file manages the debian dependencies that need to be installed on development systems and docker images.

Sometimes the debian.txt file is insufficient and in this case the Dockerfile may need to be modified directly to
install complex dependencies.