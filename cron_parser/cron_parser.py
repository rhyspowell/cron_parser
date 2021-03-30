import sys


def help():
    print(
        """
    Expected input follows

    cron_parser.py "<minute> <hour> <day of month> <month> <day of week> <command>"

    cron is expected to follow the cron standard without special item spans
    see https://en.wikipedia.org/wiki/Cron

    please wrap the cron script in \" as diffrent shells behave differently
    """
    )


def create_value_string(value, n):
    if value:
        value = value + " " + str(n)
    else:
        value = str(n)

    return value


def process_values(requested_input, value_type):
    print(requested_input)
    print(value_type)

    options = {
        "minutes": (0, 60),
        "hours": (0, 24),
        "day of month": (1, 32),
        "month": (1, 13),
        "day of week": (0, 7),
    }
    if value_type in options:
        x = options[value_type][0]
        y = options[value_type][1]

    value = ""
    if requested_input == "*":
        print("*")
        for n in range(x, y):
            value = create_value_string(value, n)
    elif "/" in requested_input:
        print("/")
        start_repeat = requested_input.split("/")
        if start_repeat[0] == "*":
            n = 0
        else:
            n = int(start_repeat[0])
        while n < y:
            value = create_value_string(value, n)
            n = n + int(start_repeat[1])
    elif "," in requested_input:
        print(",")
        start_repeat = requested_input.split(",")
        for n in start_repeat:
            value = create_value_string(value, n)
    else:
        print("Single value")
        value = requested_input

    return value


def main(inputs):
    if len(inputs) < 2:
        help()
        return 1

    data_parsed = {}

    split_inputs = inputs[1].split()
    split_names = {
        "minutes": split_inputs[0],
        "hours": split_inputs[1],
        "day of month": split_inputs[2],
        "month": split_inputs[3],
        "day of week": split_inputs[4],
    }

    for key in split_names:
        processed_value = process_values(split_names[key], key)
        data_parsed[key] = processed_value

    data_parsed["command"] = split_inputs[5]

    return data_parsed


if __name__ == "__main__":
    parsed = main(sys.argv)
    for k in parsed:
        print(f"{k} {parsed[k]:13}")
