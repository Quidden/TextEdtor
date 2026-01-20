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

    id = len(temp)

    item = {"id": id, "black_list": black_list, "white_list": white_list}

    temp.append(item)

    json_object = json.dumps(temp, indent=4, sort_keys=True, ensure_ascii=False)

    with open("black_list.json", "w") as outfile:
        outfile.write(json_object)

    for tems in temp:
        print(tems)



black_list_load(black_list="123423sfdgsdfgsdfg", white_list="45a34242sd6")

