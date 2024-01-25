from typing import OrderedDict


def normalize_fk_serializer_data(representation_data: OrderedDict):
    # Nested key value Data from serializer
    # to be normalized to a list of dictionaries format
    data = []
    for item in list(representation_data):
        data.append(dict(list(dict(item).values())[0]))
    return data
