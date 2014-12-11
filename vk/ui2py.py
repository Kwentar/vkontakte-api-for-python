# -*- coding: utf-8 -*-
import os
import sys
from subprocess import call
# файлы исходники с расширениеми .ui и .qrc
src_dirname = 'src'
# готовые модули
dst_dirname = 'ui'
python_path = os.path.dirname(sys.executable)
puic_path = python_path + '\\Lib\\site-packages\\PyQt4\\uic\\pyuic.py'
curpath = os.path.dirname(__file__)
items = os.listdir(src_dirname)
for item in items:
    path = src_dirname + '\\' + item
    if os.path.isfile(path):
        name, extension = os.path.splitext(item)
        extension = extension.lower()
        if extension in ['.ui', '.qrc']:
            infile = os.path.join(curpath, path) 
            if extension == '.ui':
                outfile = os.path.join(curpath, dst_dirname, 'Ui_' + name + '.py')
                call(['python', puic_path, infile, '-o', outfile])
            elif extension == '.qrc':
                outfile = os.path.join(curpath, dst_dirname, name + '_rc.py')
                call(['pyrcc4', '-o', outfile, infile])
