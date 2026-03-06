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

## Usage: azul-plugin-alphabets

Features found alphabets.

Usage on local files:

```
azul-plugin-alphabets test.exe
```

Example Output:

```
----- AzulPluginAlphabets results -----
COMPLETED

events (1)

event for test.exe:None
  {}
  output features:
          b32_alphabet:  #$)034:;?ABCDFGJLNOQUVWY[\_cdei @ 0xb280b46 (offset)
                        =>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\ @ 0xb33371d (offset)
                        DEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abc @ 0xb071b30 (offset)
                        DEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abc @ 0xb073c30 (offset)
    b32_alphabet_count: 4
          b64_alphabet: ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+- @ 0xb073d28 (offset)
                        ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/ @ 0x79c4a40 (offset)
                        ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/ @ 0x7a59a60 (offset)
                        ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/ @ 0xb4bae20 (offset)
                        ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/ @ 0xb4d3e80 (offset)
                        ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_ @ 0xb3b6ba0 (offset)
                        ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_ @ 0xb3b74e0 (offset)
                        abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-. @ 0x75bde68 (offset)
    b64_alphabet_count: 8

Feature key:
  b32_alphabet:  Possible base32 alphabet
  b32_alphabet_count:  Count of possible base32 alphabets
  b64_alphabet:  Possible base64 alphabet
  b64_alphabet_count:  Count of possible base64 alphabets
```

Automated usage in system:

```
azul-plugin-alphabets --server http://azul-dispatcher.localnet/
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