import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(ROOT_DIR, "data")
BLACK_LIST_FILE = os.path.join(DATA_DIR, "black_list.json")