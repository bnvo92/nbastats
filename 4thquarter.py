import pandas as pd
import numpy as np
import matplotlib as plt


df = pd.read_csv('shot_logs.csv', header=0)

##df2 = pd.concat(df['GAME_ID'], df['W'], df['FINAL_MARGIN'], df['PERIOD'], df['GAME_CLOCK'],
##                  df['player_id'], df['player_name'] ,df['SHOT_RESULT'],df['PTS_TYPE'], axis=1)

shooter_df = pd.concat( [df['player_id'], df['player_name']], axis=1, keys=['PLAYERID', 'player'])
shooter_df = shooter_df.drop_duplicates()

for index, row in shooter_df.iterrows():
    this_id = row['PLAYERID']
    #field goal made
    shooter_df.loc[shooter_df['PLAYERID']==this_id,'FGM']=df[(df['SHOT_RESULT']=='made')&(df['player_id']==this_id)]['player_id'].count()
    #field goal attempted
    shooter_df.loc[shooter_df['PLAYERID']==this_id,'FGA']=df[(df['player_id']==this_id)]['player_id'].count()

    shooter_df['FG%'] = shooter_df['FGM']/shooter_df['FGA']

    shooter_df.loc[shooter_df['PLAYERID']==this_id,'4th FGM']=df[(df['SHOT_RESULT']=='made')&(df['player_id']==this_id)&(df['PERIOD']==4)]['player_id'].count()
    shooter_df.loc[shooter_df['PLAYERID']==this_id,'4th FGA']=df[(df['player_id']==this_id)&(df['PERIOD']==4)]['player_id'].count()
    
    shooter_df['4th FG%'] = shooter_df['4th FGM']/shooter_df['4th FGA']

    shooter_df.loc[shooter_df['PLAYERID']==this_id, '4th 3FGM']=df[(df['SHOT_RESULT']=='made')&(df['PTS_TYPE']==3)&(df['player_id']==this_id)&(df['PERIOD']==4)]['player_id'].count()
    shooter_df.loc[shooter_df['PLAYERID']==this_id, '4th 3FGA']=df[(df['PTS_TYPE']==3)&(df['player_id']==this_id)&(df['PERIOD']==4)]['player_id'].count()

    shooter_df['4th 3FG%'] = shooter_df['4th 3FGM']/shooter_df['4th 3FGA']
    
print('done')

fourth_df = shooter_df.sort_values(by='4th FG%', axis=0, ascending=False, inplace=False)
##fourth_df[(fourth_df['4th FGA']>50)].head(15)
