import unittest
import datetime

from src.league.competition import Competition
from src.league.team import Team
from src.league.team_member import TeamMember
from src.league.tests.fake_emailer import FakeEmailer


class CompetitionTests1(unittest.TestCase):
    """STUDENT MADE TESTS"""
    def test_create(self):
        oid = 13
        teams = []
        location = "Da Best League"
        now = datetime.datetime.now()
        c1 = Competition(oid, teams, location, now)
        self.assertEqual(oid, c1.oid)
        self.assertEqual(teams, c1.teams_competing)
        self.assertEqual(location, c1.location)
        self.assertEqual(now, c1.date_time)
        # test no datetime object
        c2 = Competition(oid, teams, location)
        self.assertEqual(oid, c2.oid)
        self.assertEqual(teams, c2.teams_competing)
        self.assertEqual(location, c2.location)
        self.assertEqual(None, c2.date_time)
        # test input of datetime object as String
        c3 = Competition(oid, teams, location, location)
        self.assertEqual(None, c3.date_time)

    def test_hash_based_on_id(self):
        """SPEC: return hash code based on object's oid"""
        tm_1 = TeamMember(9, "name", "email")
        tm_2 = TeamMember(2, "other name", "other email")
        tm_4 = TeamMember(4, "fourth name", "email4")
        now = datetime.datetime.now()
        t1 = Team(9, "Team 1")  # two members
        t3 = Team(7, "Team 3")  # no members
        t4 = Team(8, "Team 4")  # member 4
        t1.add_member(tm_1)
        t1.add_member(tm_2)
        t4.add_member(tm_4)
        c1 = Competition(9, [t1, t3], "There", now)
        c2 = Competition(10, [t1, t3], "There", now)
        c3 = Competition(10, [t1, t4], "Here", None)
        self.assertTrue(hash(c2) == hash(c2))
        self.assertTrue(hash(c1) == hash(c1))
        self.assertTrue(hash(c3) == hash(c3))
        self.assertTrue(hash(c2) == hash(c3))
        self.assertTrue(hash(c1) != hash(c2))

    def test_str(self):
        """SPEC: return a string like the following:
        'Competition at location on date_time with N teams'
        (note: date_time may be None in which case just omit
        the "on date_time" part. If present, format the
        date_time property similar to the following example
        "12/31/1995 19:30".)"""
        date = datetime.datetime(2022, 12, 28, 23, 55, 59, 342380)
        t1 = Team(1, "Team 1")
        t2 = Team(2, "Team 2")
        t3 = Team(3, "Team 3")
        c1 = Competition(1, [t1, t2], "Here", None)
        c2 = Competition(2, [t2, t3, t1], "There", date)
        self.assertEqual("Competition at Here with 2 teams", str(c1))
        self.assertEqual(f"Competition at There on 12/28/2022 23:55 with 3 teams", str(c2))

    def test_sends_email(self):
        """SPEC: use the emailer argument to email all members of all
        teams in this competition without duplicates.  That is,
        a team member may be on multiple teams that may be
        competing against each other. Only send one email to
        each team member on all the teams in this competition.
        This method should send a single email so if the teams
        have N and M members respectively, the recipient list
        will have N+M elements assuming all the members were
        distinct.  If the teams have S "shared" members
        then we'd expect a single email with N+M-S recipients."""
        tm_1 = TeamMember(1, "name", "email")
        tm_2 = TeamMember(2, "other name", "other email")
        tm_3 = TeamMember(3, "third name", "email")
        tm_4 = TeamMember(4, "fourth name", "email4")
        fe = FakeEmailer()
        now = datetime.datetime.now()
        t1 = Team(1, "Team 1")  # two members
        t2 = Team(2, "Team 2")  # repeat emails
        t3 = Team(3, "Team 3")  # no members
        t4 = Team(4, "Team 4")  # member 4
        t1.add_member(tm_1)
        t1.add_member(tm_2)
        t2.add_member(tm_1)
        t2.add_member(tm_2)
        # t2.add_member(tm_3) DuplicateEmail
        t4.add_member(tm_4)
        c1 = Competition(1, [t1, t2], "Here", None)
        c2 = Competition(2, [t1, t3], "There", now)
        c3 = Competition(2, [t1, t4], "There", now)
        c4 = Competition(4, [], "Where?", None)
        # Test for two teams
        c1.send_email(fe, "Foo", "Bar")
        self.assertEqual(["email", "other email"], fe.recipients)
        self.assertEqual("Foo", fe.subject)
        self.assertEqual("Bar", fe.message)
        self.assertEqual(2, len(fe.recipients))
        # Test for repeat
        c2.send_email(fe, "Different", "Ugh")
        self.assertEqual(["email", "other email"], fe.recipients)
        self.assertEqual("Different", fe.subject)
        self.assertEqual("Ugh", fe.message)
        self.assertEqual(2, len(fe.recipients))
        # Test for all emails
        c3.send_email(fe, "More", "Stuff")
        self.assertEqual(["email", "other email", "email4"], fe.recipients)
        self.assertEqual(3, len(fe.recipients))
        # Test for no teams
        c4.send_email(fe, "h", "i")
        self.assertEqual(0, len(fe.recipients))
        self.assertEqual([], fe.recipients)

    def test_equality_based_on_id(self):
        """SPEC: two IndentifiedObjects are equal if they have the same type and the same oid"""
        tm_1 = TeamMember(9, "name", "email")
        tm_2 = TeamMember(2, "other name", "other email")
        tm_4 = TeamMember(4, "fourth name", "email4")
        now = datetime.datetime.now()
        t1 = Team(9, "Team 1")  # two members
        t3 = Team(7, "Team 3")  # no members
        t4 = Team(8, "Team 4")  # member 4
        t1.add_member(tm_1)
        t1.add_member(tm_2)
        t4.add_member(tm_4)
        c1 = Competition(9, [t1, t3], "There", now)
        c2 = Competition(10, [t1, t3], "There", now)
        c3 = Competition(10, [t1, t4], "Here", None)
        # must be equal to themselves
        self.assertTrue(c2 == c2)
        self.assertTrue(c1 == c1)
        self.assertTrue(c3 == c3)
        # same id are equal, even if other fields different
        self.assertTrue(c2 == c3)
        # different ids are not equal, even if other fields the same
        self.assertTrue(c1 != c2)
        # must be same type
        self.assertFalse(c1 == t1)
        self.assertFalse(c1 == tm_1)

    def test_for_optional_datetime(self):
        tm_1 = TeamMember(9, "name", "email")
        tm_2 = TeamMember(2, "other name", "other email")
        t1 = Team(9, "Team 1")  # two members
        t3 = Team(7, "Team 3")  # no members
        t1.add_member(tm_1)
        t1.add_member(tm_2)
        c1 = Competition(9, [t1, t3], "There")
        self.assertTrue(None is c1.date_time)


if __name__ == '__main__':
    unittest.main()
