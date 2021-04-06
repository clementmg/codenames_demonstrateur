from AI.AI_3 import get_clue1
from AI.EmbeddingsAI import get_clue2
import time

# call all AI and return results
def AI_manager(word_to_guess, enemy_words, neutral, assassin):
    results = []
    results.append(timing(get_clue1, word_to_guess, enemy_words, neutral, assassin))
    results.append(timing(get_clue2, word_to_guess, enemy_words, neutral, assassin))
    return results

def timing(func, word_to_guess, enemy_words, neutral, assassin):
    start = time.time()
    res = func(word_to_guess, enemy_words, neutral, assassin)
    end = time.time()
    elapsed = round((end - start), 2)
    return [res, elapsed]
    