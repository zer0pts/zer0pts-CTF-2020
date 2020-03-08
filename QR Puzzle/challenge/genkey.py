import random

n = 25 * 25
size = 25

output = ''
for i in range(n):
    x, y = random.randrange(size), random.randrange(size)
    choices = [0, 1, 2, 3]
    if x == 0: choices.remove(0)
    if x == size - 1: choices.remove(1)
    if y == 0: choices.remove(2)
    if y == size - 1: choices.remove(3)
    a = random.choice(choices)
    output += '{}#({},{})'.format(a, x, y)
    output += '\n'

print(output)
