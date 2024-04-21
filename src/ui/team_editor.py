from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox

from src.league.exception_duplicate_email import DuplicateEmail
from src.league.team import Team
from src.league.team_member import TeamMember

Ui_MainWindow, QtBaseWindow = uic.loadUiType("ui/team_editor.ui")


class TeamEditorDialog(QtBaseWindow, Ui_MainWindow):

    def __init__(self,  db=None, league=None, team=None, team_title=None, parent=None):
        """Initializes the Team Editor Dialog window."""
        super().__init__(parent)
        self.database = db
        self.league = league
        oid = self.database.next_oid()
        self.setupUi(self)
        if team:
            self.team = team
            self.teams_name_line_edit.setText(team_title)
        elif team_title:
            self.teams_name_line_edit.setText(team_title)
            self.team = Team(oid, team_title)
        else:
            self.team = Team(oid, f"Team {oid}")
        self.update_ui()
        # Add connections to signals
        self.add_member_button.clicked.connect(self.add_button_clicked)
        self.delete_member_button.clicked.connect(self.delete_button_clicked)
        self.edit_member_button.clicked.connect(self.edit_button_clicked)
        self.buttonBox.accepted.connect(self.button_box_accepted)
        self.team_list_widget.currentRowChanged.connect(self.team_list_selection_changed)

    def team_list_selection_changed(self):
        """Sets the text for the line edit if the list widget selection changes."""
        current_row = self.team_list_widget.currentRow()
        if current_row != -1:
            member = self.team.members[current_row]
            self.member_name_line_edit.setText(member.name)
            self.member_email_line_edit.setText(member.email)

    def warn(self, title, message):
        """Pop-up window with the warning message of the arguments provided."""
        mb = QMessageBox(QMessageBox.Icon.NoIcon, title, message, QMessageBox.StandardButton.Ok)
        return mb.exec()

    def update_ui(self):
        """Updates the list widget with the league_database."""
        row = self.team_list_selected_row()
        self.team_list_widget.clear()
        for member in self.team.members:
            # print(member)
            self.team_list_widget.addItem(str(member))
        if row != -1 and len(self.team.members) > row:
            self.team_list_widget.setCurrentItem(self.team_list_widget.item(row))

    def team_list_selected_row(self):
        """Finds and returns the item selected in the list widget. If none, returns -1."""
        selection = self.team_list_widget.selectedItems()
        if len(selection) == 0:
            return -1
        assert len(selection) == 1
        selected_item = selection[0]
        for i, t in enumerate(self.team.members):
            if str(t) == selected_item.text():
                return i
        return -1

    def add_button_clicked(self):
        """Adds the team member to the team. Creates a pop-up warning if there is information missing,
        or if the email is duplicated."""
        name = self.member_name_line_edit.text()
        email = self.member_email_line_edit.text()
        if name == "":
            return self.warn("Member Name Missing", "You must type in the member's name to add.")
        zoid = self.database.next_oid()
        name = self.member_name_line_edit.text()
        email = self.member_email_line_edit.text()
        try:
            member = TeamMember(zoid, name, email)
            self.team.add_member(member)
        except DuplicateEmail:
            return self.warn("Duplicate Email", "You must type in a unique email address.")
        self.update_ui()
        self.member_name_line_edit.clear()
        self.member_email_line_edit.clear()

    def delete_button_clicked(self):
        """If the delete button is clicked, deletes the selected row from the database.
                        A window pops up to confirm deletion."""
        row = self.team_list_selected_row()
        if row == -1:
            return self.warn("Select member", "You must select the member to remove.")
        # team = self.team.members[row]
        dialog = QMessageBox(QMessageBox.Icon.Question,
                             "Are you sure?",
                             "Are you sure you want to remove this member?",
                             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if dialog.exec() == QMessageBox.StandardButton.Yes:
            del self.team.members[row]
            self.update_ui()
            self.member_name_line_edit.clear()
            self.member_email_line_edit.clear()

    def edit_button_clicked(self):
        """If the edit button is clicked, it changes the selected team member with the information in the
        line edit. Pops-up a warning if there is no member selected, or if there is information missing in
        the line edits."""
        row = self.team_list_selected_row()
        if row == -1:
            return self.warn("Select member", "You must select the member to edit.")
        name = self.member_name_line_edit.text()
        if name == "":
            return self.warn("Info Missing", "You must fill in the new name and email.")
        else:
            zoid = self.database.next_oid()
            email = self.member_email_line_edit.text()
            self.team.members[row] = TeamMember(zoid, name, email)
            self.member_name_line_edit.clear()
            self.member_email_line_edit.clear()
        self.update_ui()

    def button_box_accepted(self):
        """When the team is finalized, the team is added to the database
        with the name provided in the name edit."""
        self.database.remove_league(self.league)
        self.league.remove_team(self.team)
        name = self.teams_name_line_edit.text()
        if name:
            self.team.name = name
        self.league.add_team(self.team)
        self.database.add_league(self.league)
        self.member_name_line_edit.clear()
        self.member_email_line_edit.clear()
