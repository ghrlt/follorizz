def getInteger(minimum: int=None, maximum: int=None) -> int:
    """Get an integer from the user.

    Args:
        minimum (int): Minimum value (inclusive)
        maximum (int): Maximum value (inclusive)

    Returns:
        int: The integer entered by the user
    """
    while True:
        try:
            num = int(input())
            if minimum is not None and num < minimum:
                print("Value must be at least {}".format(minimum))
            elif maximum is not None and num > maximum:
                print("Value must be at most {}".format(maximum))
            else:
                return num
        except ValueError:
            print("Value must be an integer")
