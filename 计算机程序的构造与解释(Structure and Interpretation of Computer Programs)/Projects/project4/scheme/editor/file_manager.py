import os


def get_scm_files():
    files = filter(lambda x: x.lower().endswith(".scm"), os.listdir(os.curdir))
    return sorted(files)


def save(code, filename):
    with open(filename, "w+") as file:
        file.truncate(0)
        file.seek(0)
        file.write("\n".join(code))
        file.flush()


def read_file(filename):
    with open(filename, "r") as file:
        return "".join([x for x in file])


def new_file(filename):
    if filename + ".scm" in get_scm_files():
        return False
    open(filename + ".scm", "w")
    return True
