import spacy
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import pairwise_distances

filename = "C:/Users/terri/OneDrive/Documents/codenames-ai/data/words.txt"

nlp = spacy.load('en_core_web_lg')
text = pd.read_csv(filename, header=None)
game = text.sample(9)[0].tolist()

# retuns the top <number> most similar words to <guess_word> out of <game_words>
# Inputs:
#	guess_word - str
#	number - int
#	game_words - character list

def guesser(guess_word, number, game_words):
    try:
        similarity_vector = np.argsort([nlp(word).similarity(nlp(guess_word)) for word in game_words])[::-1]
        return [game_words[w] for w in similarity_vector[:number]]
    except Exception as e:
        print(f'Something went wrong \n{e}')
        return game_words[0]

# returns the top <n> most similar words to the vector of input words based on the 
# trained nlp model
# Inputs:
#	input_words: string of words to hint at, each word separated by a space
#	n: number of best guesses to return. Ranked from best to worst

def similar_words_cosine(input_words, n = 10):
	# initialize inputs
	input_tokens = nlp(input_words)
	input_vecs = np.array([x.vector for x in input_tokens])

	# get all word vectors from the model
	ids = [x for x in nlp.vocab.vectors.keys()]
	vectors = np.array([nlp.vocab.vectors[x] for x in ids])

	# calculate cosine similarity between input words and the model words
	sim = cosine_similarity(vectors, input_vecs)
	similar_vec_arg = np.argsort(sim.sum(axis=1))[::-1]
	similarity_keys = [ids[x] for x in similar_vec_arg]
	similarity_words = [nlp.vocab.strings[x] for x in similarity_keys]

	# lowercase everything and pull distinct
	similarity_words_lower = [x.lower() for x in similarity_words]
	similarity_words_unique = pd.Series(similarity_words_lower).drop_duplicates().tolist()

	# drop similar words or words with s at the end
	words_l = input_words.split()
	words_drop = [x for x in similarity_words_unique if x not in words_l]
	words_s = [x for x in similarity_words_unique if x.endswith("s")]
	words_drop = [x for x in words_drop if x not in words_s[:n]]
	return words_drop[:n]

# same as the cosine similar words, but with euclidian distance similarity instead
# has some printing errors plus it's not as good as cosine similarity yet

def similar_words_euclid(input_words, n = 10):
	# initialize inputs
	input_tokens = nlp(input_words)
	input_vecs = np.array([x.vector for x in input_tokens])

	# get all word vectors from the model
	ids = [x for x in nlp.vocab.vectors.keys()]
	vectors = np.array([nlp.vocab.vectors[x] for x in ids])

	# calculate euclidian distance between input words and the model words
	sim = pairwise_distances(vectors, input_vecs)
	similar_vec_arg = np.argsort(sim.sum(axis=1))[::1]
	similarity_keys = [ids[x] for x in similar_vec_arg]
	similarity_words = [nlp.vocab.strings[x] for x in similarity_keys]

	# lowercase everything and pull distinct

	similarity_words_lower = [x.lower() for x in similarity_words]
	similarity_words_unique = pd.Series(similarity_words_lower).drop_duplicates().tolist()

	# drop similar words or words with s at the end
	words_l = input_words.split()
	words_drop = [x for x in similarity_words_unique if x not in words_l]
	words_s = [x for x in similarity_words_unique if x.endswith("s")]
	words_drop = [x for x in words_drop if x not in words_s[:n]]

	return words_drop[:n]