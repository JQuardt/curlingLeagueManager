from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox, QFileDialog

from src.league.league_database import LeagueDatabase
from src.ui.league_editor import LeagueEditorDialog

Ui_MainWindow, QtBaseWindow = uic.loadUiType("ui/main_window.ui")


class MainWindow(QtBaseWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.db = LeagueDatabase.instance()
        # name of button . what signal? . connect to a (slot)
        self.update_ui()
        self.add_league_button.clicked.connect(self.add_button_clicked)
        self.delete_league_button.clicked.connect(self.delete_button_clicked)
        self.edit_league_button.clicked.connect(self.edit_button_clicked)
        self.action_load.triggered.connect(self.action_load_triggered)
        self.action_save.triggered.connect(self.action_save_triggered)
        self.main_list_widget.currentRowChanged.connect(self.main_list_selection_changed)

    def main_list_selection_changed(self):
        current_row = self.main_list_widget.currentRow()
        if current_row != -1:
            league = self.db.leagues[current_row]
            self.league_line_edit.setText(league.name)

    def warn(self, title, message):
        mb = QMessageBox(QMessageBox.Icon.NoIcon, title, message, QMessageBox.StandardButton.Ok)
        return mb.exec()

    def update_ui(self):
        row = self.main_list_selected_row()
        self.main_list_widget.clear()
        for league in self.db.leagues:
            self.main_list_widget.addItem(str(league))
        if row != -1 and len(self.db.leagues) > row:
            self.main_list_widget.setCurrentItem(self.main_list_widget.item(row))

    def main_list_selected_row(self):
        selection = self.main_list_widget.selectedItems()
        if len(selection) == 0:
            return -1
        assert len(selection) == 1
        selected_item = selection[0]
        for i, c in enumerate(self.db.leagues):
            if str(c) == selected_item.text():
                return i
        return -1

    def add_button_clicked(self):
        new_league_name = self.league_line_edit.text()
        dialog = LeagueEditorDialog(league_title=new_league_name, db=self.db)
        dialog.exec()
        self.update_ui()
        self.league_line_edit.clear()

    def edit_button_clicked(self):
        row = self.main_list_selected_row()
        if row == -1:
            return self.warn("Select league", "You must select the league to edit.")
        if self.league_line_edit.text() == "":
            return self.warn("Info Missing", "You must fill in the league name or select the team.")
        else:
            name = self.db.leagues[row].name
            dialog = LeagueEditorDialog(league_title=name, league=self.db.leagues[row], db=self.db)
            dialog.exec()
            self.league_line_edit.clear()
        self.update_ui()

    def delete_button_clicked(self):
        row = self.main_list_selected_row()
        if row == -1:
            return self.warn("Select league", "You must select the league to remove.")
        dialog = QMessageBox(QMessageBox.Icon.Question,
                             "Are you sure?",
                             "Are you sure you want to remove this league?",
                             QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if dialog.exec() == QMessageBox.StandardButton.Yes:
            del self.db.leagues[row]
            self.update_ui()
            self.league_line_edit.clear()

    def action_load_triggered(self):
        """Uses load method of LeagueDatabase class to unpickle .dat file into current database."""
        fd = QFileDialog()
        if fd.exec() == QFileDialog.DialogCode.Accepted:
            self.db.load(fd.selectedFiles()[0])
            self.db = self.db.instance()
            self.update_ui()

    def action_save_triggered(self):
        """Uses save method of LeagueDatabase class to pickle current database into .dat file."""
        (filename, filter_str) = QFileDialog.getSaveFileName(self, "Save File", filter="Data File (*.dat)")
        if filename:
            self.db.save(filename)
            mb = QMessageBox(QMessageBox.Icon.NoIcon, "File Saved",
                             f"These leagues has been saved in a file at {filename}", QMessageBox.StandardButton.Ok)
            mb.exec()



