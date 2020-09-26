from codenames_bot import guesser
import os
import pandas as pd
import spacy
nlp = spacy.load('en_core_web_lg')
os.chdir('/Users/tbarton/Documents/GitHub/Living_diary/LivingDiary')

text = pd.read_csv('words.txt', header=None)

# selecting game
game = text.sample(25)

# organaizing game
game.loc[:, 'label'] = ['red' for i in range(8)] + ['blue' for i in range(9)] + ['black'] + ['grey' for i in range(7)]
game.columns = ['word', 'label']
game.loc[:, 'vector'] = [[nlp(word).vector] for word in game.word.tolist()]
game.index = game.word.values
game.to_csv('gamestate.csv')

def play_game(game):
    while((len(game.loc[game['label'] == 'red']) != 0) or (len(game.loc[game['label'] == 'blue']) != 0)):
        game = pd.read_csv('gamestate.csv')
        game_dictionary = {}
        for i in range(len(game)):
            game_dictionary[game.iloc[i, :].name] = i
        print(game.loc[game['label'] != 'chosen', ['word', 'label']])
        team = input('who is currently playing?: ')
        hint = input('what is your hint?: ')
        number = int(input('what is your number?: '))
        guess = guesser(hint, number, game.word.tolist())
        print(f'my guess(s) is (are) {guess}')
        for g in guess:
            if g in game.loc[game['label'] == team, 'word'].tolist():
                game.loc[g, 'label'] = 'chosen'
            elif g in game.loc[:, 'word'].tolist():
                game.loc[g, 'label'] = 'chosen'
                break
            else:
                break
        if len(game.loc[game['label'] == 'red']) == 0:
            print('red wins!!!!')
            return 'red'
        if len(game.loc[game['label'] == 'blue']) == 0:
            print('blue wins!!!!')
            return 'blue'

        game.to_csv('gamestate.csv')



print(play_game(game))