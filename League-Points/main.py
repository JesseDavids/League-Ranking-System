#running python 3.9.5
#Jesse Davids 
import pandas as pd
import csv
import os
import sys
import numpy as np
filename = sys.argv[1]
if(filename[-3:] != "csv"):
    print("Please select only CSV files, and that your data is in this format.\n"
    "'team one, score one, team two, score two' one game results per line"
    )
    exit()

rows = []
#open csv file
file = 'results.csv'
if(os.path.exists(file) and os.path.isfile(file)):
    os.remove(file)

with open(filename, 'r') as csvfile:
    teams_from_csv = csv.reader(csvfile)
    next(teams_from_csv)
    #add csv items to list
    for row in teams_from_csv:
        rows.append(row)
    
    #expand list description
    for x in rows:
        #print(x)
        team1 = x[0]
        team1score = x[1]
        team2 = x[2]
        team2score = x[3]      

        team1points = 0
        team2points = 0

        #determine amount of points to receive
        if(int(team1score) < int(team2score)):            
            epoints = 0
            team1points = team1points + epoints  
            
        elif(int(team1score) > int(team2score)):
            epoints = 3
            team1points = team1points + epoints 

        elif(int(team1score) == int(team2score)):
            epoints = 1
            team1points = team1points + epoints 
            team2points = team2points + epoints 

        if(int(team2score) < int(team1score)):            
            epoints = 0
            team2points = team2points + epoints
            
        elif(int(team2score) > int(team1score)):
            epoints = 3
            team2points = team2points + epoints             

        res = team1 + " " + str(team1points) 
        res2 = team2 + " " + str(team2points) 

        # points_overview = res + " " + res2
        # list_points_overview = []
        # list_points_overview.append(points_overview)

        team_and_points_list = []
        team_and_points_list.append(res)
        team_and_points_list.append(res2)

        for x in team_and_points_list:
            points = x[len(x)-1:]
            teams = x[:-1]
            fieldnames = ['Team', 'Points']
            data = [{'Team':teams, 'Points':points}]            
            with open('results.csv', 'a+', encoding='UTF8', newline='') as f:
                # create the csv writer
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writerows(data)
    
#push csv data to pandas dataframe
df = pd.read_csv('results.csv', delimiter=',', names=["Team", "Points"])
#group by teams and sum by points
df_new = df.groupby('Team')['Points'].sum()
#sort values from descending
final_points = df_new.sort_values(axis=0, ascending=False)
#get rank of each team
rank = final_points.rank(axis=0, method='dense', numeric_only=True, na_option='top', ascending=False)
print(str(final_points))
print("----------------------------")
print(str(rank.astype(np.int64)))