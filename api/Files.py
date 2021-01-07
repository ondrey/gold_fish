"""
Работа с файлами в системе
    Все файлы регистрируются в БД и в каталоге,
    путь к файлу определяется как ГОД/Месяц/Наименование объекта/Файлы.*
"""

from api.ObjectDb import ObjectDb
import tempfile
import os
import base64


class Files(ObjectDb):
    def __init__(self):
        ObjectDb.__init__(self)

    def create_file(self, file):
        # print tempfile.gettempdir() # prints the current temporary directory
        fullname = os.path.join(tempfile.gettempdir(), file['name'])

        with open(fullname, 'wb') as f:
            f.write(base64.b64decode(file['content']))
        return fullname

    def save_file(self, full_path_name):
        pass

