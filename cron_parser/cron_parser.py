import sys

data_parsed = {}


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


def process_values(requested_input, value_type):

    options = {
        "minutes": (0, 60),
        "hours": (0, 24),
        "dom": (1, 32),
        "month": (1, 13),
        "dow": (0, 7),
    }
    if value_type in options:
        x = options[value_type][0]
        y = options[value_type][1]
    print(x)
    print(y)

    value = ""
    if requested_input == "*":
        print("*")
        for n in range(x, y):
            if value:
                value = value + " " + str(n)
            else:
                value = str(n)
    elif "/" in requested_input:
        print("/")
        start_repeat = requested_input.split("/")
        if start_repeat[0] == "*":
            n = 0
        else:
            n = int(start_repeat[0])
        while n < y:
            if value:
                value = value + " " + str(n)
            else:
                value = str(n)
            n = n + int(start_repeat[1])
    elif "," in requested_input:
        print(",")
        start_repeat = requested_input.split(",")
        for n in start_repeat:
            if value:
                value = value + " " + str(n)
            else:
                value = str(n)
    else:
        print("Single value")
        value = requested_input

    return value


def main(inputs):
    if len(inputs) < 2:
        help()
        return 1

    split_inputs = inputs[1].split()

    minutes_value = process_values(split_inputs[0], "minutes")
    data_parsed["minute"] = minutes_value

    hours_value = process_values(split_inputs[1], "hours")
    data_parsed["hours"] = hours_value

    dom_value = process_values(split_inputs[2], "dom")
    data_parsed["day of month"] = dom_value

    month_value = process_values(split_inputs[3], "month")
    data_parsed["month"] = month_value

    dow_value = process_values(split_inputs[4], "dow")
    data_parsed["day of week"] = dow_value

    data_parsed["command"] = split_inputs[5]

    return data_parsed


if __name__ == "__main__":
    parsed = main(sys.argv)
    for k in parsed:
        print(f"{k} {parsed[k]:13}")
