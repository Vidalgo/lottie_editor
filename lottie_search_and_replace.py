import json


def load_json(file_name):
    file = open(file_name)
    json_obj = json.load(file)
    return json_obj


def store_json(file_name, data):
    # with open(file_name, 'w', encoding='utf-8') as outfile:
    #    json.dump(data, outfile, ensure_ascii=False, indent=4)
    with open(file_name, 'w') as outfile:
        json.dump(data, outfile)


def is_list_or_dic(obj):
    if type(obj) is dict:
        return True
    elif type(obj) is list:
        return True
    return False


def is_dic(obj):
    if type(obj) is dict:
        return True
    return False


def is_obj_dic_or_list(obj):
    if type(obj) is dict:
        return True
    if type(obj) is list:
        if not obj:
            return False
        elif type(obj[0]) is dict:
            return True
    return False


def get_value(obj, key):
    if type(obj) is dict:
        return obj[key]
    elif type(obj) is list:
        return obj[obj.index(key)]
    else:
        return obj


def find_object_in_lottie(lottie_obj, key_obj):
    return find_and_replace_object_in_lottie(lottie_obj, key_obj, False, False)


def replace_object_in_lottie(lottie_obj, key_obj, replace_obj):
    return find_and_replace_object_in_lottie(lottie_obj, key_obj, False, replace_obj)


def find_parent_object_in_lottie(lottie_obj, key_obj):
    return find_and_replace_object_in_lottie(lottie_obj, key_obj, True, False)


def replace_parent_object_in_lottie(lottie_obj, key_obj, replace_obj):
    find_and_replace_object_in_lottie(lottie_obj, key_obj, True, replace_obj)


def func_on_object_in_lottie(lottie_obj, key_obj, func):
    return find_and_replace_object_in_lottie(lottie_obj, key_obj, False, False, func)


def func_on_parent_object_in_lottie(lottie_obj, key_obj, func):
    return find_and_replace_object_in_lottie(lottie_obj, key_obj, True, False, func)


def find_and_replace_object_in_lottie(lottie_obj, key_obj, find_parent=False, replace_obj=False, func=False,
                                      parent_obj=None):
    if not is_obj_dic_or_list(lottie_obj):
        return False
    first_dic_object_key = list(key_obj[0].keys())[0]
    first_dic_object_value = list(key_obj[0].values())[0]
    # look for the first key in the lottie object
    if first_dic_object_key in lottie_obj:
        # Key found! Compare also the value when required.
        # This is when the user looks for both key='name' and value='john'
        if not first_dic_object_value or first_dic_object_value == lottie_obj[first_dic_object_key]:
            # If requested, execute function on object
            if func:
                if func[0]:
                    if find_parent is True:
                        func[0](lottie_obj)
                    else:
                        func[0](lottie_obj[first_dic_object_key])
                func.pop(0)
            # A single key is remaining (the comparison to the previous keys was successful or this is the only key)
            if len(key_obj) == 1:
                # Replace operation is required or just find
                if replace_obj is not False:
                    # Replace parent is required or replace of the direct object
                    if find_parent is True:
                        parent_object_key = list(parent_obj)[0]
                        parent_obj[parent_object_key] = replace_obj
                        return lottie_obj
                    else:
                        lottie_obj[first_dic_object_key] = replace_obj
                        return lottie_obj[first_dic_object_key]
                else:
                    if find_parent is True:
                        return lottie_obj
                    else:
                        return lottie_obj[first_dic_object_key]
            # The comparison of the current key was successful but there are more keys to compare to.
            # Continue searching with the next keys
            else:
                key_obj.pop(0)
                ret = find_and_replace_object_in_lottie(lottie_obj[first_dic_object_key], key_obj, find_parent,
                                                        replace_obj, func, lottie_obj)
                if ret is not False:
                    return ret
    # Key (or key:value) not found in the current dictionary level.
    # Continue searching in lower levels for each dictionary object.
    for lottie_input_key in reversed(lottie_obj):
        lottie_input_value = get_value(lottie_obj, lottie_input_key)
        # Note that the search will continue for objects that are dictionaries or lists and not for simple value nodes
        # (e.g. ints, strings)
        if type(lottie_input_value) is dict or type(lottie_input_value) is list:
            ret = find_and_replace_object_in_lottie(lottie_input_value, key_obj, find_parent, replace_obj, func,
                                                    lottie_obj)
            # When the search succeeds a valid value is returned
            if ret is not False:
                return ret
    # Search failed in all objects at the current level
    return False


def remove_image_assets_from_lottie(lottie_obj):
    assets_obj = find_object_in_lottie(lottie_obj, 'assets')
    # A simple remove of a specific asset (image)
    if assets_obj is not False:
        index = 0
        while index < len(assets_obj):
            # Image assets have a "p" or "e" keys within
            if "p" in assets_obj[index] or "e" in assets_obj[index]:
                assets_obj.remove(assets_obj[index])
            else:
                index = index + 1
        lottie_obj['assets'] = assets_obj
        return lottie_obj


