def error(message: str) -> str:
    return f"""usage: crlf [-h] [-V] [-R] filename
crlf: error: {message}
"""
