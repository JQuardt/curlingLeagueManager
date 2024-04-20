from PyQt5 import uic
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from src.league.league import League
from src.ui.team_editor import TeamEditorDialog

Ui_MainWindow, QtBaseWindow = uic.loadUiType("ui/league_editor.ui")


class LeagueEditorDialog(QtBaseWindow, Ui_MainWindow):

    def __init__(self, league=None, league_title=None, db=None, parent=None):
        super().__init__(parent)
        self.database = db
        oid = self.database.next_oid()
        self.setupUi(self)
        if league:
            self.league = league
            self.league_name_line_edit.setText(league_title)
        elif league_title:
            self.league_name_line_edit.setText(league_title)
            self.league = League(oid, league_title)
            self.database.add_league(self.league)
        else:
            self.league = League(oid, f"League {oid}")
            self.database.add_league(self.league)
        self.update_ui()
        # Connections to signal begin here:
        self.add_team_button.clicked.connect(self.add_button_clicked)
        self.delete_team_button.clicked.connect(self.delete_button_clicked)
        self.edit_team_button.clicked.connect(self.edit_button_clicked)
        self.import_button.clicked.connect(self.import_button_clicked)
        self.export_button.clicked.connect(self.export_button_clicked)
        self.buttonBox.accepted.connect(self.button_box_accepted)
        self.league_editor_list_widget.currentRowChanged.connect(self.editor_list_selection_changed)
        self.rejected.connect(self.league_rejected)

    def league_rejected(self):
        self.database.remove_league(self.league)

    def editor_list_selection_changed(self):
        current_row = self.league_editor_list_widget.currentRow()
        if current_row != -1:
            team = self.league.teams[current_row]
            self.team_name_line_edit.setText(team.name)

    def warn(self, title, message):
        mb = QMessageBox(QMessageBox.Icon.NoIcon, title, message, QMessageBox.StandardButton.Ok)
        return mb.exec()

    def update_ui(self):
        row = self.league_editor_list_selected_row()
        self.league_editor_list_widget.clear()
        for team in self.league.teams:
            self.league_editor_list_widget.addItem(str(team))
        if row != -1 and len(self.league.teams) > row:
            self.league_editor_list_widget.setCurrentItem(self.league_editor_list_widget.item(row))

    def league_editor_list_selected_row(self):
        selection = self.league_editor_list_widget.selectedItems()
        if len(selection) == 0:
            return -1
        assert len(selection) == 1
        selected_item = selection[0]
        for i, c in enumerate(self.league.teams):
            if str(c) == selected_item.text():
                return i
        return -1

    def add_button_clicked(self):
        new_league_name = self.team_name_line_edit.text()
        dialog = TeamEditorDialog(team_title=new_league_name, db=self.database, league=self.league)
        dialog.exec()
        self.update_ui()
        self.team_name_line_edit.clear()

    def delete_button_clicked(self):
        row = self.league_editor_list_selected_row()
        if row == -1:
            return self.warn("Select team", "You must select the member to remove.")
        dialog = QMessageBox(QMessageBox.Icon.Question,
                             "Are you sure?",
                             "Are you sure you want to remove this team?",
                             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if dialog.exec() == QMessageBox.StandardButton.Yes:
            del self.league.teams[row]
            self.update_ui()
            self.team_name_line_edit.clear()

    def edit_button_clicked(self):
        row = self.league_editor_list_selected_row()
        if row == -1:
            return self.warn("Select team", "You must select the team to edit.")
        name = self.team_name_line_edit.text()
        if name == "":
            return self.warn("Info Missing", "You must fill in the team name to select the team.")
        else:
            dialog = TeamEditorDialog(team_title=name, team=self.league.teams[row], db=self.database, league=self.league)
            dialog.exec()
            self.team_name_line_edit.clear()
        self.update_ui()

    def import_button_clicked(self):
        fd = QFileDialog()
        if fd.exec() == QFileDialog.DialogCode.Accepted:
            self.database.import_league_teams(self.league, fd.selectedFiles()[0])
            self.update_ui()

    def export_button_clicked(self):
        (filename, filter_str) = QFileDialog.getSaveFileName(self, "Save CSV File", filter="CSV File (*.csv)")
        if filename:
            self.database.export_league_teams(self.league, filename)
            mb = QMessageBox(QMessageBox.Icon.NoIcon, "File Saved",
                             f"This league has been saved in a CSV file at {filename}", QMessageBox.StandardButton.Ok)
            mb.exec()

    def button_box_accepted(self):
        self.database.remove_league(self.league)
        name = self.league_name_line_edit.text()
        if name:
            self.league.name = name
        self.database.add_league(self.league)
