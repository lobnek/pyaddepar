import pandas as pd
from csv import reader


def parse(frame, dates=[], numbers=[], index=None):
    """
    taken a bare DataFrame convert columns into dates or numbers
    :param frame: Pandas DataFrame
    :param dates: Names of columns that shall be converted into dates
    :param numbers: Names of columns that shall be converted into floats
    :param index: Name(s) of the columns that shall be the index

    :return:
    """
    for key in dates:
        frame[key] = pd.to_datetime(frame[key], errors="coerce", exact=True, format="%m/%d/%Y").apply(lambda x: x.date())

    for key in numbers:
        frame[key] = pd.to_numeric(frame[key], errors="ignore")

    if index:
        return frame.set_index(index)
    else:
        return frame


def request2frame(request):
    rows = [a.decode() for a in request]
    assert len(rows) >= 1
    # parse them into lists of strings, note that a comma between " " double-quotes is ignored
    # compare with http://tinyurl.com/gn7kmvu
    lines = [line for line in reader(rows)]
    return pd.DataFrame(columns=lines[0], data=lines[1:])