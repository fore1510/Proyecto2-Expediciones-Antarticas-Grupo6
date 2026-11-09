"""Proyecto 2 - expediciones antárticas. Python estándar, sin paquetes externos."""
from pathlib import Path
import sqlite3

DIR = Path(__file__).resolve().parent
DB = DIR / 'expediciones_antarticas.db'


def conectar():
    con = sqlite3.connect(DB)
    con.execute('PRAGMA foreign_keys = ON')
    return con


def inicializar():
    with conectar() as con:
        con.executescript((DIR / '01_esquema.sql').read_text(encoding='utf-8'))
        if con.execute('SELECT COUNT(*) FROM pais').fetchone()[0] == 0:
            con.executescript((DIR / '02_datos.sql').read_text(encoding='utf-8'))
    print('Base lista:', DB)


def mostrar_consultas():
    # Separa consultas por ; porque las cinco consultas no contienen ; internos.
    consultas = [s.strip() for s in (DIR / '03_consultas.sql').read_text(encoding='utf-8').split(';') if s.strip()]
    with conectar() as con:
        for numero, consulta in enumerate(consultas, start=1):
            cur = con.execute(consulta)
            print(f'\nCONSULTA {numero}')
            print(' | '.join(col[0] for col in cur.description))
            for fila in cur.fetchall():
                print(' | '.join(str(v) for v in fila))


def registrar_muestra():
    """Inserta una muestra genérica (sin especializar) y la mantiene tras cerrar conexión."""
    codigo = input('Código único (ej. M99): ').strip().upper()
    descripcion = input('Descripción: ').strip()
    fecha = input('Fecha de hallazgo (AAAA-MM-DD): ').strip()
    if not codigo or not descripcion or not fecha:
        print('No se guardó: los campos son obligatorios.')
        return
    try:
        with conectar() as con:
            con.execute('INSERT INTO muestra (codigo_muestra, descripcion, fecha_hallazgo, estado_conservacion, tipo_especializacion) VALUES (?, ?, ?, ?, NULL)', (codigo, descripcion, fecha, 'Pendiente'))
        print('Guardado permanente (COMMIT). Cierra y vuelve a abrir para verificar.')
    except sqlite3.IntegrityError as exc:
        print('Error de integridad:', exc)


def verificar():
    codigo = input('Código de muestra que deseas consultar: ').strip().upper()
    with conectar() as con:
        fila = con.execute('SELECT codigo_muestra,descripcion,fecha_hallazgo FROM muestra WHERE codigo_muestra=?', (codigo,)).fetchone()
    print('Resultado:', fila if fila else 'No existe')


def main():
    inicializar()
    while True:
        print('\n1) Ver las 5 consultas  2) Insertar muestra  3) Verificar muestra  4) Salir')
        opcion = input('Opción: ').strip()
        if opcion == '1': mostrar_consultas()
        elif opcion == '2': registrar_muestra()
        elif opcion == '3': verificar()
        elif opcion == '4': break
        else: print('Opción no válida.')

if __name__ == '__main__':
    main()
