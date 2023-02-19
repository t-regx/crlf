# CRLF - cli tool to edit text files line endings

## Installation

```bash
pip install -r requirements/requirements.txt
python setup.py install
crlf --help
```

## Overview

Tool `crlf` can be used to change line endings to CRLF or LF of a single file, all files in a directory
or all nested directories (with option `-R`).

### Standard options

Show help message and options
```bash
crlf --help
crlf -h
```

Perform dry-run - inspect how the files would change, without actually modifying files:
```bash
crlf --dry-run  # no files will be changed
```

Suppress output - display only summary:
```bash
crlf --quiet  # display only summary
crlf -q
```

Suppress complete output - display nothing:
```bash
crlf --silent
crlf -s
```

Show version:
```bash
crlf --version
crlf -V         # uppercase "V"
```

### Change line endings

Change file line endings:

```bash
crlf ./file.txt --to crlf   # change line endings of "file.txt" to CRLF
crlf ./file.txt --to lf
```


Change line endings of files in directory:

```bash
crlf directory/ --to crlf   # change line endings of all files in "directory" to CRLF
crlf directory/ --to lf
```


Change line endings of files in directory and its nested directories

```bash
crlf -R directory/ --to crlf   # change line endings of all nested files in "directory" to CRLF
crlf -R directory/ --to lf
```

## Example execution

Example of standard execution:
```bash
crlf . --to crlf
```
```
Updated: .gitignore
Updated: CONTRIBUTING.md
Failed:  file.txt
         ^ ! expected text file in unicode encoding, failed to parse file
Updated: ReadMe.md
Updated: setup.py
Ignored: version
         ^ file already has CRLF line endings
Updated: version.py
Done. Updated: 5 files, ignored: 1 files, failed to read: 1 files.
```

Example of quiet execution:
```bash
crlf . --to crlf --quiet
```
```
Done. Updated: 5 files, ignored: 1 files, failed to read: 1 files.
```
