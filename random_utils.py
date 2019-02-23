from random import randint


def random_choice_index(chances):
    random_chance = randint(1, sum(chances))
    # print("random chance " + str(random_chance))
    running_sum = 0
    choice = 0
    for w in chances:
        running_sum += w

        if random_chance <= running_sum:
            return choice
        choice += 1


def random_choice_from_dict(choice_dict):
    choices = list(choice_dict.keys())
    # print('Choices ' + str(choices))
    chances = list(choice_dict.values())
    # print('Chances ' + str(chances))
    # print(choices[random_choice_index(chances)])
    return choices[random_choice_index(chances)]
