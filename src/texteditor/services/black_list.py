import \
    os
import json
import \
    re
from ..config import \
    BLACK_LIST_FILE, \
    DATA_DIR

def black_list_load(*, black_list: str, white_list: str):
    black_list = black_list.strip()

    if not black_list:
        return "black list item is empty"

    try:
        os.makedirs(DATA_DIR, exist_ok=True)
    except OSError:
        return "mkdir error"

    temp = []

    try:
        if not os.path.exists(
                BLACK_LIST_FILE):
            with open(
                    BLACK_LIST_FILE, "w") as outfile:
                json.dump([],outfile)
    except OSError:
        return "create json error"

    try:
        with open(
                BLACK_LIST_FILE, "r") as read_file:
            temp = json.load(read_file)

        for item in temp:
            if item["black_list"] == black_list:
                return False

        id = len(temp)

        item = {"id": id, "black_list": black_list, "white_list": white_list}

        temp.append(item)

        json_object = json.dumps(temp, indent=4, sort_keys=True, ensure_ascii=False)

        with open(
                BLACK_LIST_FILE, "w") as outfile:
            outfile.write(json_object)
    except (OSError, json.JSONDecodeError, KeyError):
        return "write json error"

    return True

def black_list_item_delete(id):
    try:
        with open(
                BLACK_LIST_FILE, "r") as read_file:
            temp = json.load(read_file)
        if id < 0 or id >= len(temp):
            return "item not found"
        temp.pop(id)
        json_object = json.dumps(temp, indent=4, sort_keys=True, ensure_ascii=False)
        with open(
                BLACK_LIST_FILE, "w") as outfile:
            outfile.write(json_object)
    except (OSError, json.JSONDecodeError):
        return "write json error"
    return True

def get_black_list_items():
    try:
        if not os.path.exists(
                BLACK_LIST_FILE):
            return []
        with open(
                BLACK_LIST_FILE, "r") as read_file:
            temp = json.load(read_file)
        return temp
    except (OSError, json.JSONDecodeError):
        return []

def refresh_black_list():
    try:
        refreshed_list = [('id:' + str(item['id']) +
                           ': (' + str(item['black_list']) +
                           ') -> (' + str(item['white_list'] + ')'))
                          for item in get_black_list_items()]
        return refreshed_list
    except KeyError:
        return []

def accept_black_list(text: str, cbx: bool, el: bool):
    try:
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
    except (KeyError, TypeError):
        return "error"
