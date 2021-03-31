import sys


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
    """Just process value to string cleanly"""
    if value:
        value = value + " " + str(n)
    else:
        value = str(n)

    return value


def process_values(requested_input, value_type):
    """
    core processing of the data supplied

    map the range of values for each of the options

    process the variance of each option following std cron formatting
    so the range of numbers are accepted along with the special characters
    "*", "-", "/"

    tries to fix incorrect entries, will still return a warning, if not errors out
    """

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
        #simple glob catch
        if requested_input == "*":
            for n in range(x, y):
                value = create_value_string(value, n)
        
        #manage span
        elif "/" in requested_input:
            start_repeat = requested_input.split("/")
            if start_repeat[0] == "*":
                n = x
            elif int(start_repeat[0]) < x:
                print("Warning incorrect value for range " + start_repeat[0])
                n = x
            else:
                n = int(start_repeat[0])
            while n < y:
                value = create_value_string(value, n)
                n = n + int(start_repeat[1])
        
        #manage the list options
        elif "," in requested_input:
            start_repeat = requested_input.split(",")
            for n in start_repeat:
                value = create_value_string(value, n)

        #manage the range options. Check that the ranges fit
        elif "-" in requested_input:
            start_repeat = requested_input.split("-")
            if int(start_repeat[0]) < x:
                print("Warning incorrect value for range " + start_repeat[0])
                start_repeat[0] = x
            if int(start_repeat[1]) > y:
                print("Warning incorrect value for range " + start_repeat[1])
                #This has a -1 because we add one on full range to suit everything else
                start_repeat[1] = y - 1
            full_range = range(int(start_repeat[0]), int(start_repeat[1]) + 1)
            for n in full_range:
                value = create_value_string(value, n)
        
        #check single ints are within the required range
        elif int(requested_input) in range(x, y):
            value = requested_input

        #if we don't match raise a value error
        else:
            raise ValueError("Input does not match patterns")

        return value

    #this exception means that all bad characters get thrown out
    except ValueError as error:
        print(error)
        print("Please confirm your cron information is correct")
        help()
        sys.exit(error)


def main(inputs):
    """
    Takes a cron entry and returns the infomation on when it will run and the command called

    Will warn and fix if the values are out of bounds of the numbers allowed.

    If a sensible choice cant be made the program fails out

    Any failure displays the help text to assist with problem resolution

    """
    inputs = inputs.split()
    data_parsed = {}

    # safety check that all info is there
    if len(inputs) != 6:
        help()
        sys.exit("cron construction not right")

    #Map the inputs to the values they should represent
    split_names = {
        "minutes": inputs[0],
        "hours": inputs[1],
        "day of month": inputs[2],
        "month": inputs[3],
        "day of week": inputs[4],
    }

    #pass the data for processing
    for key in split_names:
        processed_value = process_values(split_names[key], key)
        data_parsed[key] = processed_value

    #Not mapped as its a straight return value
    data_parsed["command"] = inputs[5]

    return data_parsed


if __name__ == "__main__":
    if len(sys.argv) < 2:
        help()
        sys.exit("Input missing")
    parsed = main(sys.argv[1])
    for k in parsed:
        print(f"{k:13} {parsed[k]}")
