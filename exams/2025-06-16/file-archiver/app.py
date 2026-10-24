#path: $HOME/file-archiver/app.py
import argparse
import os
import sys
import shutil
import time

#Percorri quindi ricorsivamente l’albero delle directory al percorso fornito come primo argomento (os.listdir, os.path.join, os.path.isdir). 
# Per ogni file incontrato (os.path.isfile), calcola da quanti secondi non viene modificato (os.path.getmtime, time.time). 
#  Se l'età in secondi è maggiore o uguale al valore di soglia, sposta il file nella cartella ~/archive (shutil.move) 
#   e stampa un messaggio di log sullo standard output (print). 
# Non tentare di spostare directory.
def walk(basepath, seconds, archive_path):
  for filename in os.listdir(basepath):
        path = os.path.join(basepath, filename)
        if os.path.isfile(path):
            file_age_seconds = time.time() - os.path.getmtime(path)
            if file_age_seconds >= seconds:
                shutil.move(path, archive_path)
                print(f"moved {path} to {archive_path}")
        elif os.path.isdir(path):
            walk(path, seconds, archive_path)

def main():
  #ARGOMENTI
  # Deve accettare esattamente due argomenti da linea di comando, analizzati con il modulo argparse.
  # --path: stringa obbligatoria che indica il percorso assoluto della directory da controllare,
  # --seconds: intero obbligatorio che specifica l’età massima (in secondi) oltre la quale i file devono essere spostati. 
  parser = argparse.ArgumentParser(description="file archiver")
  parser.add_argument(
    "--path",
    type=str,
    required=True,
    help="percorso assoluto della directory da controllare",
  )
  parser.add_argument(
    "--seconds",
    type=int,
    required=True,
    help="specifica l’età massima (in secondi) oltre la quale i file devono essere spostati",
  )
  args = parser.parse_args()

  #VALIDAZIONE
  # Controlla che il percorso sia assoluto (os.path.isabs),
  # Esista (os.path.exists),
  # Sia una directory (os.path.isdir),
  # --seconds Sia un intero positivo.
  if not os.path.isabs(args.path):
    print(f"error: {args.path} deve essere un percorso assoluto", file=sys.stderr)
  sys.exit(1)
  if not os.path.isabs(args.path):
    print(f"error: {args.path} deve esistere", file=sys.stderr)
  sys.exit(1)
  if not os.path.isabs(args.path):
    print(f"error: {args.path} deve essere una directory", file=sys.stderr)
  sys.exit(1)
  if args.seconds <= 0:
    print(f"error: {args.seconds} deve essere un intero positivo", file=sys.stderr)
  sys.exit(1)

  #ASSICURATI CHE IN ~ ESISTA LA CARTELLA ARCHIVE 
  # os.path.expanduser,
  # os.makedirs.
  archive_path = os.path.expanduser("~archive")
  os.makedirs(archive_path, exist_ok=True)
  walk(args.path, args.seconds, archive_path)

if __name__ == "__main__":
    main()
