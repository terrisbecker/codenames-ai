import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sn
import numpy as np
from sklearn.metrics import confusion_matrix
from matplotlib import colors
from matplotlib.colors import ListedColormap

def plot_field(game_dict, colors=None):
    labels = np.array([i for i in game_dict.keys()]).reshape(5, 5)
    color_numbers = np.random.randint(0, 4, (5, 5))
    cmap = ListedColormap(['red', 'blue', 'grey', 'black'])
    sns.heatmap(color_numbers, cmap=cmap, annot=labels, fmt='s', cbar=False)
    plt.show()
    ### Up next you are going to incorrperate this into your function, and then you are going to
    ### fix your code so that you do not need to delete 'game' entries with "chosen" as their entry, so you can use
    ### them as your color metric in plot_feild