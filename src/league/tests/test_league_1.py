import unittest
import datetime

from src.league.competition import Competition
from src.league.league import League
from src.league.team import Team
from src.league.team_member import TeamMember
from src.league.exception_duplicate_email import DuplicateEmail
from src.league.exception_duplicate_oid import DuplicateOid


class LeagueTests1(unittest.TestCase):
    """STUDENT MADE TESTS"""
    def test_create(self):
        oid = 13
        name = "Da Best League"
        league = League(oid, name)
        self.assertEqual(oid, league.oid)
        self.assertEqual(name, league.name)
        self.assertEqual([], league.teams)
        self.assertEqual([], league.competitions)

    def test_equality_based_on_id(self):
        """SPEC: two IndentifiedObjects are equal if they have the same type and the same oid"""
        l1 = League(1, "name")
        l2 = League(1, "other name")
        l3 = League(2, "name")
        t1 = Team(1, "what?")
        # must be equal to themselves
        self.assertTrue(l1 == l1)
        self.assertTrue(l2 == l2)
        self.assertTrue(l3 == l3)
        # same id are equal, even if other fields different
        self.assertTrue(l1 == l2)
        # different ids are not equal, even if other fields the same
        self.assertTrue(l1 != l3)
        # different type, same id
        self.assertTrue(t1 != l1)

    def test_hash_based_on_id(self):
        """SPEC: return hash code based on object's oid"""
        l1 = League(1, "name")
        l2 = League(1, "other name")
        l3 = League(2, "name")
        # hash depends only on id
        self.assertTrue(hash(l1) == hash(l2))
        self.assertTrue(hash(l1) == hash(l1))

        # objects with different id's may have different hash codes
        self.assertTrue(hash(l1) != hash(l3))

    def test_adding_teams(self):
        """SPEC: add team to the teams collection
        unless they are already in it (in which case do nothing)"""
        t1 = Team(1, "Havocs")
        t2 = Team(2, "Jailbirds")
        t3 = Team(3, "Havocs")
        league = League(3, "AL State Curling League")
        self.assertEqual(0, len(league.teams))
        self.assertNotIn(t1, league.teams)
        league.add_team(t1)
        self.assertEqual(1, len(league.teams))
        league.add_team(t2)
        self.assertIn(t1, league.teams)
        self.assertIn(t2, league.teams)
        self.assertEqual(2, len(league.teams))
        # Testing DuplicateOid Exception
        with self.assertRaises(DuplicateOid):
            league.add_team(t1)
        self.assertEqual(2, len(league.teams))
        league.add_team(t3)
        self.assertEqual(3, len(league.teams))

    def test_removing_teams(self):
        """SPEC: remove the team if they are in the teams list,
        otherwise do nothing"""
        t1 = Team(1, "Havocs")
        t2 = Team(2, "Jailbirds")
        t3 = Team(3, "Bananas")
        league = League(4, "AL State Curling League")
        league.add_team(t1)
        league.add_team(t2)
        league.add_team(t3)
        c1 = Competition(1, [t1], "Here", None)
        league.add_competition(c1)
        with self.assertRaises(ValueError):
            league.remove_team(t1)
        self.assertEqual(3, len(league.teams))
        league.remove_team(t2)
        self.assertEqual(2, len(league.teams))
        self.assertNotIn(t2, league.teams)
        self.assertIn(t1, league.teams)
        self.assertIn(t3, league.teams)
        league.remove_team(t2)
        self.assertEqual(2, len(league.teams))
        self.assertNotIn(t2, league.teams)
        league.remove_team(t3)
        self.assertEqual(1, len(league.teams))
        self.assertNotIn(t3, league.teams)
        self.assertIn(t1, league.teams)
        league.remove_team(t3)
        league.remove_team(t2)
        self.assertEqual(1, len(league.teams))
        self.assertNotIn(t3, league.teams)

    def test_team_named(self):
        """SPEC: return the team in this league whose name equals
        team_name (case-sensitive) or None if no such team exists"""
        t1 = Team(1, "Havocs")
        t2 = Team(2, "Jailbirds")
        league = League(4, "AL State Curling League")
        league.add_team(t1)
        league.add_team(t2)
        self.assertEqual(t1, league.team_named("Havocs"))
        self.assertEqual(t2, league.team_named("Jailbirds"))
        self.assertIsNone(league.team_named("havocs"))
        self.assertIsNone(league.team_named("HAVOCS"))
        self.assertIsNone(league.team_named("jailbirds"))
        self.assertIsNone(league.team_named("Jail birds"))

    def test_teams_for_member_method(self):
        """SPEC: return a list of all teams for which a member plays."""
        tm1 = TeamMember(1, "Fred", "fred")
        tm2 = TeamMember(2, "Barney", "barney")
        tm3 = TeamMember(3, "Wilma", "wilma")

        t1 = Team(1, "t1")
        t2 = Team(2, "t2")
        t3 = Team(3, "t3")
        t1.add_member(tm2)
        t1.add_member(tm1)
        t2.add_member(tm1)
        t3.add_member(tm1)
        league = League(1, "Some league")
        league.add_team(t1)
        league.add_team(t2)
        league.add_team(t3)

        # Test for team member on 1 team
        self.assertIn(t1, league.teams_for_member(tm2))
        self.assertNotIn(t2, league.teams_for_member(tm2))
        self.assertNotIn(t3, league.teams_for_member(tm2))
        self.assertEqual(1, len(league.teams_for_member(tm2)))

        # Test for team member on all teams
        self.assertIn(t1, league.teams_for_member(tm1))
        self.assertIn(t2, league.teams_for_member(tm1))
        self.assertIn(t3, league.teams_for_member(tm1))
        self.assertEqual(3, len(league.teams_for_member(tm1)))

        # Test for team member on no teams
        self.assertNotIn(t1, league.teams_for_member(tm3))
        self.assertNotIn(t2, league.teams_for_member(tm3))
        self.assertNotIn(t3, league.teams_for_member(tm3))
        self.assertEqual(0, len(league.teams_for_member(tm3)))

    def test_competitions_for_team(self):
        """SPEC: return a list of all competitions in
        which team is participating"""
        league = League(1, "Some league")
        t1 = Team(1, "t1")
        t2 = Team(2, "t2")
        t3 = Team(3, "t3")
        t4 = Team(4, "t4")
        all_teams = [t1, t2, t3, t4]
        for team in all_teams:
            league.add_team(team)
        now = datetime.datetime.now()
        c1 = Competition(1, [t1, t2], "Here", None)
        c2 = Competition(2, [t1, t2], "There", now)
        c3 = Competition(3, [t1, t4], "There", now)
        all_comp = [c1, c2, c3]
        for comp in all_comp:
            league.add_competition(comp)
        # Test three competitions for team
        self.assertIn(c1, league.competitions_for_team(t1))
        self.assertIn(c2, league.competitions_for_team(t1))
        self.assertIn(c3, league.competitions_for_team(t1))
        # Test one competition for team
        self.assertIn(c3, league.competitions_for_team(t4))
        self.assertNotIn(c2, league.competitions_for_team(t4))
        self.assertNotIn(c1, league.competitions_for_team(t4))
        # Test no competitions for team
        self.assertNotIn(c1, league. competitions_for_team(t3))
        self.assertNotIn(c2, league.competitions_for_team(t3))
        self.assertNotIn(c3, league.competitions_for_team(t3))

    def test_competitions_for_member(self):
        """SPEC: return a list of all competitions for which member
        played on one of the competing teams"""
        league = League(1, "Some league")
        t1 = Team(1, "t1")
        t2 = Team(2, "t2")
        t3 = Team(3, "t3")
        t4 = Team(4, "t4")
        tm1 = TeamMember(1, "Fred", "fred")
        tm2 = TeamMember(2, "Fred", "fred")
        tm3 = TeamMember(3, "Wilma", "wilma")
        tm4 = TeamMember(4, "Barney", "barney")
        t1.add_member(tm1)
        with self.assertRaises(DuplicateEmail):
            t1.add_member(tm2)
        t2.add_member(tm2)
        t3.add_member(tm2)
        t4.add_member(tm2)
        t4.add_member(tm4)
        t3.add_member(tm3)
        all_teams = [t1, t2, t3, t4]
        for team in all_teams:
            league.add_team(team)
        now = datetime.datetime.now()
        c1 = Competition(1, [t1, t2], "Here", None)
        c2 = Competition(2, [t1, t2], "There", now)
        c3 = Competition(3, [t1, t4], "There", now)
        all_comp = [c1, c2, c3]
        for comp in all_comp:
            league.add_competition(comp)
        # Test three competitions for member
        self.assertIn(c1, league.competitions_for_member(tm1))
        self.assertIn(c2, league.competitions_for_member(tm1))
        self.assertIn(c3, league.competitions_for_member(tm1))
        # Test one competition for member
        self.assertIn(c3, league.competitions_for_member(tm4))
        self.assertNotIn(c2, league.competitions_for_member(tm4))
        self.assertNotIn(c1, league.competitions_for_member(tm4))
        # Test no competition for member
        self.assertNotIn(c1, league.competitions_for_team(tm3))
        self.assertNotIn(c2, league.competitions_for_team(tm3))
        self.assertNotIn(c3, league.competitions_for_team(tm3))

    def test_str_and_duplicate_email(self):
        """SPEC: return a string resembling the following:
        'League Name: N teams, M competitions' where N and M
        are replaced by the obvious values"""
        league = League(1, "Some league")
        self.assertEqual("Some league: 0 teams, 0 competitions", str(league))
        t1 = Team(1, "t1")
        t2 = Team(2, "t2")
        league.add_team(t1)
        self.assertEqual("Some league: 1 teams, 0 competitions", str(league))
        tm1 = TeamMember(1, "Fred", "fred")
        tm2 = TeamMember(2, "Fred", "fred")
        t2.add_member(tm1)
        with self.assertRaises(DuplicateEmail):
            t2.add_member(tm2)
        league.add_team(t2)
        self.assertEqual("Some league: 2 teams, 0 competitions", str(league))
        now = datetime.datetime.now()
        c1 = Competition(1, [t1, t2], "Here", None)
        c2 = Competition(2, [t1, t2], "There", now)
        league.add_competition(c1)
        self.assertEqual("Some league: 2 teams, 1 competitions", str(league))
        league.add_competition(c2)
        self.assertEqual("Some league: 2 teams, 2 competitions", str(league))
        with self.assertRaises(ValueError):
            league.remove_team(t1)
        self.assertEqual("Some league: 2 teams, 2 competitions", str(league))

    def test_add_competitions_duplicate_oid_and_value_error(self):
        league = League(1, "Some league")
        t1 = Team(1, "t1")
        t2 = Team(2, "t2")
        tm1 = TeamMember(1, "Fred", "fred")
        tm2 = TeamMember(2, "Fred", "fredd")
        t1.add_member(tm1)
        league.add_team(t1)
        now = datetime.datetime.now()
        c1 = Competition(1, [t1, t2], "Here", None)
        c2 = Competition(1, [t1, t2], "There", now)
        with self.assertRaises(ValueError):
            league.add_competition(c1)
        league.add_team(t2)
        t2.add_member(tm2)
        league.add_competition(c2)
        with self.assertRaises(DuplicateOid):
            league.add_competition(c2)


if __name__ == '__main__':
    unittest.main()
