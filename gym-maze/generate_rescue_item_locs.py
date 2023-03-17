import random
import pickle

maze_size = 10
all_items = []
for i in range(500):
    riddle_types = ["server", "cipher", "pcap", "captcha"]
    random.shuffle(riddle_types)
    rescue_items_dict = {}

    for riddle_type in riddle_types:
        position = (
            random.randrange(0, maze_size - 1),
            random.randrange(0, maze_size - 1),
        )
        while position == (0, 0) or position == (9, 9) or position in rescue_items_dict:
            position = (
                random.randrange(0, maze_size - 1),
                random.randrange(0, maze_size - 1),
            )
        rescue_items_dict[position] = riddle_type
    all_items.append(rescue_items_dict)
pickle.dump(all_items, open("maze_gen_rescue_items.p", "wb"))
