import spacy
import pandas as pd
import os
import numpy as np
nlp = spacy.load('en_core_web_lg')
os.chdir('/Users/tbarton/Documents/GitHub/Living_diary/LivingDiary')
text = pd.read_csv('words.txt', header=None)

# selecting game
game = text.sample(25)

# organaizing game
game.loc[:, 'label'] = ['red' for i in range(8)] + ['blue' for i in range(9)] + ['black'] + ['grey' for i in range(7)]
game.columns = ['word', 'label']
game.loc[:, 'vector'] = [[nlp(word).vector] for word in game.word.tolist()]

# guess
guess = 'Royal'
number = 1


# choose
similarity_vector = np.argsort([nlp(word).similarity(nlp(guess)) for word in game.word.tolist()])[::-1]
game.iloc[similarity_vector[:number], :]


def guesser(guess_word, number, game_words):
    similarity_vector = np.argsort([nlp(word).similarity(nlp(guess_word)) for word in game_words])[::-1]
    return [game_words[w] for w in similarity_vector[:number]]


# hinter ensures that that top word is blue

def most_similar(word, game, n=1):
    ms = nlp.vocab.vectors.most_similar(np.asarray([nlp.vocab.vectors[nlp.vocab.strings[word]]]), n=10000)
    ms = [str(nlp.vocab.strings[w]).lower() for w in ms[0][0] if word.lower() != nlp.vocab.strings[w].lower()]
    index = np.unique(ms, return_index=True)[1]
    ms = [ms[i] for i in sorted(index)]
    ms = [w for w in ms if w.isalpha()]
    ms = [w for w in ms if w not in game.word.tolist()]
    ms = [w for w in ms if not any([True for z in game.word.tolist() if (w.lower() in z.lower()) or (z.lower() in w.lower())])]
    return ms[:n]



def most_similar(word, topn=5):
  word = [w for w in nlp.vocab]
  queries = [
      w for w in word
      if w.is_lower == word.is_lower and w.prob >= -15 and np.count_nonzero(w.vector)
  ]

  by_similarity = sorted(queries, key=lambda w: word.similarity(w), reverse=True)
  return [(w.lower_, w.similarity(word)) for w in by_similarity[:topn+1] if w.lower_ != word.lower_]

most_similar("dog", topn=3)

ms = nlp.vocab.vectors.most_similar(np.asarray([nlp.vocab.vectors[nlp.vocab.strings[word]]]), n=100)
[nlp.vocab.strings[w] for w in ms[0][0] if word.lower() != nlp.vocab.strings[w].lower()]