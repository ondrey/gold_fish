"""
Работа с файлами в системе
    Все файлы регистрируются в БД и в каталоге,
    путь к файлу определяется как ГОД/Месяц/Наименование объекта/Файлы.*
"""

from api.ObjectDb import ObjectDb
import tempfile
import os
import base64
import shutil
from pathlib import Path

class Files(ObjectDb):
    def __init__(self):
        ObjectDb.__init__(self)
        self.home_path = os.path.expanduser("~")
        self.app_path = os.path.join(self.home_path, "/kjm_files")
        print(self.app_path)
        if not os.path.exists(self.app_path):
            os.mkdir(self.app_path)

    def create_file(self, file):
        fullname = os.path.join(tempfile.gettempdir(), file['name'])

        with open(fullname, 'wb') as f:
            f.write(base64.b64decode(file['content']))
        return fullname

    def save_file(self, full_path_name, object_name):
        pass

