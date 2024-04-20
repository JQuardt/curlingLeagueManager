from src.league.identified_object import IdentifiedObject
import datetime as dt


class Competition(IdentifiedObject):

    def __init__(self, oid, teams, location, datetime=None):
        """initialization method that sets the oid, teams,
        location and date_time properties as specified in
        the arguments (note: should call superclass constructor).
          Note: teams should be a list.
        The date_time should be datetime objects (not a string!)
        indicating when the competition will begin."""
        super().__init__(oid)
        self._teams_competing = teams
        self.location = location
        if datetime is None or type(datetime) == type(dt.datetime.now()):
            self.date_time = datetime
        else:
            self.date_time = None

    @property
    def teams_competing(self):
        return self._teams_competing

    def send_email(self, emailer, subject, message):
        """use the emailer argument to email all members of all
        teams in this competition without duplicates.  That is,
        a team member may be on multiple teams that may be
        competing against each other. Only send one email to
        each team member on all the teams in this competition.
        This method should send a single email so if the teams
        have N and M members respectively, the recipient list
        will have N+M elements assuming all the members were
        distinct.  If the teams have S "shared" members
        then we'd expect a single email with N+M-S recipients."""
        recipients = []
        for team in self.teams_competing:
            for member in team.members:
                if member.email not in recipients:
                    recipients.append(member.email)
        emailer.send_plain_email(recipients, subject, message)

    def __str__(self):
        """return a string like the following:
        "Competition at location on date_time with N teams"
        (note: date_time may be None in which case just omit
        the "on date_time" part.  If present, format the
        date_time property similar to the following example
        "12/31/1995 19:30".)"""
        return f"Competition at {self.location} with {len(self.teams_competing)} teams" if self.date_time is None else \
            f"Competition at {self.location} on {self.date_time.strftime('%m/%d/%Y %H:%M')} " \
            f"with {len(self.teams_competing)} teams"
