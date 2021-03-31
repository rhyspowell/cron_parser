import sys, errno


def help():
    print(
        """
    Expected input follows

    cron_parser.py "<minute> <hour> <day of month> <month> <day of week> <command>"

    cron is expected to follow the cron standard without special item spans
    see https://en.wikipedia.org/wiki/Cron

    please wrap the cron script in \" as different shells behave differently
    """
    )


def create_value_string(value, n):
    if value:
        value = value + " " + str(n)
    else:
        value = str(n)

    return value


def process_values(requested_input, value_type):

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
    try:
        if requested_input == "*":
            for n in range(x, y):
                value = create_value_string(value, n)
        elif "/" in requested_input:
            start_repeat = requested_input.split("/")
            if start_repeat[0] == "*":
                n = 0
            else:
                n = int(start_repeat[0])
            while n < y:
                value = create_value_string(value, n)
                n = n + int(start_repeat[1])
        elif "," in requested_input:
            start_repeat = requested_input.split(",")
            for n in start_repeat:
                value = create_value_string(value, n)
        elif "-" in requested_input:
            start_repeat = requested_input.split("-")
            if int(start_repeat[1]) > y:
                print("Warning incorrect value for range " + start_repeat[1])
                start_repeat[1] = y
            full_range = range(int(start_repeat[0]), int(start_repeat[1])+1)
            for n in full_range:
                value = create_value_string(value, n)
        elif requested_input in range(x, y):
            value = requested_input
        else:
            raise ValueError("Input does not match patterns")
            
        return value
    except ValueError as error:
        print(error)
        print("Please confirm your cron information is correct")
        help()
        sys.exit(errno.EACCES)


def main(inputs):
    if len(inputs) < 2:
        help()
        sys.exit("Input missing")

    data_parsed = {}

    split_inputs = inputs[1].split()
    if len(split_inputs) != 6:
        help()
        sys.exit("cron construction not right")
    
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
