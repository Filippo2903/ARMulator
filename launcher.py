import subprocess
import sys
import os
import signal

def run_mainweb():
    subprocess.run([sys.executable, 'mainweb.py'], check=True)

def run_start_native_app():
    process = subprocess.Popen([sys.executable, 'start_native_app.py'])
    # Attendi che il processo principale di start_native_app.py finisca
    process.wait()

    # Quando il processo termina (finestra chiusa), termina anche gli altri processi
    print("La finestra di start_native_app.py è stata chiusa. Terminando tutto.")
    os.kill(os.getpid(), signal.SIGTERM)  # Termina il processo principale

if __name__ == '__main__':
    print("Avvio mainweb.py e start_native_app.py in parallelo...")

    # Avvia mainweb.py in un processo separato
    process1 = subprocess.Popen([sys.executable, 'mainweb.py'])

    # Avvia start_native_app.py in un altro processo separato
    run_start_native_app()  # Questo ora monitora la finestra

    # Attendi che mainweb.py finisca
    process1.wait()

    print("Entrambi gli script sono terminati.")
