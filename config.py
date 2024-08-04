def get_environmental_variable(variable: str, default: str | None = None):
    with open(".env") as env:
        for line in env:
            line = line.split("=")
            if line[0] == variable:
                return line[1]
    return default


ENVIRONMENT = get_environmental_variable("ENVIRONMENT", "").capitalize()
DEBUG = get_environmental_variable("DEBUG", "True").capitalize() == "True"
DATABASE = get_environmental_variable("DATABASE").lower()
if DATABASE is None:
    raise ValueError("DAtABASE NOT DEFINED!!")
DATABASE_USERNAME = get_environmental_variable("DATABASE_USERNAME")
DATABASE_PASSWORD = get_environmental_variable("DATABASE_PASSWORD")


if __name__ == "__main__":
    pass