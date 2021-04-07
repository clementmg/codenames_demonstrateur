from AI.lexicalAI import get_clue2
from AI.EmbeddingsAI import get_clue1
import time

# call all AI and return results
def AI_manager(word_to_guess, enemy_words, neutral, assassin):
    results = []
    results.append(timing(get_clue1, word_to_guess, enemy_words, neutral, assassin))
    print("gard on est la")
    print(results)
    results.append(timing(get_clue2, word_to_guess, enemy_words, neutral, assassin))
    print(results)
    return results

def timing(func, word_to_guess, enemy_words, neutral, assassin):
    start = time.time()
    res = func(word_to_guess, enemy_words, neutral, assassin)
    end = time.time()
    elapsed = round((end - start), 2)
    return [res, elapsed]
    