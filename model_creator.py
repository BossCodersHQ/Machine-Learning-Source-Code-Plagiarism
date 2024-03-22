from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import accuracy_score,log_loss, r2_score
import pandas as pd
import numpy as np
import os
import pickle
import itertools

def calculate_mean_rows(row_list):
    new_rows = []
    index = 0
    for file1_att, file2_att in itertools.combinations(row_list, 2):
        data = np.array([file1_att, file2_att])
        mean = np.average(data, axis=0)
        new_rows.append(mean.tolist())
        index += 1
        if index > 30000:
            return new_rows
    return new_rows

print("creating dataframes")
df = pd.read_csv('dataframes/soco_train_24.csv',header=0)
test_df = pd.read_csv('dataframes/soco_test_A1_24.csv',header=0)

df.set_index(['filename_1_', 'filename_2_'], inplace=True)
test_df.set_index(['filename_1_', 'filename_2_'], inplace=True)

df = df.fillna(-1)
test_df = test_df.fillna(-1)

top_scores_df = df[df['similarity']>0.3]
top_scores_test_df = test_df[test_df['similarity']>0.3]

top_scores = top_scores_df.append(top_scores_test_df)
top_list = top_scores.values.tolist()

x = calculate_mean_rows(top_list)
additional_scores = x + top_list

low_scores = df[df['similarity']<0.3].values.tolist()

final_score_list = additional_scores + low_scores

columns = df.columns.tolist()
final_df = pd.DataFrame(final_score_list, columns=columns)

jfiles_df = pd.read_csv('dataframes/jfiles_24.csv',header=0)
jfiles_df.drop(['filename_1_', 'filename_2_'], axis=1,inplace=True)
jfiles_df = jfiles_df.fillna(-1)

final_df = final_df.append(jfiles_df)
print("creating model")
rf_regressor = RandomForestRegressor(n_estimators=1500, max_depth=20, max_features = 'sqrt', n_jobs = -1)
print("fitting model")
rf_regressor.fit(final_df.drop(['similarity'], axis=1), final_df['similarity'].values.ravel())

pkl_filename = "random_forest_model.pkl"
with open(pkl_filename, 'wb') as file:
    pickle.dump(rf_regressor, file)
