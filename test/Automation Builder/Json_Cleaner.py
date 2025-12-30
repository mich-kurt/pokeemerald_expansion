import json
import pandas as pd
import numpy as np
import re
import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
pd.options.mode.chained_assignment = None


with open(r"test\Automation Builder\moves.json", 'r') as f:
    moves_json = json.load(f)

with open(r'test\Automation Builder\pokedex (1).json', 'r') as f:
    pokedex_json = json.load(f)

with open(r'test\Automation Builder\learnsets.json', 'r') as f:
    learnsets_json = json.load(f)


with open(r'test\Automation Builder\wild_encounters.json', 'r') as f:
    encounter_json = json.load(f)


#print(encounter_json['wild_encounter_groups'][0]['encounters'])


def move_cleaner():
    moves_df = pd.DataFrame(columns=["num",'accuracy','basePower','name','category','status','type','chance','isZ','priority'])
    moves_df['name_key'] = [i for i in moves_json]
    moves_df['name'] = [moves_json[i]['name'] for i in moves_json]
    moves_df['num'] = [moves_json[i]['num'] if 'num' in moves_json[i] else 0 for i in moves_json]
    moves_df['accuracy'] = [moves_json[i]['accuracy'] if 'accuracy' in moves_json[i] else 0 for i in moves_json]
    moves_df['basePower'] = [moves_json[i]['basePower'] if 'basePower' in moves_json[i] else 0 for i in moves_json]
    moves_df['category'] = [moves_json[i]['category'] if 'category' in moves_json[i] else 0 for i in moves_json]
    moves_df['type'] = [moves_json[i]['type'] if 'type' in moves_json[i] else 0 for i in moves_json]
    moves_df['isZ'] = [moves_json[i]['isZ'] if 'isZ' in moves_json[i] else 0 for i in moves_json]
    moves_df['chance'] = [moves_json[i]['secondary']['chance'] if 'secondary' in moves_json[i].keys() and moves_json[i]['secondary'] != None and 'chance' in moves_json[i]['secondary'].keys()   else 0 for i in moves_json]
    moves_df['status'] = [moves_json[i]['status'] if 'status' in moves_json[i].keys() and moves_json[i]['status'] != None else 0 for i in moves_json]
    moves_df['2nd_status'] = [moves_json[i]['secondary']['status'] if 'secondary' in moves_json[i].keys() and moves_json[i]['secondary'] != None and 'status' in moves_json[i]['secondary'].keys()   else 0 for i in moves_json]
    moves_df['priority'] = [moves_json[i]['priority'] if 'priority' in moves_json[i].keys() and moves_json[i]['priority'] != None else 0 for i in moves_json]
    moves_df['boosts'] = [sum(moves_json[i]['boosts'].values()) if 'boosts' in moves_json[i].keys() and moves_json[i]['boosts'] != None else 0 for i in moves_json]
    moves_df['charge'] = [1 if 'flags' in moves_json[i].keys() and 'charge' in moves_json[i]['flags'].keys() or 'flags'
                         in moves_json[i].keys() and 'recharge' in moves_json[i]['flags'].keys() or 'flags' in moves_json[i].keys() and 'futuremove' in moves_json[i]['flags'].keys()
                         else 0 for i in moves_json]
    moves_df['sideCondition'] = [1 if 'sideCondition' in moves_json[i].keys() else 0 for i in moves_json]

    moves_df = moves_df[moves_df['isZ'] == 0]
    moves_df = moves_df[moves_df['num'] > 0]
    return moves_df

#x= move_cleaner()
#print(x.loc[x['name']=='Future Sight'])
def learnset_cleaner():
    learnsets_df = pd.DataFrame()
    learnsets_df['pokemon'] = [i for i in learnsets_json]
    learnsets_df['learnset'] = [learnsets_json[i]['learnset'].keys() if 'learnset' in learnsets_json[i].keys() else 0 for i in learnsets_json]
    learnsets_df = learnsets_df[learnsets_df['learnset'] != 0]
    learnsets_df['learnset'] = [list(i) for i in learnsets_df['learnset']]
    return learnsets_df

