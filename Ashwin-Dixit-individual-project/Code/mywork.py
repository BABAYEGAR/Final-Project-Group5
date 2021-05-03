def get_match_predictors():
    query = f'SELECT  CASE  WHEN home_team_goal > away_team_goal THEN 1 	WHEN home_team_goal < away_team_goal THEN 2 	' \
            f'ELSE 0 END AS Match_Outcome, ht_buildUpPlaySpeed, ht_buildUpPlayDribbling, ht_buildUpPlayPassing, ht_chanceCreationPassing, ht_chanceCreationCrossing,' \
            f' ht_chanceCreationShooting, ht_defencePressure, ht_defenceAggression, ht_defenceTeamWidth, at_buildUpPlaySpeed, at_buildUpPlayDribbling, at_buildUpPlayPassing,' \
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
            f' at_buildUpPlaySpeed, at_buildUpPlayDribbling, at_buildUpPlayPassing, at_chanceCreationPassing, at_chanceCreationCrossing, at_chanceCreationShooting, at_defencePressure, at_defenceAggression, at_defenceTeamWidth ' \
            f' FROM   (SELECT 	AVG(buildUpPlaySpeed) AS ht_buildUpPlaySpeed, AVG(buildUpPlayDribbling) AS ht_buildUpPlayDribbling, AVG(buildUpPlayPassing) AS ht_buildUpPlayPassing,AVG(chanceCreationPassing) AS ht_chanceCreationPassing, ' \
            f'AVG(chanceCreationCrossing) AS ht_chanceCreationCrossing, AVG(chanceCreationShooting) AS ht_chanceCreationShooting, 	 	' \
            f'AVG(defencePressure) AS ht_defencePressure, AVG(defenceAggression) AS ht_defenceAggression, AVG(defenceTeamWidth) AS ht_defenceTeamWidth 	 	FROM Team_Attributes home_attr 	JOIN Team home_team ' \
            f'	ON home_attr.team_api_id =  home_team.team_api_id ' \
            f'	WHERE team_long_name = "{home_team_name}" ) ht_attr  JOIN   ( 	 ' \
            f'	SELECT  AVG(buildUpPlaySpeed) AS at_buildUpPlaySpeed, AVG(buildUpPlayDribbling) AS at_buildUpPlayDribbling, AVG(buildUpPlayPassing) AS at_buildUpPlayPassing, 	 	AVG(chanceCreationPassing) ' \
            f'AS at_chanceCreationPassing, AVG(chanceCreationCrossing) AS at_chanceCreationCrossing,' \
            f' AVG(chanceCreationShooting) AS at_chanceCreationShooting, 	 AVG(defencePressure) AS at_defencePressure, AVG(defenceAggression) AS at_defenceAggression, AVG(defenceTeamWidth) AS at_defenceTeamWidth 	 	' \
            f'FROM Team_Attributes away_attr 	JOIN Team away_team 	ON away_attr.team_api_id =  away_team.team_api_id 	WHERE team_long_name = "{away_team_name}" ) at_attr  ON 1=1  ;'
    return pd.read_sql(query, con)
	
	

def analyzeMatch(self):
    home_team = str(self.homeTeamComboBox.currentText())
    away_team = str(self.awayTeamComboBox.currentText())
    self.figure.clear()
    team_formations.team_formation(home_team, away_team)
    self.canvas.draw()
    match_predictors_variables = database.get_match_predictors()
    match_predictors_variables = match_predictors_variables.dropna()
    teams_predictor_variables = database.get_team_predictors(home_team, away_team).fillna(0)
    X = match_predictors_variables.values[:, 1:19]
    y = match_predictors_variables.values[:, 0]
    p = teams_predictor_variables.values[:, 0:18]
    clf = DecisionTreeClassifier(criterion="gini")
    clf.fit(X, y)
    y_pred = clf.predict(p)
    report = classification_report(numpy.full(len(y), y_pred), y)
    if y_pred == 1:
        outcome = home_team + " (Home team) wins"
    elif y_pred == 2:
        outcome = away_team + " (Away team) wins"
    else:
        outcome = "Draw"
    self.result.setPlainText(outcome)
    self.result.appendPlainText(report)
	
	
	
