from pathlib import Path
import re
from typing import List


def read_csv(path_to_file: str, sep: str = ",") -> List:
    resulting_list = []
    path = Path(path_to_file)
    if not path.is_file():
        print("Error, such file doesn't exist")
        return resulting_list
    with path.open() as file:
        for line in file:
            resulting_list.append(
                [
                    i.strip().replace('"', "")
                    for i in re.split("""%s(?=(?:[^'"]|'[^']*'|"[^"]*")*$)""" % sep, line)
                ]
            )
    return resulting_list


def write_csv(path_to_file: str, data: List, sep: str = ",") -> None:
    path = Path(path_to_file)
    if not path.parent.exists():
        print("Error, directory doesn't exist")
        return
    data_to_w = [sep.join(i) + "\n" for i in data]
    with path.open("w") as file:
        file.writelines(data_to_w)


print(read_csv("/Users/mikhaillebedev/study/python/data.csv", ";"))
d = read_csv("/Users/mikhaillebedev/study/python/data.csv", ";")
print(write_csv("/Users/mikhaillebedev/study/python/keka/data_out.csv", d, ","))