def pokedex_cleaner():
    learnset_df = learnset_cleaner()
    pokedex_df = pd.DataFrame(columns=["num","Name",'types',"hp","atk","def","spa","spd","spe",'bst',"ability1","ability2","abilityh","evolvl"])
    pokedex_df['name_key'] = [i for i in pokedex_json]
    pokedex_df['Name'] = [pokedex_json[i]['name'] for i in pokedex_json]
    pokedex_df['types'] = [pokedex_json[i]['types'] if 'types' in pokedex_json[i].keys() else 0 for i in pokedex_json]
    pokedex_df['num'] = [pokedex_json[i]['num'] if 'num' in pokedex_json[i].keys() else 0 for i in pokedex_json]
    pokedex_df['hp'] = [pokedex_json[i]['baseStats']['hp'] if 'baseStats' in pokedex_json[i].keys() else 0  for i in pokedex_json]
    pokedex_df['atk'] = [pokedex_json[i]['baseStats']['atk'] if 'baseStats' in pokedex_json[i].keys() else 0  for i in pokedex_json]
    pokedex_df['def'] = [pokedex_json[i]['baseStats']['def'] if 'baseStats' in pokedex_json[i].keys() else 0  for i in pokedex_json]
    pokedex_df['spa'] = [pokedex_json[i]['baseStats']['spa'] if 'baseStats' in pokedex_json[i].keys() else 0  for i in pokedex_json]
    pokedex_df['spd'] = [pokedex_json[i]['baseStats']['spd'] if 'baseStats' in pokedex_json[i].keys() else 0  for i in pokedex_json]
    pokedex_df['spe'] = [pokedex_json[i]['baseStats']['spe'] if 'baseStats' in pokedex_json[i].keys() else 0  for i in pokedex_json]
    pokedex_df['bst'] = pokedex_df['hp'] + pokedex_df['atk'] + pokedex_df['def'] + pokedex_df['spa'] + pokedex_df['spd'] + pokedex_df['spe']
    pokedex_df['ability1'] = [pokedex_json[i]['abilities']['0'] if 'abilities' in pokedex_json[i].keys()  else 0  for i in pokedex_json]
    pokedex_df['ability2'] = [pokedex_json[i]['abilities']['1'] if 'abilities' in pokedex_json[i].keys() and  '1' in pokedex_json[i]['abilities'].keys() else 0  for i in pokedex_json]
    pokedex_df['abilityh'] = [pokedex_json[i]['abilities']['H'] if 'abilities' in pokedex_json[i].keys() and  'H' in pokedex_json[i]['abilities'].keys() else 0  for i in pokedex_json]
    pokedex_df['evolvl'] = [pokedex_json[i]['evoLevel'] if 'evoLevel' in pokedex_json[i].keys() else 0  for i in pokedex_json]
    pokedex_df = pokedex_df[pokedex_df['num'] > 0 ]
    pokedex_df = pokedex_df[~pokedex_df['Name'].str.contains('-Mega|-Gmax|-Totem|Pikachu-|Pichu-|Eevee-Starter|Castform-|-Primal|Deoxys-|Cherrim-Sunshine') ]
    pokedex_df['PhyAttacker'] = np.where(pokedex_df['atk'] > pokedex_df['spa'], 1, 0)
    pokedex_df = pokedex_df.merge(learnset_df,left_on='name_key',right_on='pokemon',how='inner')
    pokedex_df['LvlGroup'] = [3 if i >= 550 else 2 if i >= 485  else 1 if i > 410 else 0 for i in pokedex_df['bst']]
    pokedex_df['type1'] = [i[0] for i in pokedex_df['types']]
    pokedex_df['type2'] = [i[1] if len(i) == 2 else 0 for i in pokedex_df['types']]
    pokedex_df = pokedex_df[(pokedex_df['Name'] != 'Tatsugiri-Stretchy')
                            & (pokedex_df['Name'] != 'Cosmoem')
                            & (pokedex_df['Name'] != 'Dolliv')
                            & (pokedex_df['Name'] != 'Eldegoss')
                            & (pokedex_df['Name'] != 'Pyukumuku')
                            & ('Rotom-Wash' != pokedex_df['Name'])
                            & ('Zygarde-10%' != pokedex_df['Name'])
                            & ('Rotom-Frost' != pokedex_df['Name'])
                            & ('Rotom-Heat' != pokedex_df['Name'])
                            & ('Rotom-Mow' != pokedex_df['Name'])
                            & ('Rotom-Fan' != pokedex_df['Name'])
                            & ('Wobbuffet' != pokedex_df['Name'])
                            & ('Necrozma-Dawn-Wings' != pokedex_df['Name'])
                            & ('Zamazenta-Crowned' != pokedex_df['Name'])
                            & ('Zacian-Crowned' != pokedex_df['Name'])
                            & ('Necrozma-Dusk-Mane' != pokedex_df['Name'])
                            ]
    pokedex_df = pokedex_df.drop(columns= ['name_key','pokemon'])
    return pokedex_df

