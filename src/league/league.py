from src.league.identified_object import IdentifiedObject
from src.league.exception_duplicate_oid import DuplicateOid


class League(IdentifiedObject):

    def __init__(self, oid, name):
        """initialization method that sets the oid and
        name properties as specified in the arguments
        (note: should call superclass constructor)"""
        super().__init__(oid)
        self.name = name
        self._teams = []
        self._competitions = []

    @property
    def teams(self):
        """Protects read-only teams"""
        return self._teams

    @property
    def competitions(self):
        """Protects read-only competition"""
        return self._competitions

    def add_team(self, team):
        """add team to the teams collection unless they are already in it
        (in which case do nothing). Raises DuplicateOid exception if the oid
        of the new team is already in use."""
        if team is not None:
            if team.oid in [t.oid for t in self.teams]:
                raise DuplicateOid(f"The oid is duplicated when adding team {team}")
            else:
                self.teams.append(team)

    def remove_team(self, team):
        """remove the team if they are
        in the teams list, otherwise do nothing"""
        if self.competitions is not None:
            for c in self.competitions:
                if team in c.teams_competing:
                    raise ValueError(f"This team {team} is in this league's competition.")
        if team in self.teams:
            self.teams.remove(team)

    def team_named(self, team_name):
        """return the team in this league whose name
        equals team_name (case-sensitive)
        or None if no such team exists"""
        for team in self.teams:
            if team_name == team.name:
                return team
        return None

    def add_competition(self, competition):
        """Adds competition to the competitions collection.
        Raises DuplicateOid Exception if oid of new competition is duplicated.
        Verifies that all teams in the competition are part of the league.
        Throws ValueError if one or more is invalid."""
        if competition is not None:
            for t in competition.teams_competing:
                if t not in self.teams:
                    raise ValueError(f"This team {t} in the attempted addition of the "
                                     f"competition is not in the league.")
            if competition.oid in [c.oid for c in self.competitions]:
                raise DuplicateOid(f"The oid is duplicated when adding competition {competition}")
            else:
                self.competitions.append(competition)

    def teams_for_member(self, member):
        """return a list of all teams for which member plays"""
        comp_list = []
        for team in self.teams:
            if member in team.members:
                comp_list.append(team)
        return comp_list

    def competitions_for_team(self, team):
        """return a list of all competitions in which
        team is participating"""
        comp_list = []
        for comp in self.competitions:
            if team in comp.teams_competing:
                comp_list.append(comp)
        return comp_list

    def competitions_for_member(self, member):
        """return a list of all competitions in which
        member played on one of the competing teams"""
        comp_list = []
        for comp in self.competitions:
            for team in comp.teams_competing:
                if member in team.members:
                    comp_list.append(comp)
        return comp_list

    def __str__(self):
        """return a string resembling the following:
        "League Name: N teams, M competitions"
        where N and M are replaced by the obvious values"""
        return f"{self.name}: {len(self.teams)} teams, {len(self.competitions)} competitions"
