import spacy
import random
import numpy as np
import pickle
import pandas as pd
from AI.db_download import BDD 

nlp = spacy.load("fr_core_news_lg")

from nltk import PorterStemmer
st = PorterStemmer()

# with open(BDD, "rb") as f:
#     BDD = pickle.load(f)
    
with open("database/wordlist.pkl", 'rb') as f:
    lst = pickle.load(f)
     
all_words = np.array(list(BDD.values()))

# @njit
def is_stopwords(w, lst_words):
    if w in lst_words:
        return False
    stem_w = st.stem(w)
    for word in lst_words:
        if stem_w in word:
            return False
        if word in w:
            return False
    if len(w) < 3:
        return False
    return True

# @njit
def get_clue(pos_words, neg_words, neu_words, assassin_word, danger_coeff=1.8, agg=0.05, topn=50000, given_indices=[]):
    
    #vectorize words
    pos_vecs = [nlp.vocab.get_vector(str(w)) for w in pos_words]   # Shape (8, 300)
    neg_vecs = [nlp.vocab.get_vector(str(w)) for w in neg_words]
    neu_vecs = [nlp.vocab.get_vector(str(w)) for w in neu_words]
    ass_vec = nlp.vocab.get_vector(str(assassin_word))             # Shape (300)

    #get n_best candidates with the highest min scalar product
    #get pos_words scores
    pw = (all_words @ np.array(pos_vecs).T)                # Shape (37124, 8)
    #get neg_words scores (max)
    ngw = (all_words @ np.array(neg_vecs).T).max(axis=1)   # Shape (37124,)
    if len(neu_words) > 0:
        nw = (all_words @ np.array(neu_vecs).T).max(axis=1)    # Shape (37124,)
    aw = all_words @ np.array(ass_vec).T                   # Shape (37124,)


    #get top candidates:
    df = pd.DataFrame(pw, index=BDD.keys())              # 37124 rows 8 columns
    neg_df = pd.DataFrame(ngw, index=BDD.keys())         # 37124 rows 1 column
    if len(neu_words) > 0:
        neu_df = pd.DataFrame(nw, index=BDD.keys())
    ass_df = pd.DataFrame(aw, index=BDD.keys())

    for w in np.concatenate([pos_words, given_indices]): # Remove pos words and already given clues
        if w in BDD.keys():
            df.drop(w, inplace=True)
            neg_df.drop(w, inplace=True)
            if len(neu_words) > 0:
                neu_df.drop(w, inplace=True)
            ass_df.drop(w, inplace=True)

    #filter
    df["top"] = df.apply(lambda x: np.sort(x)[-1:], axis=1)
    threshold = np.sort(df.top)[::-1][:topn][-1][0]
    max_len = 1
    

    if len(pos_words) > 1:
        #get a top 2
        df["top"] = df.apply(lambda x: np.sort(x)[-2:].min(), axis=1)
        threshold = np.sort(df.top)[::-1][:topn][-1]
        max_len = 2

        
    
    df["is_top"] = df.top >= threshold
    df["neg_filter"] = df["top"] > danger_coeff*neg_df.max(axis=1)
    if len(neu_words) > 0:
        df["neu_filter"] = df["top"] > 1.2*neu_df.max(axis=1)
    df["ass_filter"] = df["top"] > danger_coeff*ass_df.max(axis=1)

    if len(neu_words) > 0:
        candidates = df.loc[df.is_top].loc[df.neu_filter].loc[df.neg_filter].loc[df.ass_filter]
    if len(neu_words) == 0:
        candidates = df.loc[df.is_top].loc[df.neg_filter].loc[df.ass_filter]

    best_clue, best_score, best_k, best_g = None, -1, 0, ()
    
    # ------------ added : dict
    allResults = dict()
    i_key = 0
    # ------------
    
    for clue_i, scores in enumerate(candidates.iloc[:,:len(pos_words)].values):


        #transform clue_i into the actual word
        clue_word = candidates.index[clue_i]

        if not is_stopwords(clue_word, pos_words):
            continue
        

        # Order scores by lowest to highest inner product with the clue.
        ss = sorted((s, i) for i, s in enumerate(scores))
        groups = []
        groups_score = []
        for i in range(len(scores)):
            group = ss[-(i+1):]
            group_score = []
            for tpl in group:
                group_score.append(tpl[0])

                # Calculate the "real score" by
                #    (lowest score in group) * [ (group size)^aggressiveness - 1].
                # The reason we subtract one is that we never want to have a group of
                # size 1.
            groups_score.append((np.min(group_score)) * (len(group)**agg - 0.99))
            groups.append([tpl[1] for tpl in group])


        real_score = max(groups_score)

        if real_score > best_score:
            #update
            ind = groups[np.argmax(groups_score)]
            best_g = np.array(pos_words)[ind]
            best_k = len(best_g)
            best_clue = clue_word
            best_score = real_score
            
            # added to get result
            indice = str(i_key)
            allResults[indice] = [best_clue, np.round(best_score, 2), best_g.tolist()]
            print("Res : ", best_clue, np.round(best_score, 2), best_g)
            i_key += 1

    candidates = candidates.sort_values(by=['top'], ascending = False)
    
    # return best_clue, best_score, best_g, candidates
    return allResults