def trainer_cleaner():
    with open(r'test\Automation Builder\Emerald_Trainers.txt', 'r') as fh:
        trainer_txt = fh.read()
    trainer_txt = trainer_txt.split('/*Comments can also be on a single line*/')[1][3:]
    trainers = re.split(r'\n===', trainer_txt)
    trainer_name = [i.split("===")[0].strip() for i in trainers][1:]

    levels = [re.findall(r"Level: \d+",i) for i in trainers][1:]
    trainer_class = [re.findall(r"Class: \w.*", i) for i in trainers][1:]
    name = [re.findall(r"Name: \w+.*",i) for i in trainers][1:]
    pic = [re.findall(r"Pic: \w+.*", i) for i in trainers][1:]
    gender = [re.findall(r"Gender: \w+.*", i) for i in trainers][1:]
    music = [re.findall(r"Music: \w+.*", i) for i in trainers][1:]
    trainer_data = pd.DataFrame()
    trainer_data['trainer'] = [i for i in trainer_name]
    trainer_data['Levels'] = [i for i in levels]
    trainer_data['class'] = [j.split('Class: ')[1] for i in trainer_class for j in i]
    trainer_data['name'] = [j.split('Name: ')[1] for i in name for j in i]
    trainer_data['pic'] = [j.split('Pic: ')[1] for i in pic for j in i]
    trainer_data['gender'] = [j.split('Gender: ')[1] for i in gender for j in i]
    trainer_data['music'] = [j.split('Music: ')[1] for i in music for j in i]

    max_level = []
    for index, level in trainer_data.iterrows():
        length = len(trainer_data['Levels'][index])
        l1 =[]
        for q in range(length):
            l1.append(int(trainer_data['Levels'][index][q - 1].split("Level: ")[1]))
        max_level.append(max(l1))

    trainer_data['max_level'] = [i for i in max_level]
    trainer_data['type'] = "NA"

    trainer_dict = {'ROXANNE' : 'Rock', 'BRAWLY' : 'Fighting',
                    'WATTSON': 'Electric','FLANNERY' : 'Fire',
                    'JUAN':'Fairy','NORMAN': 'Normal', 'WINONA' : "Flying",
                    "TATE_AND_LIZA" : 'Psychic',
                    'MAXIE' : 'Fire|Ground|Rock', "MAGMA" :'Fire|Ground|Rock',
                    'ARCHIE':'Water|Dark|Poison', 'AQUA' : 'Water|Dark|Poison',
                    "SIDNEY" : 'Dark', "GLACIA" : 'Ice','DRAKE' : 'Dragon', "PHOEBE" : 'Ghost','WALLACE' : 'Water'
                    }
    for i in trainer_dict:
        for index,col in trainer_data.iterrows():
            if i in col['trainer']:
                trainer_data.loc[index,'type'] = trainer_dict[i]
    trainer_data["minBST"] = [350 if i <= 15 else 375 if i<= 19 else 410 if i <= 25 else 425 if i <= 35 else 450 if i <= 40 else 500 if i<=50 else 500  for i in trainer_data['max_level']]
    trainer_data["maxBST"] = [400 if i <= 15 else 450 if i<= 19 else 450 if i <= 25 else 475 if i <= 35 else 500 if i <= 40 else 575 if i<= 50 else 700  for i in trainer_data['max_level']]



    trainer_data = trainer_data.drop(columns='Levels')
    trainer_data['type'] = [i.split("|") if "|" in i else i for i in trainer_data['type'] ]
    return trainer_data


