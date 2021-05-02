import sqlite3
import pandas as pd

con = sqlite3.connect("soccer.sqlite")
cur = con.cursor()


def get_all_countries():
    return pd.read_sql('SELECT * FROM Country;', con)

def get_country_leagues(country_name):
    query = f'SELECT DISTINCT l.name FROM League l ' \
            f'JOIN Country c ON l.country_id = c.id ' \
            f'WHERE c.name =  "{country_name}" ORDER BY l.name ASC'
    return pd.read_sql(query, con)

def get_league_teams(league_name):
    query = f'SELECT DISTINCT l.name , t.team_long_name FROM Match m  JOIN League l ' \
            f'ON m.league_id = l.id  JOIN Team t  ON m.home_team_api_id = t.team_api_id WHERE' \
            f' l.name = "{league_name}"' \
            f'ORDER BY t.team_long_name ASC;'
    return pd.read_sql(query, con)


def get_match_predictors():
    query = f'SELECT  CASE  WHEN home_team_goal > away_team_goal THEN 1 	WHEN home_team_goal < away_team_goal THEN 2 	' \
            f'ELSE 0 END AS Match_Outcome, ht_buildUpPlaySpeed, ht_buildUpPlayDribbling, ht_buildUpPlayPassing, ht_chanceCreationPassing, ht_chanceCreationCrossing,' \
            f' ht_chanceCreationShooting, ht_defencePressure, ht_defenceAggression, ht_defenceTeamWidth, at_buildUpPlaySpeed, at_buildUpPlayDribbling,' \
            f' at_buildUpPlayPassing,' \
            f'at_chanceCreationPassing, at_chanceCreationCrossing, at_chanceCreationShooting, at_defencePressure, at_defenceAggression, at_defenceTeamWidth ' \
            f'FROM Match m JOIN  ( 	SELECT team_api_id,	AVG(buildUpPlaySpeed) AS ht_buildUpPlaySpeed,' \
            f'AVG(buildUpPlayDribbling) AS ht_buildUpPlayDribbling, AVG(buildUpPlayPassing) AS ht_buildUpPlayPassing, 	' \
            f'AVG(chanceCreationPassing) AS ht_chanceCreationPassing, AVG(chanceCreationCrossing) AS ht_chanceCreationCrossing,' \
            f'AVG(chanceCreationShooting) AS ht_chanceCreationShooting,' \
            f'AVG(defencePressure) AS ht_defencePressure, ' \
            f'AVG(defenceAggression) AS ht_defenceAggression, AVG(defenceTeamWidth) AS ht_defenceTeamWidth 	FROM Team_Attributes' \
            f' GROUP BY team_api_id ) ht_attr ON ht_attr.team_api_id = home_team_api_id JOIN  ' \
            f'(SELECT team_api_id, AVG(buildUpPlaySpeed) AS at_buildUpPlaySpeed, AVG(buildUpPlayDribbling)' \
            f' AS at_buildUpPlayDribbling, AVG(buildUpPlayPassing) AS at_buildUpPlayPassing, 	 	' \
            f'AVG(chanceCreationPassing) AS at_chanceCreationPassing, AVG(chanceCreationCrossing)' \
            f' AS at_chanceCreationCrossing, AVG(chanceCreationShooting) AS at_chanceCreationShooting, 	 ' \
            f'	AVG(defencePressure) AS at_defencePressure, AVG(defenceAggression) AS at_defenceAggression, ' \
            f'AVG(defenceTeamWidth) AS at_defenceTeamWidth 	FROM Team_Attributes 	GROUP BY team_api_id ) ' \
            f' at_attr ON at_attr.team_api_id = away_team_api_id;'
    return pd.read_sql(query, con)


def get_team_predictors(home_team_name, away_team_name):
    query = f'SELECT   ht_buildUpPlaySpeed, ht_buildUpPlayDribbling, ht_buildUpPlayPassing, ht_chanceCreationPassing,' \
            f' ht_chanceCreationCrossing, ht_chanceCreationShooting, ht_defencePressure, ht_defenceAggression, ht_defenceTeamWidth, ' \
            f' at_buildUpPlaySpeed, at_buildUpPlayDribbling, at_buildUpPlayPassing, at_chanceCreationPassing, at_chanceCreationCrossing, at_chanceCreationShooting, ' \
            f'at_defencePressure, at_defenceAggression, at_defenceTeamWidth ' \
            f' FROM   (SELECT 	AVG(buildUpPlaySpeed) AS ht_buildUpPlaySpeed, AVG(buildUpPlayDribbling) AS ht_buildUpPlayDribbling, AVG(buildUpPlayPassing) ' \
            f'AS ht_buildUpPlayPassing,AVG(chanceCreationPassing) AS ht_chanceCreationPassing, ' \
            f'AVG(chanceCreationCrossing) AS ht_chanceCreationCrossing, AVG(chanceCreationShooting) AS ht_chanceCreationShooting, 	 	' \
            f'AVG(defencePressure) AS ht_defencePressure, AVG(defenceAggression) AS ht_defenceAggression, AVG(defenceTeamWidth) AS ht_defenceTeamWidth 	 	' \
            f'FROM Team_Attributes home_attr 	JOIN Team home_team ' \
            f'	ON home_attr.team_api_id =  home_team.team_api_id ' \
            f'	WHERE team_long_name = "{home_team_name}" ) ht_attr  JOIN   ( 	 ' \
            f'	SELECT  AVG(buildUpPlaySpeed) AS at_buildUpPlaySpeed, AVG(buildUpPlayDribbling) AS at_buildUpPlayDribbling, AVG(buildUpPlayPassing) ' \
            f'AS at_buildUpPlayPassing, 	 	AVG(chanceCreationPassing) ' \
            f'AS at_chanceCreationPassing, AVG(chanceCreationCrossing) AS at_chanceCreationCrossing,' \
            f' AVG(chanceCreationShooting) AS at_chanceCreationShooting, 	 AVG(defencePressure) AS at_defencePressure, AVG(defenceAggression) ' \
            f'AS at_defenceAggression, AVG(defenceTeamWidth) AS at_defenceTeamWidth 	 	' \
            f'FROM Team_Attributes away_attr 	JOIN Team away_team 	ON away_attr.team_api_id =  away_team.team_api_id 	' \
            f'WHERE team_long_name = "{away_team_name}" ) at_attr  ON 1=1  ;'
    return pd.read_sql(query, con)



