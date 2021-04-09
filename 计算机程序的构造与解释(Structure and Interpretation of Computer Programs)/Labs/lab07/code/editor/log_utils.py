counter = 0


def get_id():
    global counter
    counter += 1
    return str(counter)
