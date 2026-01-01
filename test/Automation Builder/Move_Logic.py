import random

from Json_Cleaner import move_cleaner, pokedex_cleaner
import pandas as pd
import numpy as np
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
pd.options.mode.chained_assignment = None
def base_points(df):
    moves_df = move_cleaner()
    pokedex_df = pokedex_cleaner()
    df['Points'] = [4 if i >= 100 else 3 if i >= 80 else 2 if i >= 60 else 1 if i > 0 else 0 for i in df['basePower']]
    df['Points'] += [1 if i >= 100 else 0 if i >= 80 else 0 if i == True else - 1
        if i >= 60 else - 2 for i in df['accuracy']]
    df['Points'] += [4 if i == 'slp' else 1 if i == 'frz' else 0 if i == 0 else 2 for i in df['status']]
    df['Points'] += [3 if i >= 2 else 1 if i == 1 else 1 if i == -1 else 1.5 if i < - 1 else 0 for i in df['boosts']]
    df['Points'] += [3 if i == 'Yawn' else -2 if i == 'Dream Eater' or i == 'Last Resort' else -1 if i == 'Focus Punch' or i == 'Swagger' or i == 'Agility' or i == 'Work Up' or i == "Steel Roller" or i == 'Iron Defense' or i == 'Amnesia' or i == 'Thrash' else 0 for i in df['name']]
    df['Points'] += [1 if i > 0 else 0 for i in df['priority']]
    df['Points'] += [-2 if i == 1 else 0 for i in df['charge']]
    df['Points'] += [1 if i == 1 else 0 for i in df['sideCondition']]
    #df['Level Groups'] = [3 if i >= 4 else 2 if i > 2 else 1 for i in df['Points']]
    return df

def pokemon_specific_points(moves_data,pokemon,pokemon_data):
    pokemon_info = pokemon_data.loc[pokemon_data['Name'] == pokemon].reset_index()
    moves_data['avaliable'] = 0
    for j,i in moves_data.iterrows():
        if i['name_key'] in pokemon_info['learnset'][0]:
            moves_data.loc[j,'avaliable'] = 1
    moves_data = moves_data[moves_data['avaliable'] == 1]
    for j,i in moves_data.iterrows():
        if i['type'] in pokemon_info['types'][0] and i['category'] != 'Status':
            moves_data.loc[j,'Points'] += 2
    for j,i in moves_data.iterrows():
        if i['category'] == 'Physical' and pokemon_info['PhyAttacker'][0] == 1:
            moves_data.loc[j,'Points'] += 2
        elif i['category'] == 'Special' and pokemon_info['PhyAttacker'][0] == 0:
            moves_data.loc[j, 'Points'] += 2
        else:
            continue
    pokemon_altered_moves = moves_data.copy()
    pokemon_altered_moves['EarlyGameMove'] = [1 if i <= 7 else 0 for i in pokemon_altered_moves['Points']]
    
    if len(pokemon_altered_moves) < 4:
        print("GOT HERE")
    return pokemon_altered_moves

def assigning_4_moves(pokemon_altered_moves):
    status_moves = pokemon_altered_moves[pokemon_altered_moves['category'] == 'Status']
    status_moves = status_moves[status_moves['Points'] == max(status_moves['Points'])]
    status_moves = list(status_moves['name'])
    status_moves = random.choices(status_moves, k = 1)

    atk_moves = pokemon_altered_moves[pokemon_altered_moves['category'] != 'Status']
    atk_list = []
    type_list = []
    atk_moves = atk_moves.sort_values(by='Points', ascending = False )
    while len(atk_list) < 4:
        for index, move in atk_moves.iterrows():

            if atk_moves['type'][index] not in type_list:
                atk_list.append(atk_moves['name'][index])
                type_list.append(atk_moves['type'][index])
                break

    atk_moves = random.sample(atk_list, 3)
    atk_moves.append(status_moves[0])

    return atk_moves

