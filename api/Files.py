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


class Files(ObjectDb):
    def __init__(self):
        ObjectDb.__init__(self)
        self.home_path = os.path.expanduser("~")
        self.app_path = os.path.join(self.home_path, "\\kjm_files")

        if not os.path.exists(self.app_path):
            os.mkdir(self.app_path)

    @staticmethod
    def create_file(file):
        fullname = os.path.join(tempfile.gettempdir(), file['name'])

        with open(fullname, 'wb') as f:
            f.write(base64.b64decode(file['content']))
        return fullname

    def save_file(self, tmp_file, dir_name, file_name):
        new_path = os.path.join(self.app_path, dir_name)
        if not os.path.exists(new_path):
            os.mkdir(new_path)
        new_file = os.path.join(new_path, file_name)
        shutil.move(tmp_file, new_file)

        pass

