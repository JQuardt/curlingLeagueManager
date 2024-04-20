from src.league.identified_object import IdentifiedObject
from src.league.exception_duplicate_oid import DuplicateOid
from src.league.exception_duplicate_email import DuplicateEmail


class Team(IdentifiedObject):

    def __init__(self, oid, name):
        """initialization method that sets the oid and
        name properties as specified in the arguments
        (note: should call superclass constructor)"""
        super().__init__(oid)
        self.name = name
        self._members = []

    @property
    def members(self):
        return self._members

    def add_member(self, member):
        """Adds new member to team. Ignore request to add team member that is
        already in members. Raises DuplicateOid and DuplicateEmail exceptions if email or
        oid is already in use for that member. DuplicateEmail is case-insensitive."""
        if member is not None:
            if member in self.members:
                raise DuplicateOid("The oid is duplicated for the intended member addition.")
            elif member.email is None:
                self.members.append(member)
            elif member.email.upper() in [m.email.upper() for m in self.members]:
                raise DuplicateEmail("The member has a duplicated email address.")
            else:
                self.members.append(member)

    def member_named(self, s):
        """return the member of this team
        whose name equals s (case-sensitive)
        or None if no such member exists"""
        for member in self.members:
            if member.name == s:
                return member
        return None

    def remove_member(self, member):
        """remove the specified member from this team"""
        if member is not None and member in self.members:
            self.members.remove(member)

    def send_email(self, emailer, subject, message):
        """use the emailer argument to email
        to all members of a team except those whose
        email address is None.  This method should send a
        single email so if the team has N members,
        the recipient list will have N elements."""
        recipients = []
        for member in self.members:
            if member.email is not None:
                recipients.append(member.email)
        emailer.send_plain_email(recipients, subject, message)

    def __str__(self):
        """return a string like the following: 
        'Team Name: N members'"""
        return f"{self.name}: {len(self.members)} members"
