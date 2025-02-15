#  NanoVNASaver
#
#  A python program to view and export Touchstone data from a NanoVNA
#  Copyright (C) 2019, 2020  Rune B. Broberg
#  Copyright (C) 2020 NanoVNA-Saver Authors
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
import logging
from time import strftime, localtime
from urllib import request, error

from PyQt5 import QtWidgets, QtCore

from NanoVNASaver.About import INFO_URL
from NanoVNASaver.Version import Version

logger = logging.getLogger(__name__)


class AboutWindow(QtWidgets.QWidget):
    def __init__(self, app: QtWidgets.QWidget):
        super().__init__()
        self.app = app

        self.setWindowTitle("About NanoVNASaver")
        self.setWindowIcon(self.app.icon)
        top_layout = QtWidgets.QHBoxLayout()
        self.setLayout(top_layout)
        QtWidgets.QShortcut(QtCore.Qt.Key_Escape, self, self.hide)

        icon_layout = QtWidgets.QVBoxLayout()
        top_layout.addLayout(icon_layout)
        icon = QtWidgets.QLabel()
        icon.setPixmap(self.app.icon.pixmap(128, 128))
        icon_layout.addWidget(icon)
        icon_layout.addStretch()

        layout = QtWidgets.QVBoxLayout()
        top_layout.addLayout(layout)

        layout.addWidget(QtWidgets.QLabel(
            f"NanoVNASaver version {self.app.version}"))
        layout.addWidget(QtWidgets.QLabel(""))
        layout.addWidget(QtWidgets.QLabel(
            "\N{COPYRIGHT SIGN} Copyright 2019, 2020 Rune B. Broberg\n"
            "\N{COPYRIGHT SIGN} Copyright 2020 NanoVNA-Saver Authors"
            ))
        layout.addWidget(QtWidgets.QLabel(
            "This program comes with ABSOLUTELY NO WARRANTY"))
        layout.addWidget(QtWidgets.QLabel(
            "This program is licensed under the"
            " GNU General Public License version 3"))
        layout.addWidget(QtWidgets.QLabel(""))
        link_label = QtWidgets.QLabel(
            f'For further details, see: <a href="{INFO_URL}">'
            f"{INFO_URL}")
        link_label.setOpenExternalLinks(True)
        layout.addWidget(link_label)
        layout.addWidget(QtWidgets.QLabel(""))

        self.versionLabel = QtWidgets.QLabel(
            "NanoVNA Firmware Version: Not connected.")
        layout.addWidget(self.versionLabel)

        layout.addStretch()

        btn_check_version = QtWidgets.QPushButton("Check for updates")
        btn_check_version.clicked.connect(self.findUpdates)

        self.updateLabel = QtWidgets.QLabel("Last checked: ")
        self.updateCheckBox = QtWidgets.QCheckBox(
            "Check for updates on startup")

        self.updateCheckBox.toggled.connect(self.updateSettings)

        check_for_updates = self.app.settings.value(
            "CheckForUpdates", "Ask")
        if check_for_updates == "Yes":
            self.updateCheckBox.setChecked(True)
            self.findUpdates(automatic=True)
        elif check_for_updates == "No":
            self.updateCheckBox.setChecked(False)
        else:
            logger.debug("Starting timer")
            QtCore.QTimer.singleShot(2000, self.askAboutUpdates)

        update_hbox = QtWidgets.QHBoxLayout()
        update_hbox.addWidget(btn_check_version)
        update_form = QtWidgets.QFormLayout()
        update_hbox.addLayout(update_form)
        update_hbox.addStretch()
        update_form.addRow(self.updateLabel)
        update_form.addRow(self.updateCheckBox)
        layout.addLayout(update_hbox)

        layout.addStretch()

        btn_ok = QtWidgets.QPushButton("Ok")
        btn_ok.clicked.connect(lambda: self.close())  # noqa
        layout.addWidget(btn_ok)

    def show(self):
        super().show()
        self.updateLabels()

    def updateLabels(self):
        try:
            self.versionLabel.setText(
                f"NanoVNA Firmware Version: {self.app.vna.name} "
                f"v{self.app.vna.version}")
        except (IOError, AttributeError):
            pass

    def updateSettings(self):
        if self.updateCheckBox.isChecked():
            self.app.settings.setValue("CheckForUpdates", "Yes")
        else:
            self.app.settings.setValue("CheckForUpdates", "No")

    def askAboutUpdates(self):
        logger.debug("Asking about automatic update checks")
        selection = QtWidgets.QMessageBox.question(
            self.app,
            "Enable checking for updates?",
            "Would you like NanoVNA-Saver to"
            " check for updates automatically?")
        if selection == QtWidgets.QMessageBox.Yes:
            self.updateCheckBox.setChecked(True)
            self.app.settings.setValue("CheckForUpdates", "Yes")
            self.findUpdates()
        elif selection == QtWidgets.QMessageBox.No:
            self.updateCheckBox.setChecked(False)
            self.app.settings.setValue("CheckForUpdates", "No")
            QtWidgets.QMessageBox.information(
                self.app,
                "Checking for updates disabled",
                'You can check for updates using the "About" window.')
        else:
            self.app.settings.setValue("CheckForUpdates", "Ask")

    def findUpdates(self, automatic=False):
        return
