import random
import string
import enum

VIDALGO_ID = 'cl'
ID_SUFFIX = '_'
SYMBOLS = string.ascii_letters + string.digits + string.punctuation


def generate_random_id(lottie_obj: dict):
    if lottie_obj is not None:
        lottie_obj[VIDALGO_ID] = ''.join(random.choice(SYMBOLS) for i in range(12))

def update_intersected_ids(list_obj_1: list, list_obj_2: list, suffix: str = ID_SUFFIX):
    def update(obj):
        obj['id'] += suffix

    obj_a = {obj1["id"] for obj1 in list_obj_1 if "id" in obj1}
    obj_b = {obj2["id"] for obj2 in list_obj_2 if "id" in obj2}
    intersection = obj_a.intersection(obj_b)
    if len(intersection) != 0:
        [update(obj) for obj in list_obj_1 if "id" in obj and obj["id"] in intersection]
        return list(intersection)
    return None


