def read_constants():
    constants = {}
    with open("CONSTANTS.txt", "r") as file:
        for line in file:
            line = line.strip()
            if not line or "=" not in line:  # Skip empty lines
                continue
            key, value = line.split("=")
            if "," in value:  # Convert color values to tuples
                constants[key] = tuple(map(int, value.split(",")))
            else:
                constants[key] = int(value)

    return constants