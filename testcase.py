from build import InputObject

import random

num_testcase = 10000

list_stop = InputObject.read_stop()
list_stop_id = InputObject.compress_stop_id(list_stop)
len_stop = len(list_stop_id)

with open("test.txt", 'w') as f:
    f.write(f"{num_testcase}\n")
    for i in range(num_testcase):
        a = random.randint(0, len_stop-1)
        b = random.randint(0, len_stop-1)
        f.write(f"{list_stop_id[a]} {list_stop_id[b]}\n")