def team_formation(home_team_name, away_team_name):


	con.row_factory = sqlite3.Row
	cur = con.cursor()

	sql = f'SELECT h.home_player_1, h.home_player_2, h.home_player_3, h.home_player_4, h.home_player_5, h.home_player_6, ' \
		  f'h.home_player_7, h.home_player_8, h.home_player_9, h.home_player_10, h.home_player_11,  ' \
		  f'a.away_player_1, a.away_player_2, a.away_player_3, a.away_player_4, a.away_player_5, a.away_player_6, ' \
		  f'a.away_player_7, a.away_player_8, a.away_player_9, a.away_player_10, a.away_player_11, ' \
		  f'h.home_player_X1, h.home_player_X2, h.home_player_X3, h.home_player_X4, h.home_player_X5, h.home_player_X6, ' \
		  f'h.home_player_X7, h.home_player_X8, h.home_player_X9, h.home_player_X10, h.home_player_X11, ' \
		  f'h.home_player_Y1, h.home_player_Y2, h.home_player_Y3, h.home_player_Y4, h.home_player_Y5, h.home_player_Y6, ' \
		  f'h.home_player_Y7, h.home_player_Y8, h.home_player_Y9, h.home_player_Y10, h.home_player_Y11,  ' \
		  f'a.away_player_X1, a.away_player_X2, a.away_player_X3, a.away_player_X4, a.away_player_X5, a.away_player_X6, ' \
		  f'a.away_player_X7, a.away_player_X8, a.away_player_X9, a.away_player_X10, a.away_player_X11,  ' \
		  f'a.away_player_Y1, a.away_player_Y2, a.away_player_Y3, a.away_player_Y4, a.away_player_Y5, a.away_player_Y6, ' \
		  f'a.away_player_Y7, a.away_player_Y8, a.away_player_Y9, a.away_player_Y10, a.away_player_Y11 ' \
		  f'FROM  ' \
		  f'(     SELECT *      FROM Match      WHERE id = (SELECT MAX(m.id) FROM Match m JOIN Team ht ON m.home_team_api_id = ht.team_api_id AND ht.team_long_name = "{home_team_name}") ) h ' \
		  f'JOIN  ' \
		  f'(     SELECT *     FROM Match      WHERE id = (SELECT MAX(m.id) FROM Match m JOIN Team at ON m.away_team_api_id = at.team_api_id AND at.team_long_name = "{away_team_name}") ) a ' \
		  f'ON 1=1;'
	cur.execute(sql)
	match = cur.fetchone()

	# list init
	home_players_api_id = list()
	away_players_api_id = list()
	home_players_x = list()
	away_players_x = list()
	home_players_y = list()
	away_players_y = list()

	for i in range(1, 12):
		home_players_api_id.append(match['home_player_' + str(i)])
		away_players_api_id.append(match['away_player_' + str(i)])
		home_players_x.append(match['home_player_X' + str(i)])
		away_players_x.append(match['away_player_X' + str(i)])
		home_players_y.append(match['home_player_Y' + str(i)])
		away_players_y.append(match['away_player_Y' + str(i)])

	# Fetch players'names
	players_api_id = [home_players_api_id, away_players_api_id]
	players_names = [[None] * 11, [None] * 11]

	for i in range(2):
		players_api_id_not_none = [x for x in players_api_id[i] if x is not None]
		sql = 'SELECT player_api_id,player_name FROM Player WHERE player_api_id IN (' + ','.join(
			map(str, players_api_id_not_none)) + ')'
		cur.execute(sql)
		players = cur.fetchall()
		for player in players:
			idx = players_api_id[i].index(player['player_api_id'])
			name = player['player_name'].split()[-1]  # keep only the last name
			players_names[i][idx] = name

	# Goalkeeper X axis center positions
	home_players_x = [5 if x == 1 else x for x in home_players_x]
	away_players_x = [5 if x == 1 else x for x in away_players_x]

	# Home team
	plt.subplot(2, 1, 1, facecolor='seagreen')
	plt.rc('figure', figsize=(9, 6))
	plt.xlim(1, 9)
	plt.ylim(-1, 12)
	plt.gca().add_patch(patches.Rectangle([3.5, -1], width=3, height=3.25, fill=False))
	plt.gca().add_patch(patches.Rectangle([4.5, -1], width=1, height=1.2, fill=False))
	plt.gca().add_patch(patches.Arc([5, 12], height=4, width=1, angle=0, theta1=180, theta2=360, color="black"))
	plt.gca().add_patch(patches.Arc([5, 2.25], height=2.5, width=1, angle=0, theta1=360, theta2=180, color="black"))
	plt.gca().invert_yaxis()  # for having GK first
	for label, x, y in zip(players_names[0], home_players_x, home_players_y):
		plt.annotate(
			label,
			xy=(x, y), xytext=(-20, 10),
			textcoords='offset points', va='bottom')
	plt.scatter(home_players_x, home_players_y, s=150, c='midnightblue')
	plt.tick_params(bottom=False, labelbottom=False, left=False, labelleft=False)

	# Away team
	plt.subplot(2, 1, 2, facecolor='seagreen')
	plt.rc('figure', figsize=(9, 6))
	plt.xlim(1, 9)
	plt.ylim(-1, 12)
	plt.gca().add_patch(patches.Rectangle([3.5, -1], width=3, height=3.25, fill=False))
	plt.gca().add_patch(patches.Rectangle([4.5, -1], width=1, height=1.2, fill=False))
	plt.gca().add_patch(patches.Arc([5, 12], height=4, width=1, angle=0, theta1=180, theta2=360, color="black"))
	plt.gca().add_patch(patches.Arc([5, 2.25], height=2.5, width=1, angle=0, theta1=360, theta2=180, color="black"))
	plt.gca().invert_xaxis()  # Invert x axis for right wingers
	for label, x, y in zip(players_names[1], away_players_x, away_players_y):
		plt.annotate(
			label,
			xy=(x, y), xytext=(-20, -20),
			textcoords='offset points', va='bottom')
	plt.scatter(away_players_x, away_players_y, s=150, c='darkred')
	plt.tick_params(bottom=False, labelbottom=False, left=False, labelleft=False)

	plt.subplots_adjust(wspace=0, hspace=0)
	plt.plot()