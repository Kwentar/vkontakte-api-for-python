# -*- coding: utf-8 -*-
import os
import PyQt4.uic

def main(path):
    # Выбираем текущую директорию рабочей.
    os.chdir(os.path.dirname(__file__))
    
    for curpath, dirs, files in os.walk(path):
        for filename in files:
            basename, extension = os.path.splitext(filename)
            extension = extension.lower()
            
            if extension == '.ui':
                dst = os.path.join(curpath, basename + '.py')
                
                if not os.path.exists(dst):
                    src = os.path.join(curpath, filename)
                    PyQt4.uic.compileUi(open(src), open(dst, 'w'))      
            elif extension == '.qrc':
                dst = os.path.join(curpath, basename + '_rc.py')
                
                if not os.path.exists(dst):
                    src = os.path.join(curpath, filename)
                    os.system('pyrcc4 %s -o %s' % (src, dst))
                    
if __name__ == '__main__':
    main('.')