def restore_image_assets_to_lottie(lottie_source_obj, lottie_dest_obj):
    assets_source_obj = find_object_in_lottie(lottie_source_obj, 'assets')
    assets_dest_obj = find_object_in_lottie(lottie_dest_obj, 'assets')
    # A simple restore of a specific asset (image)
    if assets_source_obj is not False:
        index = 0
        for obj in assets_source_obj:
            # Image assets have a "p" or "e" keys within
            if "p" in obj or "e" in obj:
                assets_dest_obj.insert(index, obj)
                index = index + 1
        lottie_dest_obj['assets'] = assets_dest_obj
        return lottie_dest_obj


# version 2.0
def find_assets(lottie_obj, asset_id='images'):
    assets = {}
    try:
        assets_obj = lottie_obj["assets"]
        if not assets_obj:
            return {}
    except:
        raise Exception(f"Error:could not parse JSON file for assets")

    for asset in assets_obj:
        if asset_id == 'images' and "e" in asset:
            try:
                assets['image:' + str(asset["id"])] = asset
            except:
                raise Exception(f"Error:could not parse JSON file image asset {asset}")
    return assets


# version 2.0
def find_main_layers(lottie_obj):
    layers = {}

    try:
        layers_obj = lottie_obj["layers"]
        key = "layers:"
    except:
        raise Exception(f"Error:could not find layers in json file")

    for layer in layers_obj:
        try:
            layers[key + str(layer["ind"])] = layer
        except:
            raise Exception(f"Error:could not parse JSON file {layer}")
    return layers


# version 3.0
def find_pre_comp_layers(lottie_obj):
    layers = {}
    try:
        assets_obj = lottie_obj["assets"]
        if not assets_obj:
            return {}
    except:
        raise Exception(f"Error:could not parse JSON file for assets")
    for pre_comp in assets_obj:
        if "e" not in pre_comp and 'layers' in pre_comp:
            for layer in pre_comp['layers']:
                try:
                    if 'ind' in layer:
                        layer_id = layer['ind']
                    else:
                        layer_id = 'no_id'
                    layers[str(pre_comp['id']) + ':' + str(layer_id)] = layer
                except:
                    raise Exception(f'Error:could not parse JSON file pre composition assets {layer}')

    return layers


# version 2.0
def find_pre_comp(lottie_obj):
    pre_comp = {}
    try:
        assets_obj = lottie_obj["assets"]
        if not assets_obj:
            return {}
    except:
        raise Exception(f"Error:could not parse JSON file for assets")
    for asset in assets_obj:
        if "e" not in asset:
            try:
                pre_comp[asset['id']] = asset
            except:
                raise Exception(f"Error:could not parse JSON file pre composition assets {asset}")

    return pre_comp


# version 2.0
def replace_layer(lottie_obj, layer_id, new_layer_obj, composition_id='layers'):
    try:
        if composition_id == "layers" and "layers" in lottie_obj and lottie_obj["layers"]:
            search_and_replace_obj = lottie_obj["layers"]
        elif "assets" in lottie_obj and lottie_obj["assets"]:
            for pre_comp in lottie_obj["assets"]:
                if "e" not in pre_comp and "id" in pre_comp and pre_comp["id"] == composition_id:
                    search_and_replace_obj = pre_comp["layers"]
                    break
            else:
                return False
        else:
            return False

        for index, layer in enumerate(search_and_replace_obj):
            if layer['ind'] == layer_id:
                search_and_replace_obj[index] = new_layer_obj
                return lottie_obj

        return False
    except:
        raise Exception("Faulty Lottie object")


# version 2.0
def replace_asset(lottie_obj, asset_id, new_asset_obj, asset_key='images'):
    try:
        if asset_key == "images" and "assets" in lottie_obj and lottie_obj["assets"]:
            search_and_replace_obj = lottie_obj["assets"]
            key = "id"
        else:
            return False

        for index, layer in enumerate(search_and_replace_obj):
            if layer[key] == asset_id:
                search_and_replace_obj[index] = new_asset_obj
                return lottie_obj

        return False
    except:
        raise Exception("Faulty Lottie object")


# version 2.0
def add_layer(lottie_obj, layer_obj, composition_id='layers', order='last', layer_id=''):
    try:
        if composition_id == "layers" and "layers" in lottie_obj and lottie_obj["layers"]:
            search_and_replace_obj = lottie_obj["layers"]
        elif "assets" in lottie_obj and lottie_obj["assets"]:
            for pre_comp in lottie_obj["assets"]:
                if "e" not in pre_comp and pre_comp["id"] == composition_id:
                    search_and_replace_obj = pre_comp["layers"]
                    break
            else:
                return False
        else:
            return False

        if order == 'first':
            search_and_replace_obj.insert(0, layer_obj)
            return lottie_obj
        elif order == 'last':
            search_and_replace_obj.append(layer_obj)
            return lottie_obj
        else:
            for index, layer in enumerate(search_and_replace_obj):
                if layer["ind"] == layer_id:
                    if order == 'before':
                        search_and_replace_obj.insert(index, layer_obj)
                        return lottie_obj
                    elif order == 'after':
                        search_and_replace_obj.insert(index + 1, layer_obj)
                        return lottie_obj
                    else:
                        return False

        return False
    except:
        raise Exception("Faulty Lottie object")


