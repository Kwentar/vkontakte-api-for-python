# -*- coding: utf-8 -*-
import os
import sys
from subprocess import call
import re
# файлы исходники с расширениеми .ui и .qrc
src_relpath = 'sources'
# готовые модули
dst_relpath = 'compiled'
template="""# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui
from ui_{module} import Ui_{klass}

class {klass}(QtGui.{widget}):
    def __init__(self, parent=None):
        QtGui.{widget}.__init__(self, parent)
        self.parent=parent
        self.ui=Ui_{klass}()
        self.ui.setupUi(self)

if __name__ == '__main__':
    a=QtGui.QApplication(sys.argv)
    w={klass}()
    w.show()
    a.exec_()
"""
ui_re='<class>([^<]+)</class>\n <widget class="([^"]+)'
python_path = os.path.dirname(sys.executable)
puic_path = python_path + '\Lib\site-packages\PyQt4\uic\pyuic.py'
curpath = os.path.dirname(__file__)
items = os.listdir(src_relpath)
for item in items:
    path = os.path.join(src_relpath, item)
    if os.path.isfile(path):
        name, extension = os.path.splitext(item)
        extension = extension.lower()
        if extension in ['.ui', '.qrc']:
            infile = os.path.join(curpath, path) 
            if extension == '.ui':
                outfile = os.path.join(curpath, dst_relpath,
                                       'ui_' + name + '.py')
                call(['python', puic_path, infile, '-o', outfile])
                # Ищем в исходнике имя класса и виджет от которого он 
                # наследуется.
                f=open(infile)
                content=f.read()
                f.close()
                m=re.search(ui_re, content)
                cls=m.group(1)
                wdg=m.group(2)
                data=template.format(module=name, klass=cls, widget=wdg)
                filename=os.path.join(curpath, dst_relpath, name + '.py')
                f=open(filename, 'w')
                f.write(data)
                f.close()
            elif extension == '.qrc':
                outfile = os.path.join(curpath, dst_relpath, name + '_rc.py')
                call(['pyrcc4', '-o', outfile, infile])
