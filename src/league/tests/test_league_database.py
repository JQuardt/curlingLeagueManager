import unittest
import os.path
from src.league.league_database import LeagueDatabase
from src.league.league import League


class TestingLeagueDatabase(unittest.TestCase):

    def test_create(self):
        league_db1 = LeagueDatabase()
        self.assertIsNotNone(league_db1)

    def test_add_league(self):
        league = League(1, "AL State Curling League")
        league_db = LeagueDatabase()
        league_db.add_league(league)
        self.assertEqual(league_db.leagues[0], league)

    def test_league_named(self):
        league = League(1, "AL State Curling League")
        league_db = LeagueDatabase()
        league_db.add_league(league)
        self.assertTrue(league_db.league_named("AL State Curling League"))
        self.assertIsNone(league_db.league_named("Not a curling league"))

    def test_remove_league(self):
        league = League(1, "AL State Curling League")
        league_db = LeagueDatabase()
        league_db.remove_league(league)
        self.assertEqual(0, len(league_db.leagues))
        league_db.remove_league(league)
        self.assertEqual(0, len(league_db.leagues))

    def test_next_oid(self):
        league_db = LeagueDatabase()
        self.assertEqual(1, league_db.next_oid())
        self.assertEqual(2, league_db.next_oid())
        self.assertEqual(3, league_db.next_oid())

    def test_import_teams_csv(self):
        league_db = LeagueDatabase()
        league = League(league_db.next_oid(), "Test League")
        league = league_db.import_league_teams(league, "Teams.csv")
        league_db.add_league(league)
        self.assertTrue(league.team_named("Flintstones"))
        self.assertTrue(league.team_named("Curl Jam"))
        self.assertTrue(league.team_named("Curl Power"))
        self.assertTrue(league.team_named("Cold Fingers"))
        self.assertTrue(league_db.league_named("Test League"))
        self.assertEqual("Test League: 4 teams, 0 competitions", str(league))

    def test_export_teams_csv(self):
        league_db = LeagueDatabase()
        league = League(league_db.next_oid(), "Test League")
        league = league_db.import_league_teams(league, "Teams.csv")
        file_name = "Export_test.csv"
        league_db.export_league_teams(league, file_name)
        self.assertTrue(os.path.isfile(file_name))

    def test_save_and_load_db(self):
        league_db = LeagueDatabase()
        league = League(league_db.next_oid(), "Test League")
        league = league_db.import_league_teams(league, "Teams.csv")
        league_db.add_league(league)
        league_db.save("pickled_db.dat")
        LeagueDatabase.load("pickled_db.dat")
        # LeagueDatabase.load("notafile.dat")
        league_db1 = LeagueDatabase.instance()
        league = league_db1.league_named("Test League")
        self.assertTrue(league.team_named("Flintstones"))
        self.assertTrue(league.team_named("Curl Jam"))
        self.assertTrue(league.team_named("Curl Power"))
        self.assertTrue(league.team_named("Cold Fingers"))


if __name__ == '__main__':
    unittest.main()
