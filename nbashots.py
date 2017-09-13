import pandas as pd
import numpy as np

df = pd.read_csv('shot_logs.csv', header=0)

defender_df = pd.concat( [df['CLOSEST_DEFENDER_PLAYER_ID'], df['CLOSEST_DEFENDER']], axis=1, keys=['PLAYERID','player'])
defender_df = defender_df.drop_duplicates()

shooter_df = pd.concat( [df['player_id'], df['player_name']], axis=1, keys=['PLAYERID', 'player'])
shooter_df = shooter_df.drop_duplicates()

## FG%

for index, row in shooter_df.iterrows():
    this_id = row['PLAYERID']
    #field goal made
    shooter_df.loc[shooter_df['PLAYERID']==this_id,'FGM']=df[(df['SHOT_RESULT']=='made')&(df['player_id']==this_id)]['player_id'].count()
    #field goal attempted
    shooter_df.loc[shooter_df['PLAYERID']==this_id,'FGA']=df[(df['player_id']==this_id)]['player_id'].count()

    shooter_df['FG%'] = shooter_df['FGM']/shooter_df['FGA']

## Defender FG%

for index, row in defender_df.iterrows():
    this_id = row['PLAYERID'] #current defender
    #defender and Field goal made on defender
    defender_df.loc[defender_df['PLAYERID']==this_id,'DFGM']=df[(df['SHOT_RESULT']=='made') & (df['CLOSEST_DEFENDER_PLAYER_ID']==this_id)]['player_id'].count()
    #defednder Field goal attempts on defender
    defender_df.loc[defender_df['PLAYERID']==this_id,'DFGA']=df[(df['CLOSEST_DEFENDER_PLAYER_ID']==this_id)]['player_id'].count()
    #defending percentage
    defender_df['Defending FG%'] = defender_df['DFGM']/defender_df['DFGA']

    #finding average FG% of shooters on this defender
    defender_dict={}
    for shooter_index, shooter_row in shooter_df.iterrows():
        shooter_id = shooter_row['PLAYERID']
        shots_against=df[(df['CLOSEST_DEFENDER_PLAYER_ID']== this_id)&(df['player_id'] == shooter_id)]['player_id'].count()
        if shots_against > 0:
            defender_dict[shooter_id] = shots_against
    ofg = 0.0
    total_shots = defender_df[(defender_df['PLAYERID']==this_id)]['DFGA']
    for shooter, shots in defender_dict.items():
        ofg += (shots/total_shots)*shooter_df[(shooter_df['PLAYERID']==shooter)].iloc[0]['FG%']
    defender_df.loc[(defender_df['PLAYERID']==this_id), 'oFG%'] = ofg

defender_df['difference'] = defender_df['oFG%'] - defender_df['Defending FG%']

diff_df = defender_df.sort_values(by='difference', axis=0, ascending=False, inplace=False)
diff_df.head(10)

diff_df.to_csv('defender_df.csv')

diff_df[(diff_df['DFGA']>300.0)].head(10)
print('done')
'''
metrics
percentage of shots made, number of shots taken, total pointsshots_taken = len(lbj)
df_made = lbj.loc[lbj['SHOT_RESULT'] == 'made']
df_missed = lbj.loc[lbj['SHOT_RESULT'] == 'missed']
fgp = len(df_made)/shots_taken
'''

