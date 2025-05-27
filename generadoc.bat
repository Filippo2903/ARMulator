@echo off
REM Naviga nella cartella del progetto
cd /d "%~dp0"

REM Aggiunge la cartella di pdoc.exe al PATH
set PATH=C:\Users\matte\AppData\Roaming\Python\Python313\Scripts;%PATH%

REM Imposta il PYTHONPATH alla directory corrente (così trova i moduli locali)
set PYTHONPATH=%CD%;%CD%\translation

REM Crea la documentazione con pdoc
pdoc assembler bytecodeinterpreter components history mainweb native_app simulator tokenizer translation.dictionary translation.dictionaries.en translation.dictionaries.fr translation.dictionaries.it --output-dir pdoc-docs

REM Messaggio di completamento
echo.
echo Documentazione generata in "pdoc-docs"
pause
