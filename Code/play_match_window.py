import warnings
import numpy
import pandas as pd
from PyQt5.QtWidgets import *
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from sklearn.metrics import classification_report
from sklearn.tree import DecisionTreeClassifier
import database
import team_formations
warnings.filterwarnings('ignore')
pd.options.mode.chained_assignment = None
class play_match_window(QDialog):
    def __init__(self):
        super(play_match_window, self).__init__()
        self.setWindowTitle("DATS6103 GROUP PROJECT - TEAM 3 (SOCCER MATCH PREDICTION)")
        self.setFixedWidth(800)
        self.setFixedHeight(1000)
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        self.formGroupBox = QGroupBox("PREDICT SOCCER MATCH")
        self.homeTeamCountryComboBox = QComboBox()
        self.awayTeamCountryComboBox = QComboBox()
        self.homeTeamLeagueComboBox = QComboBox()
        self.awayTeamLeagueComboBox = QComboBox()
        self.homeTeamComboBox = QComboBox()
        self.awayTeamComboBox = QComboBox()
        self.result = QPlainTextEdit()
        self.result.setFixedWidth(500)
        self.result.setFixedHeight(200)
        self.result.setDisabled(True)
        self.homeTeamCountryComboBox.addItems(database.get_all_countries().name)
        self.homeTeamCountryComboBox.currentIndexChanged.connect(self.getHomeCountryLeagues)
        self.homeTeamLeagueComboBox.addItems(
            database.get_country_leagues(self.homeTeamCountryComboBox.currentText()).name)
        self.homeTeamLeagueComboBox.currentIndexChanged.connect(self.getHomeLeagueTeams)
        self.homeTeamComboBox.clear()
        self.homeTeamComboBox.addItems(
            database.get_league_teams(self.homeTeamLeagueComboBox.currentText()).team_long_name)
        self.awayTeamCountryComboBox.addItems(database.get_all_countries().name)
        self.awayTeamCountryComboBox.currentIndexChanged.connect(self.getAwayCountryLeagues)
        self.awayTeamLeagueComboBox.addItems(
            database.get_country_leagues(self.awayTeamCountryComboBox.currentText()).name)
        self.awayTeamLeagueComboBox.currentIndexChanged.connect(self.getAwayLeagueTeams)
        self.awayTeamComboBox.clear()
        self.awayTeamComboBox.addItems(
            database.get_league_teams(self.awayTeamLeagueComboBox.currentText()).team_long_name)
        self.platMatchForm()
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.analyzeMatch)
        self.buttonBox.rejected.connect(self.reject)
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(self.buttonBox)
        mainLayout.addWidget(self.canvas)
        self.setLayout(mainLayout)

    def getHomeCountryLeagues(self):
        self.homeTeamLeagueComboBox.clear()
        self.homeTeamComboBox.clear()
        self.homeTeamLeagueComboBox.addItems(
            database.get_country_leagues(self.homeTeamCountryComboBox.currentText()).name)

    def getAwayCountryLeagues(self):
        self.awayTeamLeagueComboBox.clear()
        self.awayTeamComboBox.clear()
        self.awayTeamLeagueComboBox.addItems(
            database.get_country_leagues(self.awayTeamCountryComboBox.currentText()).name)

    def getHomeLeagueTeams(self):
        self.homeTeamComboBox.clear()
        self.homeTeamComboBox.addItems(
            database.get_league_teams(self.homeTeamLeagueComboBox.currentText()).team_long_name)

    def getAwayLeagueTeams(self):
        self.awayTeamComboBox.clear()
        self.awayTeamComboBox.addItems(
            database.get_league_teams(self.awayTeamLeagueComboBox.currentText()).team_long_name)

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
        y_pred_report = numpy.full(len(y), y_pred)
        report = classification_report(y_pred_report, y)
        if y_pred == 1:
            outcome = home_team + " (Home team) wins"
        elif y_pred == 2:
            outcome = away_team + " (Away team) wins"
        else:
            outcome = "Draw"
        self.result.setPlainText(outcome)
        self.result.appendPlainText(report)

    def platMatchForm(self):
        layout = QFormLayout()
        layout.addRow(QLabel("Home Team Country"), self.homeTeamCountryComboBox)
        layout.addRow(QLabel("Home Team League"), self.homeTeamLeagueComboBox)
        layout.addRow(QLabel("Home Team"), self.homeTeamComboBox)
        layout.addRow(QLabel("VS"))
        layout.addRow(QLabel("Away Team Country"), self.awayTeamCountryComboBox)
        layout.addRow(QLabel("Away Team League"), self.awayTeamLeagueComboBox)
        layout.addRow(QLabel("Away Team"), self.awayTeamComboBox)
        layout.addRow(QLabel("Prediction Results"), self.result)
        self.formGroupBox.setLayout(layout)
