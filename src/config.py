def get_environmental_variable(variable: str, default: str | None = None):
    with open(".env") as env:
        for line in env:
            line = line.split("=")
            if line[0] == variable:
                return line[1].strip().strip('"')
    return default


ENVIRONMENT = get_environmental_variable("ENVIRONMENT", "").capitalize()
DEBUG = get_environmental_variable("DEBUG", "True").capitalize() == "True"
DATABASE_CLIENT = get_environmental_variable("DATABASE_CLIENT").lower()
if DATABASE_CLIENT is None:
    raise ValueError("DAtABASE NOT DEFINED!!")
DATABASE_USERNAME = get_environmental_variable("DATABASE_USERNAME")
DATABASE_PASSWORD = get_environmental_variable("DATABASE_PASSWORD")
DATABASE = get_environmental_variable("DATABASE")
DATABASE_PORT = int(get_environmental_variable("DATABASE_PORT"))
DATABASE_HOST = get_environmental_variable("DATABASE_HOST", "localhost")


if __name__ == "__main__":
    pass
