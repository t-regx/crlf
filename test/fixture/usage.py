def error(message: str) -> str:
    return f"""usage: crlf [-h] [-V] [-q] [-R] filename
crlf: error: {message}
"""
