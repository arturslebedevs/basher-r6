import random

def weighted_random_message(base_messages, extra_messages, base_weight=3, extra_weight=1):
    pool = base_messages * base_weight + extra_messages * extra_weight
    return random.choice(pool)