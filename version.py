def get_and_increment():
    try:
        with open('version', 'r+') as file:
            version = int(file.read()) + 1
            file.seek(0)
            file.write(str(version))
            return version
    except FileNotFoundError:
        with open('version', 'w') as file:
            file.write("1")
        return 1
