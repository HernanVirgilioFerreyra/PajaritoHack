import pandas as pd
import requests
from pathlib import Path
from tkinter import Tk, filedialog
import shutil

# =========================
# ASCII ART
# =========================

# Detectar ancho de terminal
terminal_width = shutil.get_terminal_size().columns

# ASCII GRANDE
BIG_BIRD = r"""
       _.--.__                                             _.--.
    ./'       `--.__                                   ..-'   ,'
  ,/               |`-.__                            .'     ./
 :,                 :    `--_    __                .'   ,./'_.....
 :                  :   /    `-:' _\.            .'   ./..-'   _.'
 :                  ' ,'       : / \ :         .'    `-'__...-'
 `.               .'  .        : \@/ :       .'       '------.,
    ._....____  ./    :     .. `     :    .-'      _____.----'
              `------------' : |     `..-'        `---.
                         .---'  :    ./      _._-----'
.---------._____________ `-.__/ : /`      ./_-----/':
`---...--.              `-_|    `.`-._______-'  /  / ,-----.__----.
   ,----' ,__.  .          |   /  `\.________./  ====__....._____.' 
   `-___--.-' ./. .-._-'----\.                  ./.---..____.--.
         :_.-' '-'            `..            .-'===.__________.'
                                 `--...__.--'

                         PajaritoHack
"""

# ASCII CHICO
SMALL_BIRD = r"""
   (
  `-`-.
  '( @ >
   _) (
  /    )
 /_,'  /
   \  /
===m""m===

 PajaritoHack
"""

# Mostrar según tamaño
if terminal_width >= 100:
    print(BIG_BIRD)
else:
    print(SMALL_BIRD)

# =========================
# MENÚ INICIAL
# =========================

print("1 -> Seleccionar CSV")
print("0 -> Salir")

option = input("\nSeleccione una opción: ").strip()

if option != "1":
    print("Saliendo...")
    exit()

# =========================
# SELECCIONAR CSV
# =========================

while True:

    try:

        root = Tk()
        root.withdraw()
        root.attributes('-topmost', True)

        csv_path = filedialog.askopenfilename(
            title="Seleccionar archivo CSV",
            filetypes=[("CSV files", "*.csv")]
        )

        root.destroy()

        if not csv_path:

            print("\nNo se seleccionó ningún archivo.")
            print("Intente nuevamente.")
            continue

        break

    except Exception as e:

        print(f"\n[ERROR TKINTER] {e}")
        print("Intente nuevamente.")

print(f"\nCSV seleccionado:")
print(csv_path)

# =========================
# CONFIGURACIÓN
# =========================

OUTPUT_DIR = "audios"
Path(OUTPUT_DIR).mkdir(exist_ok=True)

# =========================
# LEER CSV
# =========================

try:
    df = pd.read_csv(csv_path)

except Exception:
    df = pd.read_csv(csv_path, sep=";")

# =========================
# COLUMNA OBJETIVO
# =========================

column_index = 0
target_column = df.columns[column_index]

print(f"\nColumna seleccionada: {target_column}")

# =========================
# MENÚ DE FILAS
# =========================

while True:

    print("\nOpciones válidas:")
    print("20      -> descarga primeras 20 filas")
    print("1-20    -> descarga filas 1 a 20")
    print("30-35   -> descarga filas 30 a 35")

    user_input = input(
        "\nIngrese cantidad o rango: "
    ).strip()

    try:

        # =========================
        # CASO RANGO
        # =========================

        if "-" in user_input:

            start, end = user_input.split("-")

            start = int(start)
            end = int(end)

            if start <= 0 or end <= 0:
                raise ValueError(
                    "No se permiten números negativos o cero."
                )

            if start > end:
                raise ValueError(
                    "El inicio no puede ser mayor que el final."
                )

        # =========================
        # CASO SIMPLE
        # =========================

        else:

            cantidad = int(user_input)

            if cantidad <= 0:
                raise ValueError(
                    "La cantidad debe ser mayor a cero."
                )

            start = 1
            end = cantidad

        break

    except Exception as e:

        print(f"\n[ERROR] {e}")
        print("Intente nuevamente.")

# =========================
# EXTRAER IDS
# =========================

ml_numbers = (
    df[target_column]
    .dropna()
    .iloc[start - 1:end]
)

print(
    f"\nSe descargarán "
    f"{len(ml_numbers)} archivos."
)

# =========================
# DESCARGA
# =========================

BASE_URL = (
    "https://cdn.download.ams.birds.cornell.edu/"
    "api/v2/asset/{}/mp3"
)

try:

    for index, ml_number in enumerate(ml_numbers, start=start):

        try:

            # Normalizar floats tipo 12345.0
            ml_number = str(int(float(ml_number)))

            url = BASE_URL.format(ml_number)

            output_file = (
                Path(OUTPUT_DIR) / f"{ml_number}.mp3"
            )

            # Evitar redescarga
            if output_file.exists():

                print(
                    f"[{index}] SKIP -> "
                    f"Ya existe"
                )

                continue

            response = requests.get(url, timeout=30)

            if response.status_code == 200:

                with open(output_file, "wb") as f:
                    f.write(response.content)

                print(
                    f"[{index}] OK -> "
                    f"{output_file.name}"
                )

            else:

                print(
                    f"[{index}] ERROR -> "
                    f"HTTP {response.status_code}"
                )

        except Exception as e:

            print(
                f"[{index}] EXCEPCIÓN -> {e}"
            )

except KeyboardInterrupt:

    print("\n\nProceso interrumpido por el usuario.")

print("\nProceso finalizado.")