#imports
import spacy
import random
import numpy as np
import pickle
import pandas as pd
import itertools
import scipy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import pairwise
from sklearn.cluster import KMeans
from collections import Counter
from numba import jit

with open("database/wordlist.pkl", "rb") as f:
    words = pickle.load(f)
    
with open("database/word_lexicals.pkl", "rb") as f:
    texts = pickle.load(f)
    
nlp = spacy.load("fr_core_news_lg")

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import pairwise

def calculate_distance(a, b, option="cosine"):
    if option == "euclidean":
        return np.linalg.norm(a-b)
    if option == "scalar":
        return a @ b
    if option == "cosine":
        return pairwise.cosine_similarity(a.reshape(1,-1), b.reshape(1,-1))[0][0]
    
def calculate_proximity_score(word_candidate, word_board):
    w1 = nlp.vocab.get_vector(str(word_candidate))
    w2 = nlp.vocab.get_vector(str(word_board))
    if word_candidate in texts[word_board]:
        return 1 + calculate_distance(w1,w2)
    return calculate_distance(w1, w2)

def get_score_df(pos, neg, neu, assassin, indices, danger_coeff):
    
    all_words_candidate = []
    for w in pos:
        for lexical_w in texts[w]:
            #if lexical_word is too close to pos word, do not add it
            if lexical_w[:min(4, len(w))] == w[:min(4, len(w))]:
                continue
            all_words_candidate.append(lexical_w)
            
    pos_dist = [[calculate_proximity_score(word_candidate, word_board)for word_board in pos] for word_candidate in all_words_candidate]
    neg_dist = [[calculate_proximity_score(word_candidate, word_board)for word_board in neg] for word_candidate in all_words_candidate]
    neu_dist = [[calculate_proximity_score(word_candidate, word_board)for word_board in neu] for word_candidate in all_words_candidate]
    ass_dist = [calculate_proximity_score(word_candidate, assassin) for word_candidate in all_words_candidate]
    
    
    #build result df, containing candidate and their scores (positive and negative)
    df = pd.DataFrame(pos_dist, index=all_words_candidate)
    #compute a score for each row (a candidate)
    
    df["neg"] = np.max(neg_dist, axis=1) * danger_coeff
    if len(neu) > 0:
        #otherwise, no neutrals
        df["neu"] = np.max(neu_dist, axis=1) 
    df["ass"] = np.array(ass_dist) * danger_coeff
    
    #remove words
    for w in np.concatenate([pos, indices]):
        if w.lower() in all_words_candidate:
            df.drop(w, inplace=True)
    
    df.drop_duplicates(inplace=True)

    return df

def calculate_clue_score(clue, pos, neu, agg, df, min_words_to_find):
    scores = df.loc[df.index == clue]
    
    if len(neu) == 0:
        if scores[["neg", "ass"]].max(axis=1)[0] >= 1:
            return -1, None
    else:
        if scores[["neg", "neu", "ass"]].max(axis=1)[0] >= 1:
            return -1, None
        
    # Order scores by highest to lowest (highest is best
    pos_scores = scores.iloc[:, :len(pos)].values[0]
    boundary = np.max(scores.iloc[:,len(pos):], axis=1).values[0]
    i = 0
    
    min_size_group = 0
    if min_words_to_find:
        #let's go all in
        min_size_group = len(pos)
    
    # Order scores by lowest to highest inner product with the clue.
    ss = sorted((s, i) for i, s in enumerate(pos_scores))
    groups = []
    groups_score = []
    for i in range(min_size_group, len(pos_scores)+1):
        group = ss[-(i+1):]
        group_score = []
        for tpl in group:
            group_score.append(tpl[0])

            # Calculate the "real score" by
            #    (lowest score in group) * [ (group size)^aggressiveness - 1].
            # The reason we subtract one is that we never want to have a group of
            # size 1.
        groups_score.append((np.min(group_score) - (boundary/len(group))) * (len(group)**agg - 0.99))
        groups.append([tpl[1] for tpl in group])
    
    real_score = max(groups_score)
    word_indices = groups[np.argmax(groups_score)]  

    return real_score, word_indices

def get_clue2(pos_words, neg_words, neu_words, assassin_word, danger_coeff=1.2, agg=0.02, given_indices=[]):
    
    # ----- Results to be sent to front
    results = []
    # -----
    
    best_clue, best_score, words_to_guess = None, -1 , None
    
    min_words_to_find = False
    if len(neg_words) < 3:
        print("ALL IN")
        #then opponents is likely to win next round. We should go all in
        min_words_to_find = True
    
    df = get_score_df(pos_words, neg_words, neu_words, assassin_word, given_indices, danger_coeff)
    
    for candidate in df.index:
        real_score, word_ind = calculate_clue_score(candidate, pos_words, neu_words, agg, df, min_words_to_find)
        # ---- adaptation démonstrateur
        if len(results) <= 5:
            new_c = [candidate, real_score, (np.array(pos_words)[word_ind]).tolist()]
            results.append(new_c)
        results.sort(key=lambda x:x[1])
        
        if real_score > results[0][1]:
            del results[0]
            new_c = [candidate, np.round(real_score, 3), (np.array(pos_words)[word_ind]).tolist()]
            results.append(new_c)
        
    results.reverse()
    return results
