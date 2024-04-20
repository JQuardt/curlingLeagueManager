from src.league.identified_object import IdentifiedObject


class TeamMember(IdentifiedObject):

    def __init__(self, oid, name, email):
        """initialization method that sets the oid,
        name and email properties as specified in the arguments
        (note: should call superclass constructor)"""
        super().__init__(oid)
        self.name = name
        self.email = email

    def send_email(self, emailer, subject, message):
        """use the emailer argument to email this member"""
        emailer.send_plain_email([self.email], subject, message)

    def __str__(self):
        """return a string like the following: 'Name<Email>'"""
        return str(self.name + "<" + self.email + ">")