# version 2.0
def add_asset(lottie_obj, asset_obj, asset_key='images', order='last', layer_id=''):
    try:
        if asset_key == "images" and "assets" in lottie_obj and lottie_obj["assets"]:
            search_and_replace_obj = lottie_obj["assets"]
            key = "id"
        else:
            return False

        if order == 'first':
            search_and_replace_obj.insert(0, asset_obj)
            return lottie_obj
        elif order == 'last':
            search_and_replace_obj.append(asset_obj)
            return lottie_obj
        else:
            for index, layer in enumerate(search_and_replace_obj):
                if layer[key] == layer_id:
                    if order == 'before':
                        search_and_replace_obj.insert(index, asset_obj)
                        return lottie_obj
                    elif order == 'after':
                        search_and_replace_obj.insert(index + 1, asset_obj)
                        return lottie_obj
                    else:
                        return False

        return False
    except:
        raise Exception("Faulty Lottie object")


# version 3.0
def flatten_tuple(data):
    if isinstance(data, tuple):
        for x in data:
            yield from flatten_tuple(x)
    else:
        yield data


'''lottie = load_json('Merry Christmas from Vidalgo doggie.json')
layers = find_main_layers(lottie)
images = find_assets(lottie)
pre_comp_layers = find_pre_comp_layers(lottie)
pre_comp = find_pre_comp(lottie)
print(layers.keys())
print(images.keys())
print(pre_comp_layers.keys())
print(pre_comp.keys())

layers.update(pre_comp_layers)
print(layers.keys())


null_layer = {"nm": "NULL LAYER",
              "ty": 3,
              "ind": 99999,
              "ks": {"a": {"a": 0,"k": [0, 0, 0],"ix": 1},"o":{"a": 0,"k": 0,"ix": 11},"p": {"a": 0,"k": [0, 0, 0],"ix": 2},
                     "r": {"a": 0,"k": 0,"ix": 10},"s": {"a": 0,"k": [100, 100, 100],"ix": 6}}}
image_layer = {"e": 1,"h": 1000,"w": 1000,"p":"data:image/png;base64,ABCD1234","u": "","id": "image_9999"}

new_lottie = replace_asset(lottie, "image_0", image_layer)
new_lottie = replace_asset(new_lottie, "image_5", image_layer)
new_lottie = replace_asset(new_lottie, "image_9", image_layer)

new_lottie = replace_layer(new_lottie, 1, null_layer, "comp_0")
new_lottie = replace_layer(new_lottie, 2, null_layer, "comp_1")
new_lottie = replace_layer(new_lottie, 2, null_layer, "comp_2")
new_lottie = replace_layer(new_lottie, 3, null_layer, "comp_6")

new_lottie = replace_layer(new_lottie, 1, null_layer)
new_lottie = replace_layer(new_lottie, 18419, null_layer)

another_null_layer = {"nm": "NULL LAYER",
              "ty": 3,
              "ind": 11111,
              "ks": {"a": {"a": 0,"k": [0, 0, 0],"ix": 1},"o":{"a": 0,"k": 0,"ix": 11},"p": {"a": 0,"k": [0, 0, 0],"ix": 2},
                     "r": {"a": 0,"k": 0,"ix": 10},"s": {"a": 0,"k": [100, 100, 100],"ix": 6}}}
another_image_layer = {"e": 1,"h": 1000,"w": 1000,"p":"data:image/png;base64,ABCD1234","u": "","id": "image_11111"}

new_lottie = add_asset(new_lottie, another_image_layer)
new_lottie = add_asset(new_lottie, another_image_layer, order='first')
new_lottie = add_asset(new_lottie, another_image_layer, order='before', layer_id="image_9999")
new_lottie = add_asset(new_lottie, another_image_layer, order='after', layer_id="image_9999")

new_lottie = add_layer(new_lottie, another_null_layer, "comp_0")
new_lottie = add_layer(new_lottie, another_null_layer, "comp_1", order='first')
new_lottie = add_layer(new_lottie, another_null_layer, "comp_2", order='before', layer_id=99999)
new_lottie = add_layer(new_lottie, another_null_layer, "comp_6", order='after', layer_id=99999)

new_lottie = add_layer(new_lottie, another_null_layer)
new_lottie = add_layer(new_lottie, another_null_layer, order='after', layer_id=99999)'''

''' key = input("Enter a value to find or 'exit' to finish - ")
    while key != 'exit':
        value = find_object_in_lottie(lottie, key)
        if value is not False:
            print(f'key {key} found with value {value}\n')
        else:
            print('key not found\n')
        key = input("Enter a value to find or 'exit' to finish - ")'''
