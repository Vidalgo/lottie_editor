import random
import string
import json
import enum

VIDALGO_ID = 'cl'
ID_SUFFIX = '_'
SYMBOLS = string.ascii_letters + string.digits + string.punctuation


'''def generate_random_id(lottie_obj: dict):
    if lottie_obj is not None:
        lottie_obj[VIDALGO_ID] = ''.join(random.choice(SYMBOLS) for i in range(12))'''


def store_json(file_name, data):
    # with open(file_name, 'w', encoding='utf-8') as outfile:
    #    json.dump(data, outfile, ensure_ascii=False, indent=4)
    with open(file_name, 'w') as outfile:
        json.dump(data, outfile, indent=2)


def update_intersected_ids(list_obj_1: list, list_obj_2: list, suffix: str = ID_SUFFIX):
    def update(obj):
        obj.lottie_element_id += suffix

    obj_a = {obj1.lottie_element_id for obj1 in list_obj_1 if obj1.lottie_element_id is not None}
    obj_b = {obj2.lottie_element_id for obj2 in list_obj_2 if obj2.lottie_element_id is not None}
    intersection = obj_a.intersection(obj_b)
    if len(intersection) != 0:
        [update(obj) for obj in list_obj_1 if obj.lottie_element_id is not None and obj.lottie_element_id in intersection]
        return list(intersection)
    return None


