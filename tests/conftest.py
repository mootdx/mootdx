import pandas


def is_empty(obj):
    if isinstance(obj, pandas.DataFrame):
        return obj.empty

    return not bool(obj)
