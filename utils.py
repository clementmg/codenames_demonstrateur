
def getWords(distrib, col):
    # return words_to_guess, negative, neutral, assassin words
    # color : 0 = red, 1 = blue
    negCol = 0
    if col == 0 : negCol = 1 
    
    toGuess, negative, neutral, assassin = [], [], [], ""
    
    for key in distrib : 
        if distrib[key][1] : 
            continue
        wordType = distrib[key][0]
        if (wordType == col):
            toGuess.append(key.lower())
        elif wordType == negCol :
            negative.append(key.lower())
        elif wordType == 2 : 
            neutral.append(key.lower())
        elif wordType == 3 : 
            assassin = key.lower()

    print(f"To guess : {toGuess}\n neg : {negative}\n neutral : {neutral}\n assassin : {assassin}")
    return toGuess, negative, neutral, assassin
    
def getColorName(int_):
    if int_ == 0: return "red"
    else : return "blue"