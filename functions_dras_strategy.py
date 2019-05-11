# -*- coding: utf-8 -*-
"""
Created on Thu May  2 12:32:47 2019

@author: pszydlik
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def dataset_prepering(loc, file, league):
    
    dataset = pd.read_csv(loc + file +'.csv', index_col = 0)

    dataset = dataset.loc[(dataset["HM1"] != "M") &  (dataset["AM1"] != "M")  & (dataset["AM2"] != "M")  &
                          (dataset["HM2"] != "M")  & (dataset["HM3"] != "M") & (dataset["AM3"] != "M")  &
                            (dataset["HM4"] != "M")  & (dataset["HM4"] != "M") &  (dataset["HM5"] != "M")  & (dataset["HM5"] != "M")]
    
    
    marketv = pd.read_csv(loc + 'budget_'+ league +'_final.csv', index_col = 0)
    
    marketv.Sezon = marketv.Sezon.astype(str).str[2:]
    marketv["Sezon"] = marketv["Sezon"].astype(int) + 1
    
    dataset = pd.merge(dataset, marketv,  how='inner', left_on=['HomeTeam','Sezon'], 
                           right_on = ['Club','Sezon'], sort=False)
    
    dataset = dataset.rename(columns={'Age': 'Age_H', 'Foreign': 'Foreign_H',
                                 'Total_value': 'Total_value_H', 'Market_value': 'Market_value_H'})
    
    dataset = pd.merge(dataset, marketv,  how='inner', left_on=['AwayTeam','Sezon'], 
                           right_on = ['Club','Sezon'], sort=False)
    
    dataset = dataset.rename(columns={'Age': 'Age_A', 'Foreign': 'Foreign_A',
                                    'Total_value': 'Total_value_A', 'Market_value': 'Market_value_A'})
        
        
    df_final = dataset
    
    cols_cat = [ 'HTWinStreak3', 'HTWinStreak5', 'HTLossStreak3',
       'HTLossStreak5', 'ATWinStreak3', 'ATWinStreak5', 'ATLossStreak3',
       'ATLossStreak5']
    df_final[cols_cat] = df_final[cols_cat].astype('category')
    
    cat_vars=["HM1", "HM2", "AM1", "AM2",
          "HM3", "HM4", "HM5", "AM3", "AM4", "AM5"]

    for var in cat_vars:
        cat_list='var'+'_'+var
        cat_list = pd.get_dummies(df_final[var], prefix=var)
        df_final1=df_final.join(cat_list)
        df_final=df_final1

    data_vars=df_final.columns.values.tolist()
    to_keep=[i for i in data_vars if i not in cat_vars]

    df_final=df_final[to_keep]
 
    cols_sel = ['HomeTeam', 'AwayTeam', 'HTGS', 'ATGS', 'HTGC', 'ATGC', 'HTP', 'ATP', 'MW', 'HomeTeamLP',
       'AwayTeamLP',  'HT_LP', 'AT_LP', 'HTFormPtsStr',
       'ATFormPtsStr', 'HTFormPts', 'ATFormPts', 'HTWinStreak3',
       'HTWinStreak5', 'HTLossStreak3', 'HTLossStreak5', 'ATWinStreak3',
       'ATWinStreak5', 'ATLossStreak3', 'ATLossStreak5', 'HTGD', 'ATGD',
        'HT_Wins', 'AT_Wins', 'HT_Loss', 'AT_Loss', 'HT_Draws', 'AT_Draws',
       'DiffPts', 'DiffFormPts', 'DiffLP', 'H2H_Home', 'H2H_Away','Total_value_H', 'Total_value_A',
       'H2H_Home_pts', 'H2H_Away_pts',  'Mean_home_goals', 'Mean_away_goals', 'Age_H', 'Age_A',
         'HM1_D',   'HM1_L', 'HM1_W', 'HM2_D', 'HM2_L', 'HM2_W', 'AM1_D', 'AM1_L',
       'AM1_W',        'AM2_D',       'AM2_L', 'AM2_W', 'HM3_D', 'HM3_L', 'HM3_W',
       'HM4_D', 'HM4_L', 'HM4_W', 'HM5_D', 'HM5_L',  'HM5_W',
       'AM3_D', 'AM3_L', 'AM3_W', 'AM4_D', 'AM4_L', 'AM4_W', 'AM5_D',
       'AM5_L', 'AM5_W']
    

    cols_sel = np.intersect1d(cols_sel,  df_final.columns)
    



    df_final = df_final[cols_sel]
    
    
    df_final.HTFormPts = df_final.HTFormPts.fillna(df_final.HTFormPts.median())
    df_final.ATFormPts = df_final.ATFormPts.fillna(df_final.ATFormPts.median())
    df_final.DiffFormPts = df_final.DiffFormPts.fillna(df_final.DiffFormPts.median())
    
    df_final["H2H_Diff"] = df_final["H2H_Home_pts"] - df_final["H2H_Away_pts"]
    df_final["Total_Diff"] = df_final["Total_value_H"] / df_final["Total_value_A"]
    df_final["Age_diff"] = df_final["Age_H"] - df_final["Age_A"]
    df_final["LP_Diff"] = df_final["HT_LP"] - df_final["AT_LP"]
    
    
     
    cols_sel = [ 'HomeTeam', 'AwayTeam','HTP', 'ATP','HM1_D', 'HM1_L', 'HM1_W',
       'HM2_D', 'HM2_L', 'HM2_W', 'AM1_D', 'AM1_L', 'AM1_W',
       'AM2_D',    'AM2_L',     'AM2_W', 'HM3_D', 'HM3_L', 'HM3_W', 'HM4_D', 'HM4_L', 'HM4_W', 'HM5_D',
       'HM5_L', 'HM5_W', 'AM3_D', 'AM3_L', 'AM3_W', 'AM4_D', 'AM4_L',
       'AM4_W', 'AM5_D', 'AM5_L',  'AM5_W', 
         'HT_Wins', 'AT_Wins', 'HT_Loss', 'AT_Loss', 'HT_Draws', 'AT_Draws',
        'MW',  'HT_LP', 'AT_LP',    'HTWinStreak3', 'HTWinStreak5', 'HTLossStreak3',
       'HTLossStreak5', 'ATWinStreak3', 'ATWinStreak5', 'ATLossStreak3',
       'ATLossStreak5', 'HTGD', 'ATGD', 'DiffPts', 'DiffFormPts', 'DiffLP',
          'H2H_Home_pts', 'H2H_Away_pts', 'Mean_home_goals', 'Mean_away_goals',
        'Total_value_H',   'Total_value_A',      'H2H_Diff', 
      'Total_Diff', 'Age_diff', 'LP_Diff']

    cols_sel = np.intersect1d(cols_sel,  df_final.columns)
    

    df_final = df_final[cols_sel]
    
    
    cols_to_int = ["MW", "DiffFormPts", "DiffLP", "HTGD",  "ATGD",  "HT_LP", "AT_LP", "HTP", "ATP",  "H2H_Home_pts", "H2H_Away_pts"]
    df_final[cols_to_int] = df_final[cols_to_int].astype('int')
    
    
    
    df_final["HTGD_by_MW"] = df_final["HTGD"] / df_final["MW"] 
    df_final["ATGD_by_MW"] = df_final["ATGD"] / df_final["MW"] 
    df_final["HTP_by_MW"] = df_final["HTP"] / df_final["MW"] 
    df_final["ATP_by_MW"] = df_final["ATP"] / df_final["MW"] 
    df_final["HT_Wins_by_MW"] = df_final["HT_Wins"] / (df_final["MW"]-1) 
    df_final["HT_Losses_by_MW"] = df_final["HT_Loss"] / (df_final["MW"]-1) 
    df_final["HT_Draws_by_MW"] = df_final["HT_Draws"] / (df_final["MW"]-1) 
    df_final["AT_Wins_by_MW"] = df_final["AT_Wins"] / (df_final["MW"]-1) 
    df_final["AT_Losses_by_MW"] = df_final["AT_Loss"] / (df_final["MW"]-1)  
    df_final["AT_Draws_by_MW"] = df_final["AT_Draws"] / (df_final["MW"]-1) 

    df_final["Goals_mean_diff"] = df_final["Mean_home_goals"] - df_final["Mean_away_goals"]
    
    
    cols_final = ['HomeTeam', 'AwayTeam','HT_LP', 'AT_LP', 
           'HTWinStreak3', 'HTWinStreak5', 'HTLossStreak3', 'HTLossStreak5',
           'ATWinStreak3', 'ATWinStreak5', 'ATLossStreak3', 'ATLossStreak5',
           'DiffPts', 'DiffFormPts', 'DiffLP',
           'Mean_away_goals',  'H2H_Diff',
                   'HT_Wins_by_MW', 'HT_Losses_by_MW', 'HT_Draws_by_MW', 'AT_Wins_by_MW', 'AT_Losses_by_MW', 'AT_Draws_by_MW',
             'Total_Diff', 'Age_diff', 'LP_Diff', 'HTGD_by_MW', 'ATGD_by_MW',
           'Goals_mean_diff', 'HM1_D', 'HM1_L', 'HM1_W',
           'HM2_D', 'HM2_L', 'HM2_W', 'AM1_D', 'AM1_L', 'AM1_W', 
           'AM2_D',        'AM2_L',
           'AM2_W', 'HM3_D', 'HM3_L', 'HM3_W', 'HM4_D', 'HM4_L', 'HM4_W', 'HM5_D',
           'HM5_L', 'HM5_W', 'AM3_D', 'AM3_L', 'AM3_W', 'AM4_D', 'AM4_L',
           'AM4_W', 'AM5_D', 'AM5_L', 'AM5_W']
    

    cols_final = np.intersect1d(cols_final,  df_final.columns)
    

    data_final = df_final[cols_final]


    return data_final



