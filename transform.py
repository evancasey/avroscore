def pluck(records, arg):
    return map(lambda x: x[arg], records)

def size(records):
    return len(records)

def first(records):
    if len(records) != 0:
        return records[0]
    else:
        return None


