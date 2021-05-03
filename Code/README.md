Data Mining Group Project

This project is designed to make soccer match predictions using the decision tree data minning algorithm. A GUI is also designed with pyQt5 to make it more interactive.

The dataset is large and exceeds the github file upload size therefore the dataset is found on this link https://drive.google.com/file/d/1nJ-AvjMkAY0e8tV3iONIcE96psd1eiVi/view?usp=sharing

1.The codes are in the DATS6103 folder. To successfully execute the program,make sure you have skilearn library and the pyqt5 library installed on your python enviroment you need to make sure you are using the correct link to the dataset in the database.py and the team_formations.py.

2.When the dataset link is correct, you run the main.py file.

3.When you run the main.py file, it populates the GUI with all the required information from the database.py file. the country, leagues and teams are all populated and are triggered based on a selection from either.

4.The user is expected to select a home and away team.

5.After the teams are selected, the program generates the predictor variables and the target variables from the database.py file from the get_match_predictors and get_team_predictors methods respectively.

6.The program now uses the skilearn decision tree classifier model to train, fit and predit the match outcome.

7.The results of the match outcome, teams formation and the accuracy of the prediction is now dislayed on the GUI.

8.To predict with another set of teams, you simply change the teams from the combo. If you want to cancel or stop the program you can use the cancel button or the window cancel icon.
