@echo off
setlocal
set PATH=C:\Users\Rodrigo\Documents\ufscbroptimusconfig\python
@echo on
call C:\Users\Rodrigo\Documents\ufscbroptimusconfig\python\Scripts\pyuic5 uiMain.ui -o ../uiMain.py
call C:\Users\Rodrigo\Documents\ufscbroptimusconfig\python\Scripts\pyuic5 uiSubwindow.ui -o ../uiSubwindow.py
call C:\Users\Rodrigo\Documents\ufscbroptimusconfig\python\Scripts\pyuic5 uiVarTable.ui -o ../uiVarTable.py
call C:\Users\Rodrigo\Documents\ufscbroptimusconfig\python\Scripts\pyrcc5 icons.qrc -o ../icons_rc.py