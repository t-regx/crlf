def error(message: str) -> str:
    return "usage: crlf [-h] [-V] [-q | -s] [-d] [-R] --to {crlf,lf} filename" + f"""
crlf: error: {message}
"""


def summary(updated: int = 0, ignored: int = 0, failed: int = 0, dryrun: bool = False) -> str:
    return append_dryrun(
        f'Done. Updated: {updated} files, ignored: {ignored} files, failed to read: {failed} files.\n',
        dryrun)


def updated(filenames: list[str], dryrun: bool = False) -> str:
    return append_dryrun(
        ''.join([f"Updated: {filename}\n" for filename in filenames]) + summary(updated=len(filenames)),
        dryrun)


def ignored(filenames: list[str], destination: str, dryrun: bool = False) -> str:
    return append_dryrun(
        ''.join([_ignored(filename, destination) for filename in filenames]) + summary(ignored=len(filenames)),
        dryrun)


def failed(filenames: list[str], dryrun: bool = False) -> str:
    return append_dryrun(
        ''.join([_failed(filename) for filename in filenames]) + summary(failed=len(filenames)),
        dryrun)


def _ignored(filename: str, destination: str) -> str:
    return f"""Ignored: {filename}
         ^ file already has {destination.upper()} line endings
"""


def _failed(filename: str) -> str:
    return f"""Failed:  {filename}
         ^ ! expected text file in unicode encoding, failed to parse file
"""


def append_dryrun(content: str, dryrun: bool) -> str:
    if dryrun:
        return content + "Executed in dry mode, no files were actually modified.\n"
    return content
