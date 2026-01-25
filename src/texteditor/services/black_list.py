import \
    os
import json
import \
    re


def black_list_load(*, black_list: str, white_list: str):

    temp = []

    if not os.path.exists(
            "../../../data/black_list.json"):
        with open(
                "../../../data/black_list.json", "w") as outfile:
            json.dump([],outfile)


    with open(
            "../../../data/black_list.json", "r") as read_file:
        temp = json.load(read_file)

    for item in temp:
        if item["black_list"] == black_list:
            return False

    id = len(temp)

    item = {"id": id, "black_list": black_list, "white_list": white_list}

    temp.append(item)

    json_object = json.dumps(temp, indent=4, sort_keys=True, ensure_ascii=False)

    with open(
            "../../../data/black_list.json", "w") as outfile:
        outfile.write(json_object)

    return True

    for tems in temp:
        print(tems)

def black_list_item_delete(id):
    with open(
            "../../../data/black_list.json", "r") as read_file:
        temp = json.load(read_file)
    temp.pop(id)
    json_object = json.dumps(temp, indent=4, sort_keys=True, ensure_ascii=False)
    with open(
            "../../../data/black_list.json", "w") as outfile:
        outfile.write(json_object)

def get_black_list_items():
    if not os.path.exists(
            "../../../data/black_list.json"):
        return []
    with open(
            "../../../data/black_list.json", "r") as read_file:
        temp = json.load(read_file)
    return temp

def refresh_black_list():
    refreshed_list = [('id:' + str(item['id']) +
                       ': (' + str(item['black_list']) +
                       ') -> (' + str(item['white_list'] + ')'))
                      for item in get_black_list_items()]
    return refreshed_list

def accept_black_list(text: str, cbx: bool, el: bool):
    white_text = text
    for item in get_black_list_items():
        if item['black_list'] in text:
            white_text = white_text.replace(item['black_list'], item['white_list'])

    if cbx:
        lines = white_text.split('\n')
        lines = [line.lstrip() for line in lines]
        white_text = '\n'.join(lines)

    if el:
        white_text = re.sub(r'\n\s*\n+', '\n\n', white_text)

    return white_text