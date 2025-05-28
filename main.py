import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from database import *
from export_csv import export_to_csv

class BookManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("F1D022072_M. Fajar Maulana")
        self.resize(800, 500)
        self.selected_id = None
        create_table()
        self.initUI()

    def initUI(self):
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)
        file_menu = menu_bar.addMenu("File")
        export_action = QAction("Ekspor ke CSV", self)
        export_action.triggered.connect(self.export_csv)
        exit_action = QAction("Keluar", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(export_action)
        file_menu.addAction(exit_action)

        edit_menu = menu_bar.addMenu("Edit")
        delete_action = QAction("Hapus Data", self)
        delete_action.triggered.connect(self.delete_data)
        edit_menu.addAction(delete_action)

        view_menu = menu_bar.addMenu("View")
        toggle_search_action = QAction("Tampilkan/Sembunyikan Pencarian", self, checkable=True)
        toggle_search_action.setChecked(True)
        toggle_search_action.triggered.connect(self.toggle_search_panel)
        view_menu.addAction(toggle_search_action)
        self.toggle_search_action = toggle_search_action
        self.title_input = QLineEdit()
        self.author_input = QLineEdit()
        self.year_input = QLineEdit()
        paste_btn = QPushButton("Paste from Clipboard")
        paste_btn.clicked.connect(self.paste_from_clipboard)
        self.save_btn = QPushButton("Simpan")
        self.save_btn.clicked.connect(self.save_data)

        form_layout = QVBoxLayout()
        form_layout.addWidget(QLabel("Judul:"))
        form_layout.addWidget(self.title_input)
        form_layout.addWidget(paste_btn)
        form_layout.addWidget(QLabel("Pengarang:"))
        form_layout.addWidget(self.author_input)
        form_layout.addWidget(QLabel("Tahun:"))
        form_layout.addWidget(self.year_input)
        form_layout.addWidget(self.save_btn)
        form_layout.addStretch()
        form_widget = QWidget()
        form_widget.setLayout(form_layout)
        form_scroll = QScrollArea()
        form_scroll.setWidgetResizable(True)
        form_scroll.setWidget(form_widget)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Cari judul...")
        self.search_input.textChanged.connect(self.search_data)

        self.search_dock = QDockWidget("Pencarian", self)
        self.search_dock.setWidget(self.search_input)
        self.search_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.addDockWidget(Qt.RightDockWidgetArea, self.search_dock)

        self.search_dock.setVisible(True)
        self.search_dock.visibilityChanged.connect(self.sync_toggle_menu)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Judul", "Pengarang", "Tahun"])
        self.table.cellDoubleClicked.connect(self.load_selected_row)
        self.table.setAlternatingRowColors(True)

        self.delete_btn = QPushButton("Hapus Data")
        self.delete_btn.clicked.connect(self.delete_data)

        table_layout = QVBoxLayout()
        table_layout.addWidget(self.table)
        table_layout.addWidget(self.delete_btn)

        main_layout = QHBoxLayout()
        main_layout.addWidget(form_scroll, 1)
        right_side = QWidget()
        right_side.setLayout(table_layout)
        main_layout.addWidget(right_side, 2)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        status_bar = QStatusBar()
        status_bar.showMessage("Fajar Maulana - F1D022072")
        self.setStatusBar(status_bar)

        self.load_data()

    def paste_from_clipboard(self):
        clipboard = QApplication.clipboard()
        text = clipboard.text()
        self.title_input.setText(text)

    def load_data(self):
        self.table.setRowCount(0)
        for row_data in fetch_books():
            row_number = self.table.rowCount()
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def save_data(self):
        title = self.title_input.text()
        author = self.author_input.text()
        year = self.year_input.text()

        if not (title and author and year):
            QMessageBox.warning(self, "Input Salah", "Semua kolom harus diisi.")
            return

        if self.selected_id:
            update_book(self.selected_id, title, author, int(year))
            self.selected_id = None
        else:
            insert_book(title, author, int(year))

        self.title_input.clear()
        self.author_input.clear()
        self.year_input.clear()
        self.load_data()

    def load_selected_row(self, row, _):
        self.selected_id = int(self.table.item(row, 0).text())
        self.title_input.setText(self.table.item(row, 1).text())
        self.author_input.setText(self.table.item(row, 2).text())
        self.year_input.setText(self.table.item(row, 3).text())

    def delete_data(self):
        selected = self.table.currentRow()
        if selected >= 0:
            book_id = int(self.table.item(selected, 0).text())
            delete_book(book_id)
            self.load_data()

    def search_data(self):
        keyword = self.search_input.text().lower()
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 1)
            self.table.setRowHidden(row, keyword not in item.text().lower())

    def export_csv(self):
        books = fetch_books()
        headers = ["ID", "Judul", "Pengarang", "Tahun"]
        export_to_csv(books, headers)

    def toggle_search_panel(self, checked):
        self.search_dock.setVisible(checked)

    def sync_toggle_menu(self, visible):
        self.toggle_search_action.setChecked(visible)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BookManager()
    window.show()
    sys.exit(app.exec_())