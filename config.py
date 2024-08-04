def get_environmental_variable(variable: str, default: str):
    with open(".env") as env:
        for line in env:
            if line.split("="):
                pass


if __name__ == "__main__":
    pass