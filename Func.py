import json
import os

def test(program):
    main_text = program.TextWidget.get_general_text()
    program.TextBoxResult1.set_text(main_text)

def black_list_load(*, black_list: str, white_list: str):

    temp = []

    if not os.path.exists("black_list.json"):
        with open("black_list.json", "w") as outfile:
            json.dump([],outfile)


    with open("black_list.json", "r") as read_file:
        temp = json.load(read_file)

    for item in temp:
        if item["black_list"] == black_list:
            return False

    id = len(temp)

    item = {"id": id, "black_list": black_list, "white_list": white_list}

    temp.append(item)

    json_object = json.dumps(temp, indent=4, sort_keys=True, ensure_ascii=False)

    with open("black_list.json", "w") as outfile:
        outfile.write(json_object)

    return True

    for tems in temp:
        print(tems)


def get_black_list_items():
    if not os.path.exists("black_list.json"):
        return []
    with open("black_list.json", "r") as read_file:
        temp = json.load(read_file)
    return temp


