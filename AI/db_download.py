import spacy
import random
import numpy as np
import pickle
import pandas as pd

# ==================

import urllib.request
import pickle
f = urllib.request.urlopen("https://www.dropbox.com/s/pj7nwhkgr4l2wtt/word_database.pkl?dl=0")
print("worked")
BDD = pickle.load(f)

# import dropbox
# BDD = None
# token = "zx9DV4T5n6MAAAAAAAAAAW1E7vMt-PSu_cGT4nOA2qkdunPsEvtufLFPzI_BMDNJ"
# file = "word_database.pkl"
# file_loc = f"/cs-codenames-app/{file}"
# dbx = dropbox.Dropbox(token)

# def read_file(dbx, file):
#     print("downloading database ...")
#     _, f = dbx.files_download(file)
#     f = f.content
#     # f = f.decode('utf-8')
#     return f
#     # f = f.decode(("utf8"))
    
# with open(read_file(dbx, file_loc), 'rb') as f:
#     BDD = pickle.load(f)
# # BDD = pickle.load(read_file(dbx, file_loc))
# # with open(read_file(dbx, file_loc), "rb") as f:
# #     print("decoding")
# #     BDD = pickle.load(f)
# # ==================