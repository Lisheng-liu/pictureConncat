import random

for i in range(3):
    print(i)

def getRandomSet(bits):
    num_set = [chr(i) for i in range(48, 58)]
    char_set = [chr(i) for i in range(97, 123)]
    total_set = num_set + char_set
    value_set = "".join(random.sample(total_set, bits))
    return value_set

print(getRandomSet(18).upper())