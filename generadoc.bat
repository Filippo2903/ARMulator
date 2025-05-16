@echo off
REM Naviga nella cartella del progetto
cd /d "%~dp0"

REM Imposta il PYTHONPATH alla directory corrente (così trova i moduli locali)
set PYTHONPATH=.

REM Crea la documentazione con pdoc
pdoc assembler bytecodeinterpreter components history mainweb native_app simulator tokenizer --output-dir pdoc-docs

REM Messaggio di completamento
echo.
echo Documentazione generata in "pdoc-docs"
pause

