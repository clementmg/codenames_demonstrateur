from AI.lexicalAI import get_clue2
from AI.EmbeddingsAI import get_clue1
import time

# call all AI and return results
def AI_manager(ai, word_to_guess, enemy_words, neutral, assassin, agg=0.1, danger=3):
    results = []
    ai = int(ai)
    agg = float(agg)
    danger = float(danger)
    if ai == 1 :
        results.append(timing(get_clue1, word_to_guess, enemy_words, neutral, assassin, agg, danger))
    elif ai == 2 :
        results.append(timing(get_clue2, word_to_guess, enemy_words, neutral, assassin, agg, danger))

    return results

def timing(func, word_to_guess, enemy_words, neutral, assassin, agg, danger):
    start = time.time()
    res = func(word_to_guess, enemy_words, neutral, assassin, danger_coeff=danger, agg=agg)
    end = time.time()
    elapsed = round((end - start), 2)
    return [res, elapsed]
    