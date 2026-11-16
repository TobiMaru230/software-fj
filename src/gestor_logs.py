"""Gestor centralizado de logs: guarda eventos y errores en un archivo de texto."""
from datetime import datetime


class GestorLogs:
    """Escribe cada evento en `registro_eventos.txt` sin usar bases de datos.

    El método `registrar` nunca lanza excepciones: si el log falla, el
    sistema sigue funcionando (requisito de estabilidad de la actividad).
    """

    _archivo_log = "registro_eventos.txt"   # ruta del archivo (main.py puede cambiarla)
    eventos_escritos = 0                    # eventos guardados correctamente
    eventos_perdidos = 0                    # intentos de escritura que fallaron

    @classmethod
    def registrar(cls, nivel: str, mensaje: str, excepcion: Exception = None) -> None:
        """Agrega una línea al log con fecha, nivel, mensaje y, si existe, la excepción y su causa."""
        escrito = False
        try:
            marca_tiempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            linea = f"[{marca_tiempo}] [{nivel.upper()}] {mensaje}"
            if excepcion is not None:
                linea += f" | Excepción: {type(excepcion).__name__}: {excepcion}"
                # Si la excepción fue encadenada (raise ... from ...), se registra la causa original.
                if excepcion.__cause__ is not None:
                    causa = excepcion.__cause__
                    linea += f" | Causa original: {type(causa).__name__}: {causa}"
            with open(cls._archivo_log, "a", encoding="utf-8") as archivo:
                archivo.write(linea + "\n")
        except Exception as error:          # un fallo del log no debe detener la aplicación
            print(f"Error crítico escribiendo en el log: {error}")
        else:
            escrito = True                  # solo se ejecuta si el try terminó sin errores
            cls.eventos_escritos += 1
        finally:
            if not escrito:                 # se ejecuta siempre; contabiliza los fallos
                cls.eventos_perdidos += 1
