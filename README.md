# tennis-glicko

generates glicko2 ratings from tennis results database

### ./settings.json

requires one object with variables data_path, rating_path, sql_user, sql_host, sql_password, and rating_period.

#### data_path and rating_path

data_path and rating_path should both be strings with no slash at the end.

#### sql_*

login information for the mysql server

#### rating_period

length of rating period, in weeks, as an integer.

### glicko/config.json

requires one object with variables columns and datatypes, both lists.

at minimum, must include tourney_date (date), winner_id (int), loser_id (int), and score (char).