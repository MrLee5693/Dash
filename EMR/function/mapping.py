from collections.abc import Callable

"""
def text_contain(row, container):
    return row["Name2"] in container or row["Name3"] in container

def generate_mapping_function(mapping_dict, contain=text_contain):

    def mapping_function(row):
        for key, set in mapping_dict.items():
            if contain(row, set):
                return key
        return "Unknown"
    return mapping_function

"""

def generate_mapping_function(row,mapping_dict):
    for key, value in mapping_dict.items():
        if row["Name2"] in value:
            return key
        elif row["Name3"] in value:
            return key
        else:
            continue
    return "Unknown"
            


   
if __name__ == "__main__":
    mapping_dict = get_breed_dict()