pokedex_data = pokedex_cleaner()
def encounter_creator():
    for index,item in enumerate(encounter_json['wild_encounter_groups'][0]['encounters']):
            #print(item.keys())
            if 'land_mons' in item.keys():
                #print("land")
                for index2,items in enumerate(item['land_mons']['mons']):
                    cleaned_name = str(items['species'].split("SPECIES_")[1].replace("_",'-').capitalize())
                    pokedex_df = pokedex_data.loc[pokedex_data['Name'] == cleaned_name].reset_index()
                    try:
                        min,max = int(pokedex_df['bst'] * .90),int(pokedex_df['bst'] * 1.10)
                    except Exception as e:
                        min, max = 400, 450
                    encounter_pool = pokedex_data[(pokedex_data['bst'] >= min) & (pokedex_data['bst'] <= max)].sample(1)['Name'].reset_index()
                    replace_mon = "SPECIES_" + encounter_pool['Name'][0].replace("-","_").upper()
                    encounter_json['wild_encounter_groups'][0]['encounters'][index]['land_mons']['mons'][index2]['species'] = replace_mon
            if 'water_mons' in item.keys():
                #print("water")
                for index3,items2 in enumerate(item['water_mons']['mons']):
                    cleaned_name = str(items2['species'].split("SPECIES_")[1].replace("_",'-').capitalize())
                    pokedex_df = pokedex_data.loc[pokedex_data['Name'] == cleaned_name].reset_index()
                    try:
                        min,max = int(pokedex_df['bst'] * .90),int(pokedex_df['bst'] * 1.10)
                    except Exception as e:
                        min, max = 400, 450
                    encounter_pool = pokedex_data[(pokedex_data['bst'] >= min) & (pokedex_data['bst'] <= max)].sample(1)['Name'].reset_index()
                    replace_mon = "SPECIES_" + encounter_pool['Name'][0].replace("-","_").upper()
                    #print(encounter_json['wild_encounter_groups'][0]['encounters'][index]['water_mons']['mons'][index3]['species'], replace_mon)
                    encounter_json['wild_encounter_groups'][0]['encounters'][index]['water_mons']['mons'][index3]['species'] = replace_mon
            if 'fishing_mons' in item.keys():
                #print("swim")
                for index4,items3 in enumerate(item['fishing_mons']['mons']):
                    #print(index3)
                    cleaned_name = str(items3['species'].split("SPECIES_")[1].replace("_",'-').capitalize())
                    pokedex_df = pokedex_data.loc[pokedex_data['Name'] == cleaned_name].reset_index()
                    try:
                        min,max = int(pokedex_df['bst'] * .90),int(pokedex_df['bst'] * 1.10)
                    except Exception as e:
                        min, max = 400, 450
                    encounter_pool = pokedex_data[(pokedex_data['bst'] >= min) & (pokedex_data['bst'] <= max)].sample(1)['Name'].reset_index()
                    replace_mon = "SPECIES_" + encounter_pool['Name'][0].replace("-","_").upper()
                    #print(encounter_json['wild_encounter_groups'][0]['encounters'][index]['fishing_mons']['mons'][index3]['species'], replace_mon)
                    encounter_json['wild_encounter_groups'][0]['encounters'][index]['fishing_mons']['mons'][index4]['species'] = replace_mon
    print(encounter_json)

