""" from threading import Thread
from mainweb import main as main_web
from start_native_app import main as main_native

# Ora esegui entrambi in parallelo usando i thread:
thread_a = Thread(target=main_web)
thread_b = Thread(target=main_native)

thread_a.start()
thread_b.start()

thread_a.join()
thread_b.join()

print("Entrambi i programmi sono terminati!") """



""" import subprocess
import sys

def run_mainweb():
    # Avvia mainweb.py come un processo separato
    try:
        subprocess.run([sys.executable, 'mainweb.py'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Errore durante l'esecuzione di mainweb.py: {e}")

if __name__ == '__main__':
    print("Avvio di mainweb.py tramite subprocess...")
    run_mainweb() """



""" import subprocess
import sys

def run_mainweb():
    subprocess.run([sys.executable, 'mainweb.py'], check=True)

def run_start_native_app():
    subprocess.run([sys.executable, 'start_native_app.py'], check=True)

if __name__ == '__main__':
    print("Avvio mainweb.py e start_native_app.py in parallelo...")
    
    # Avvia mainweb.py in un processo separato
    process1 = subprocess.Popen([sys.executable, 'mainweb.py'])
    
    # Avvia start_native_app.py in un altro processo separato
    process2 = subprocess.Popen([sys.executable, 'start_native_app.py'])
    
    # Attendi che entrambi i processi finiscano
    process1.wait()
    process2.wait()

    print("Entrambi gli script sono terminati.") """




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
