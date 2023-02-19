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
        ''.join([_updated(filename) for filename in filenames]) + summary(updated=len(filenames)),
        dryrun)


def ignored(filenames: list[str], destination: str, dryrun: bool = False) -> str:
    return append_dryrun(
        ''.join([_ignored(filename, destination) for filename in filenames]) + summary(ignored=len(filenames)),
        dryrun)


def restricted(filenames: list[str], dryrun: bool = False) -> str:
    return append_dryrun(
        ''.join([_restricted(filename) for filename in filenames]) + summary(failed=len(filenames)),
        dryrun)


def failed(filenames: list[str], dryrun: bool = False) -> str:
    return append_dryrun(
        ''.join([_failed(filename) for filename in filenames]) + summary(failed=len(filenames)),
        dryrun)


def _updated(filename: str) -> str:
    return f"Updated: {filename}\n"


def _ignored(filename: str, destination: str) -> str:
    return _format('Ignored:', filename, f'^ file already has {destination.upper()} line endings')


def _failed(filename: str) -> str:
    return _format('Failed:', filename, '^ ! expected text file in unicode encoding, failed to parse file')


def _restricted(filename: str) -> str:
    return _format('Failed:', filename, '^ insufficient permissions to open file')


def _format(type: str, filename: str, message: str) -> str:
    return type.ljust(9) + filename + "\n" + ' ' * 9 + message + "\n"


def append_dryrun(content: str, dryrun: bool) -> str:
    if dryrun:
        return content + "Executed in dry mode, no files were actually modified.\n"
    return content
