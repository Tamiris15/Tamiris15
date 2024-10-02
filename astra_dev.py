import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeView, QFileSystemModel, QVBoxLayout, QWidget, QLineEdit
from PyQt5.QtCore import QDir, Qt

class QFileSystemModelWithFolderSize(QFileSystemModel):
    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and index.column() == 1:
            file_info = self.fileInfo(index)
            if file_info.isDir():
                return self.get_folder_size(file_info.absoluteFilePath())
        return super().data(index, role)

    def get_folder_size(self, folder):
        total_size = 0
        for dirpath, _, filenames in os.walk(folder):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        return self.format_size(total_size)

    @staticmethod
    def format_size(size):
        # Helper function to format the size for better readability
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("File Viewer")

        # Основной виджет внутри окна
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Создаем виджет QTreeView
        self.tree_view = QTreeView()
        layout.addWidget(self.tree_view)

        # Устанавливаем модель файловой системы
        self.model = QFileSystemModelWithFolderSize()
        home_dir = QDir.homePath()
        self.model.setRootPath(home_dir)
        self.model.setFilter(QDir.AllEntries | QDir.Hidden | QDir.NoDotAndDotDot) # Включаем отображение скрытых файлов и папок

        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index(home_dir))

        # Добавляем виджет QLineEdit для фильтрации
        self.filter_edit = QLineEdit()
        layout.addWidget(self.filter_edit)
        self.filter_edit.setPlaceholderText("Введите текст для фильтрации")
        self.filter_edit.textChanged.connect(self.filter_folders)

    def filter_folders(self, text):
        self.model.setNameFilters([f"*{text}*"])
        self.model.setNameFilterDisables(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec_())
