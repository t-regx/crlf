# CRLF - tool to convert file line-endings

## Getting started

### Run as module

```sh
python -m crlf --help
```

### Setup and install

```sh
pip -r requirements/requirements.txt
python setup.py install
crlf --help
```

### Running automatic tests

Run all tests

```sh
pytest 
```

Run the fast tests

```sh
pytest -m memory    # only in-memory tests 
```

Run the slower tests

```sh
pytest -m process   # only sub-process tests 
```

Be incredibly intelligent

```sh
pytest --slow-last  # run in-memory tests first, then sub-process later
```

### Frequently asked questions

- Should I run `-m memory` or `-m process` tests?

    - It doesn't really matter, both run exactly the same suite of tests.
      The framework supplies the actual execution implementation using polymorphism,
      so the tests run incredibly similar.
