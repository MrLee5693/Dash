# %%
from mapping import generate_mapping_function
from mapping_dict import get_breed_dict
import pandas as pd
from tqdm import tqdm
# %%
data = pd.read_pickle('../File/Diagnosis.pkl') # 변경할 부분
# %% 
mapping_dict = get_breed_dict()
mapping_func = generate_mapping_function(mapping_dict,contain=True)
# %%
input_list = data['Name2']
mapped_list = list(map(mapping_func, tqdm(input_list)))
data['Name'] = mapped_list
# %%
input_list = data['Name3']
mapped_list = list(map(mapping_func, tqdm(input_list)))
data['Name_ko'] = mapped_list

def merge_name(row):
    if row['Name'] == "Unknown" and row['Name_ko'] != "Unknown":
        row['Name'] = row['Name_ko']
    return row['Name']
#
data['Name'] = data.apply(lambda x : merge_name(x), axis = 1)
# %%
data.query('Name == "Unknown" and Name_ko == "Unknown"')

# %%
data = data.query('Name != "Unknown"')[['Name', 'Sex', '_Month', '_Year', 'Diagnosis']] # 변경할 부분
data.to_csv('../File/Diagnosis_named.csv', index = False)
