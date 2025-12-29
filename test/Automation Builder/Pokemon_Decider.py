from Json_Cleaner import trainer_cleaner, pokedex_cleaner
import pandas as pd
import numpy as np
def random_teams():
    trainer_df = trainer_cleaner()
    trainer_df['Pokemon'] = 0
    pokedex_df = pokedex_cleaner()
    for index, col in trainer_df.iterrows():
        if col['type'] == "NA":
            trainer_dex = pokedex_df[(pokedex_df['bst'] >= col['minBST']) & (pokedex_df['bst'] <= col['maxBST'])]
            trainer_dex = trainer_dex.sample(6)
        elif type(col['type']) == list:
            trainer_dex = pokedex_df[(pokedex_df['bst'] >= col['minBST']) & (pokedex_df['bst'] <= col['maxBST'])]
            trainer_dex = trainer_dex[(trainer_dex['type1'].isin(col['type'])) | (trainer_dex['type2'].isin(col['type']))]
        else:
            trainer_dex = pokedex_df[(pokedex_df['bst'] >= col['minBST'] + 25) & (pokedex_df['bst'] <= col['maxBST'] + 40 )]
            trainer_dex = trainer_dex[(trainer_dex['type1'] == col['type']) | (trainer_dex['type2'] == col['type'])]
        trainer_dex = trainer_dex.sample(6)
        team = trainer_dex['Name'].to_list()
        trainer_df['Pokemon'][index] = team
    return trainer_df
