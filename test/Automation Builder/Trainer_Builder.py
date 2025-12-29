from Pokemon_Decider import random_teams
from Json_Cleaner import move_cleaner, pokedex_cleaner
from Move_Logic import base_points, assigning_4_moves,pokemon_specific_points
import random
import pandas as pd
import numpy as np
def Trainer_Format():
    moves = base_points(move_cleaner())
    pokedex = pokedex_cleaner()
    teams = random_teams()
    for index, col in teams.iterrows():
        first = True
        for j in col['Pokemon']:
            finalized_moves = assigning_4_moves(pokemon_specific_points(moves,j,pokedex))
            if first == True:
                x = print(f"=== {col['trainer']} ===\n"\
                f"Name: {col['name']}\n"\
                f"Class: {col['class']}\n"\
                f"Pic: {col['pic']}\n"\
                f"Gender: {col['gender']}\n"\
                f"Music: {col['music']}\n"\
                f"Items: Mega Ring\n"
                f"Double Battle: No\n"\
                f"AI: Basic Trainer\n"
                )
                first = False
            else:
                y = print(f"{j}\n"\
            f"Level: {col['max_level']}\n"
            f"IVs: {random.randint(1,31)} HP / {random.randint(1,31)} Atk / {random.randint(1,31)} Def / {random.randint(1,31)} SpA / {random.randint(1,31)} SpD / {random.randint(1,31)} Spe\n"
            f"-{finalized_moves[0]}\n" \
            f"-{finalized_moves[1]}\n"  \
            f"-{finalized_moves[2]}\n" \
            f"-{finalized_moves[3]}\n")



