import spacy
import pandas as pd
import os
import numpy as np
from tqdm import tqdm
import time
# import enchant  # This would work great! But i cannot install the dependencies on my work comp...

nlp = spacy.load('en_core_web_lg')

def guesser(guess_word, number, game_words):
    try:
        similarity_vector = np.argsort([nlp(word).similarity(nlp(guess_word)) for word in game_words])[::-1]
        return [game_words[w] for w in similarity_vector[:number]]
    except Exception as e:
        print(f'Something went wrong \n{e}')
        return game_words[0]

def fast_guesser(guess_word_nlp, number, game_words_vector):
    try:
        similarity_vector = np.argsort([guess_word_nlp.similarity(game_words_vector[i]) for i in range(len(game_words_vector))])[::-1]
        return [game_words_vector[w].text for w in similarity_vector[:number]]
    except Exception as e:
        print(f'Something went wrong \n{e}')
        return game_words_vector[0]
# hinter ensures that that top word is blue

def most_similar(word, game, n=10000):
    ms = nlp.vocab.vectors.most_similar(np.asarray([nlp.vocab.vectors[nlp.vocab.strings[word]]]), n=10000)
    ms = [str(nlp.vocab.strings[w]).lower() for w in ms[0][0] if word.lower() != nlp.vocab.strings[w].lower()]
    index = np.unique(ms, return_index=True)[1]
    ms = [ms[i] for i in sorted(index)]
    ms = [w for w in ms if w.isalpha()]
    ms = [w for w in ms if w not in game.word.tolist()]
    ms = [w for w in ms if not any([True for z in game.word.tolist() if (w.lower() in z.lower()) or (z.lower() in w.lower())])]
    return ms[:n]


# hint giver is inefficient
# lets search all 6's, theres no need for less. THen lets search decending down
def hint_giver(game, team='blue', time_me=False):
    global_total = 0
    choice_n = 1
    choice_word = ''
    other_team = ['blue' if team == 'red' else 'red' for i in [team]][0]
    good = game.loc[game['label'] == team, :]
    neutral = game.loc[game['label'] == 'grey']
    kill = game.loc[game['label'] == 'black']
    bad = game.loc[game['label'] == other_team]
    possible_words = pd.read_csv('hint_words.csv', index_col=0)  # guess words
    if time_me:  #initialize the time me df
        i = 0
        time_df = pd.DataFrame(index=range(len(possible_words)), columns=['cleaning_stage', 'guess_evaluation', 'saving_loop'])
    game_word_vector_nlp = nlp(' '.join(game.word.tolist()))
    for word in tqdm(possible_words.iloc[:, 0].tolist(), total=len(possible_words)):  # itterate over words
        s = time.time()
        if any([True for w2 in game.word.tolist() if (word in w2) or (w2 in word)]):  # eliminate illegal words
            continue
        if time_me:  # stage 1
            time_df.iloc[i, 0] = time.time() - s
            s = time.time()
        res = fast_guesser(nlp(word), len(good), game_word_vector_nlp)
        if time_me:  # stage 2
            time_df.iloc[i, 1] = time.time() - s
            s = time.time()
        if len(res) == 0:
            continue
        current_total = 0
        n = 0
        for r in res:
            if r in good.word.tolist():
                current_total += 1
                n += 1
            elif r in neutral.word.tolist():
                current_total += 0
                break
            elif r in bad.word.tolist():
                current_total += -0.1
                break
            else:
                current_total += -10
                break
        if current_total > global_total:
            choice_word = word
            choice_n = n
            global_total = current_total
        if time_me:  # stage 3
            time_df.iloc[i, 2] = time.time() - s
            s = time.time()
            i += 1
            print(time_df)
    if time_me:
        return (choice_word, choice_n, global_total, time_df)
    return (choice_word, choice_n, global_total)



def similarity(game, word):
    pass
'''min(
        min(sum(euclidean distance from blue word to hint)) 
            + 
        sum(euclidean distance from grey words to hint) 
            +
        k*sum(euclidean distance from red words to hint)
            +
        j*sum(euclidean distance from black word to hint)
    )
    in principal, we want the hint word to be closest to blue word, but furthest from bad words, some bad words are 
    worse than others. 
'''