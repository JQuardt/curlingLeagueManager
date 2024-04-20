import pickle
import os.path
from os import rename
import csv
from src.league.team_member import TeamMember
from src.league.team import Team


class LeagueDatabase:
    """Singleton. Keeps track of a list of leagues."""

    _sole_instance = None
    """Sole instance of class. A class variable"""

    @classmethod
    def instance(cls):
        """returns the sole instance of this database, creating one if it doesn't exist yet"""
        if cls._sole_instance is None:
            cls._sole_instance = cls()
        return cls._sole_instance

    @classmethod
    def load(cls, file_name):
        """loads a LeagueDatabase from the specified file and stores it in _sole_instance.
        If file_name does not exist or an error occurs when reading it,
        display a console message and load the file from the backup (if it exists).
        See save() for information on the backup file."""
        try:
            with open(file_name, mode="rb") as f:
                cls._sole_instance = pickle.load(f)
        except (FileNotFoundError, IOError, pickle.PickleError) as e:   # If file name doesn't exist
            print(e.strerror)
            try:
                with open(file_name + ".backup", mode="rb") as f:
                    cls._sole_instance = pickle.load(f)
            except FileNotFoundError:
                print('Backup file not found.')

    def __init__(self):
        self._leagues = []
        self._last_oid = 0
        """private variable holding the last id number that was supplied."""

    @property
    def leagues(self):
        """Read-only property. List of the leagues being managed."""
        return self._leagues

    def add_league(self, league):
        """add the specified league to the leagues list"""
        self.leagues.append(league)

    def remove_league(self, league):
        """remove the specified league from the leagues list.
        If league is not in the leagues list, simply do nothing (not an error)."""
        if league in self.leagues:
            self.leagues.remove(league)

    def league_named(self, name):
        """return the league with the given name or None of no such league exists"""
        for league in self.leagues:
            if name == league.name:
                return league
        return None

    def next_oid(self):
        """increment _last_id and return its new value (used to generate oid's for your objects)"""
        self._last_oid += 1
        return self._last_oid

    def save(self, file_name):
        """save this database on the specified file. Before saving,
        check if the file exists and if it does, rename it to file_name with '.backup' added."""
        if os.path.isfile(file_name):
            rename(file_name, file_name + ".backup")
        with open(file_name, mode='wb') as f:
            pickle.dump(self, f)

    def import_league_teams(self, league, file_name):
        """Load the teams and team members in a league from a CSV formatted file.
        The file will contain three columns: team name, team member name, email.
        The first line of the file will be a "header" line and should be ignored.
        The file will be UTF-8 encoded and may contain non-ASCII text.
        Note that the first argument to this method must be a league object, not the name of a league.
        If an error occurs while loading a league, display a message on the console. """
        try:
            with open(file_name, newline='', encoding="utf-8") as f:
                csv_reader = csv.reader(f)
                for row in csv_reader:
                    if csv_reader.line_num > 1:
                        # ["Team name", "Member name", "Member email"]
                        team = league.team_named(row[0])
                        if team is None:
                            team = Team(self.next_oid(), row[0])
                            league.add_team(team)
                        team.add_member(TeamMember(self.next_oid(), row[1], row[2]))
            return league
        except FileNotFoundError:
            print("File not found.")
        except IOError:
            print("An error occurred.")

    def export_league_teams(self, league, file_name):
        """write the specified league to a CSV formatted file.
        The first line of the file must be a "header" row containing the following text
        (without the leading spaces): Team name, Member name, Member email
        If an error occurs while writing a league, display a message on the console."""
        try:
            with open(file_name, 'w', newline='', encoding="utf-8") as f:
                csv_writer = csv.writer(f)
                # csv_writer.writeheader(["Team name", "Member name", "Member email"])
                csv_writer.writerow(["Team name", "Member name", "Member email"])
                for team in league.teams:
                    for member in team.members:
                        csv_writer.writerow([team.name, member.name, member.email])
        except FileNotFoundError:
            print("File not found.")
        except IOError:
            print("An error occurred.")
