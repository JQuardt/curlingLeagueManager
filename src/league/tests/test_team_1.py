import unittest

from src.league.team import Team
from src.league.team_member import TeamMember
from src.league.tests.fake_emailer import FakeEmailer
from src.league.exception_duplicate_oid import DuplicateOid
from src.league.exception_duplicate_email import DuplicateEmail


class TeamTests1(unittest.TestCase):
    """STUDENT MADE TESTS"""
    def test_create(self):
        """SPEC: initialization method that sets the oid,
        name and email properties as specified in the arguments
        (note: should call superclass constructor)"""
        name = "Curl Jam"
        oid = 10
        t = Team(oid, name)
        self.assertEqual([], t.members)

    def test_equality_based_on_id(self):
        """SPEC: two IndentifiedObjects are equal if they have the same type and the same oid"""
        t1 = Team(1, "Team 1")
        t2 = Team(2, "Team 1")
        t3 = Team(2, "Team 4")
        tm_1 = TeamMember(1, "Team 1", "email")
        self.assertEqual(t1, t1)
        self.assertTrue(t2 == t3)   # Test oid, diff. name
        self.assertFalse(t1 == t2)  # Same name, diff. oid
        self.assertTrue(t1 == t1)   # Test to itself
        self.assertFalse(t1 == tm_1)    # Test type

    def test_hash_based_on_id(self):
        """SPEC: return hash code based on object's oid"""
        t1 = Team(1, "Team 1")
        t2 = Team(2, "Team 1")
        t3 = Team(2, "Team 4")
        self.assertTrue(hash(t2) == hash(t3))
        self.assertTrue(hash(t2) == hash(t2))

        # objects with different id's may have different hash codes
        self.assertTrue(hash(t1) != hash(t2))

    def test_raise_duplicate_oid_exception(self):
        """SPEC: Raise DuplicateOid if an object is added to a collection
        which has the same oid of an object already in the collection."""
        t = Team(1, "Flintstones")
        tm1 = TeamMember(5, "f", "indigo")
        tm2 = TeamMember(6, "g", "g")
        tm3 = TeamMember(5, 'h', 'i')
        tm4 = TeamMember(7, "k", 'indigo')
        tm5 = TeamMember(8, "p", 'Indigo')
        self.assertEqual(0, len(t.members))
        t.add_member(tm1)
        with self.assertRaises(DuplicateOid):
            t.add_member(tm1)
        self.assertEqual(1, len(t.members))
        self.assertIn(tm1, t.members)
        self.assertIn(tm3, t.members)
        with self.assertRaises(DuplicateOid):
            t.add_member(tm3)
        t.add_member(tm2)
        self.assertEqual(2, len(t.members))
        # Tests DuplicateEmail
        with self.assertRaises(DuplicateEmail):
            t.add_member(tm4)
        with self.assertRaises(DuplicateEmail):
            t.add_member(tm5)

    def test_ignore_request_to_remove_team_member_already_removed(self):
        """SPEC: remove the specified member from this team."""
        t = Team(1, "Flintstones")
        self.assertEqual(0, len(t.members))
        tm1 = TeamMember(5, "f", "f")
        tm2 = TeamMember(6, "g", "g")
        tm3 = TeamMember(7, "k", "h")
        t.add_member(tm1)
        t.add_member(tm2)
        self.assertEqual(2, len(t.members))
        t.remove_member(tm1)
        self.assertNotIn(tm1, t.members)
        self.assertIn(tm2, t.members)
        self.assertEqual(1, len(t.members))
        t.remove_member(tm1)
        t.remove_member(tm3)
        self.assertEqual(1, len(t.members))
        self.assertIn(tm2, t.members)

    def test_str(self):
        """SPEC: return a string like the following: 'Team Name: N members'"""
        # Note that it is not in the specs to change word 'members' to 'member'
        # in the case if there is only one member.
        t = Team(1, "Flintstones")
        tm1 = TeamMember(5, "f", "f")
        tm2 = TeamMember(6, "g", "g")
        t.add_member(tm1)
        t.add_member(tm2)
        self.assertEqual("Flintstones: 2 members", str(t))

    def test_sends_email(self):
        """SPEC: send email to all members of a team except those whose address is None.
        This method should send a single email so if the team has N members,
        the recipient list will have N elements."""
        t = Team(1, "Flintstones")
        tm1 = TeamMember(5, "f", "f@foo.com")
        tm2 = TeamMember(6, "g", "g@bar.com")
        tm3 = TeamMember(7, "harold", "harold@curl.com")
        tm4 = TeamMember(8, "bob", None)
        t.add_member(tm1)
        t.add_member(tm2)
        t.add_member(tm3)
        t.add_member(tm4)
        fe = FakeEmailer()
        t.send_email(fe, "Subject", "Message")
        self.assertEqual(3, len(fe.recipients))
        self.assertEqual("Subject", fe.subject)
        self.assertEqual("Message", fe.message)


if __name__ == '__main__':
    unittest.main()
