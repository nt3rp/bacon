# Bacon

A tool to find the shortest path between two actors.

## Project Setup

Setup is fairly standard for a python project. Most of the dependencies you
need should already be available (assuming you are using Python 2.7). I would
advise setting up a
[virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/),
though it is by no means necessary.

1. `pip install -r requirements.txt`

## Testing

Tests are implemented using Python's built-in
[`unittest` library](https://docs.python.org/2/library/unittest.html), and
code coverage metrics are obtained using the
[`coverage` library](http://nedbatchelder.com/code/coverage/)

### Unit Tests

1. `python tests.py`

### Coverage

1. `coverage run tests.py`
2. `coverage report -m`

## Usage

Contextual help is available via `python run.py --help` or
`python run.py <command> --help`, but there are two main commands:

1. `python run.py import [directory]`
    - Import JSON files from `[directory]`. Defaults to `./films`
    - Files are assumed to be of the following format
        `{'film': {'name': <name>}, 'cast': [{'name': <name>}, ...]`

2. `python run.py search actor [target_actor]`
    - Find the path of actors and movies from `actor` to `[target_actor]`. If
      `[target_actor]` is not specified, `Kevin Bacon` be used by default.

## License

```
DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                   Version 2, December 2004

Copyright (C) 2014 Nick Terwoord <me@nt3r.com>

Everyone is permitted to copy and distribute verbatim or modified
copies of this license document, and changing it is allowed as long
as the name is changed.

           DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
  TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

 0. You just DO WHAT THE FUCK YOU WANT TO.
```