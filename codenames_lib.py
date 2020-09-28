import spacy
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
nlp = spacy.load('en_core_web_lg')

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

def similar_words(input_words, n = 100):
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

	return similarity_words[:n]
