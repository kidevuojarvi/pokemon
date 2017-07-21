INDEXDATA = []
MOVEDATA = []
TYPEDATA = []
NATUREDATA = []

def read_indexdata():
    if len(INDEXDATA) > 0:
        return
    try:
        file = open("indexdata.csv", "r", encoding="utf-8")
    except IOError:
        print("indexdata.csv not usable")
        return
    for row in file:
        row = row.rstrip().split(";")
        data = {}
        data["name"] = row[1]
        data["types"] = [row[2]]
        if row[3] != "None":
            data["types"].append(row[3])
        data["stats"] = list(map(int, row[4].split(",")))
        if row[5] == "None":
            data["evolve_level"] = None
        else:
            data["evolve_level"] = int(row[5])
        if row[6] == "None":
            data["evolution"] = None
        else:
            data["evolution"] = int(row[6])
        INDEXDATA.append(data)
    file.close()

def read_naturedata():
    """
    Stores data on pokemon natures into NATUREDATA-constant list.
    List format is List[name: str, plus: int, minus: int]
    :return: None
    """
    if len(NATUREDATA) > 0:
        return
    try:
        file = open("naturedata.csv", "r", encoding="utf-8")
    except IOError:
        print("naturedata.csv not usable")
        return
    for row in file:
        row = row.rstrip().split(",")
        row[0] = row[0].capitalize()
        row[1] = int(row[1])
        row[2] = int(row[2])
        NATUREDATA.append(row)
    file.close()

def read_movedata():
    if len(MOVEDATA) == 0:
        return

def read_typedata():
    if len(TYPEDATA) == 0:
        return

read_indexdata()
read_movedata()
read_typedata()
read_naturedata()
