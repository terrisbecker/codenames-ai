from codenames_bot import guesser
import os
import pandas as pd
import spacy
nlp = spacy.load('en_core_web_lg')
os.chdir('/Users/tbarton/Documents/GitHub/Living_diary/LivingDiary')

text = pd.read_csv('words.txt', header=None)

# selecting game_in_func
game = text.sample(25)

# organaizing game_in_func
game.loc[:, 'label'] = ['red' for i in range(8)] + ['blue' for i in range(9)] + ['black'] + ['grey' for i in range(7)]
game.columns = ['word', 'label']
game.loc[:, 'vector'] = [[nlp(word).vector] for word in game.word.tolist()]
game.index = game.word.values
game.to_csv('game_in_func.csv')

def play_game(game_in_func):
    game_in_func = pd.read_csv('game_in_func.csv')
    while((len(game_in_func.loc[game_in_func['label'] == 'red']) != 0) or (len(game_in_func.loc[game_in_func['label'] == 'blue']) != 0)):
        game_in_func_dictionary = {}
        for i in range(len(game_in_func)):
            game_in_func_dictionary[game_in_func.iloc[i, :].name] = i
        print(game_in_func.loc[game_in_func['label'] != 'chosen', ['word', 'label']])
        team = input('who is currently playing?: ')
        hint = input('what is your hint?: ')
        number = int(input('what is your number?: '))
        guess = guesser(hint, number, game_in_func.loc[game_in_func['label'] != 'chosen'].word.tolist())
        print(f'my guess(s) is (are) {guess}')
        for g in guess:
            if g in game_in_func.loc[game_in_func['label'] == team, 'word'].tolist():
                game_in_func.loc[g, 'label'] = 'chosen'
                game_in_func.to_csv('game_in_func.csv')
            elif g in game_in_func.loc[:, 'word'].tolist():
                game_in_func.loc[g, 'label'] = 'chosen'
                game_in_func.to_csv('game_in_func.csv')
                break
            else:
                break
        if len(game_in_func.loc[game_in_func['label'] == 'red']) == 0:
            print('red wins!!!!')
            return 'red'
        if len(game_in_func.loc[game_in_func['label'] == 'blue']) == 0:
            print('blue wins!!!!')
            return 'blue'


        game_in_func.to_csv('game_in_func.csv')


print(play_game(game))