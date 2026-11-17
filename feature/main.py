"""
Software FJ - Fase 4: simulaciones automáticas del sistema.

Ejecuta 16 escenarios (válidos e inválidos) y demuestra que la aplicación
no se detiene ante errores: cada fallo se captura, se muestra y se
registra en `registro_eventos.txt`.
"""
import os
import sys

# Permite importar los módulos de la carpeta src/ sin importar desde dónde se ejecute.
DIRECTORIO_ACTUAL = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(DIRECTORIO_ACTUAL, "src"))

from cliente import Cliente                                              # noqa: E402
from excepciones import SoftwareFJError                                  # noqa: E402
from gestor_logs import GestorLogs                                       # noqa: E402
from reserva import Reserva                                              # noqa: E402
from servicio import AlquilerEquipo, AsesoriaEspecializada, ReservaSala  # noqa: E402


# ----------------------- funciones auxiliares de prueba -----------------------
def _reserva_confirmada(id_reserva, cliente, servicio, duracion, **opciones):
    """Crea y confirma una reserva; la devuelve para seguir probando."""
    reserva = Reserva(id_reserva, cliente, servicio, duracion)
    reserva.confirmar_reserva(**opciones)
    return reserva


def _probar_confirmacion(id_reserva, cliente, servicio, duracion):
    print("->", _reserva_confirmada(id_reserva, cliente, servicio, duracion).obtener_resumen())


def _probar_servicio_no_disponible(cliente, servicio):
    _reserva_confirmada("RES-INACTIVO", cliente, servicio, 1)


def _probar_duracion_invalida(cliente, servicio):
    Reserva("RES-DURACION", cliente, servicio, -3)


def _probar_cancelacion(cliente, servicio):
    reserva = _reserva_confirmada("RES-CANCELAR", cliente, servicio, 3)
    reserva.cancelar_reserva()
    print("->", reserva.obtener_resumen())


def _probar_procesamiento(cliente, servicio):
    reserva = _reserva_confirmada("RES-PROCESAR", cliente, servicio, 1, incluir_iva=False)
    reserva.procesar_reserva()
    print("->", reserva.obtener_resumen(), "| Comprobante:", reserva.comprobante)


def _probar_procesar_sin_confirmar(cliente, servicio):
    Reserva("RES-PENDIENTE", cliente, servicio, 2).procesar_reserva()


def _probar_parametro_inesperado(cliente, servicio):
    # 'descuento_vip' no existe en calcular_costo -> TypeError -> se encadena en ReservaInvalidaError.
    _reserva_confirmada("RES-ENCADENADA", cliente, servicio, 1, descuento_vip=20)


def ejecutar_simulaciones():
    print("=" * 70)
    print("   SISTEMA INTEGRAL DE GESTIÓN SOFTWARE FJ - FASE 4")
    print("   Estudiante: Brayan Eduardo Torres Álvarez")
    print("=" * 70)

    # Se parte de un log limpio en cada ejecución.
    ruta_log = os.path.join(DIRECTORIO_ACTUAL, "registro_eventos.txt")
    GestorLogs._archivo_log = ruta_log
    if os.path.exists(ruta_log):
        os.remove(ruta_log)

    # Objetos base compartidos por las simulaciones.
    c1 = Cliente("1095801234", "Carlos Pérez", "carlos.perez@gmail.com", "3104567890")
    c2 = Cliente("1095805678", "Ana María Gómez", "ana.gomez@unad.edu.co", "3209876543")
    sala = ReservaSala("SR-01", 50000, 15, proyector=True)
    equipo = AlquilerEquipo("EQ-01", 35000, "Dell Latitude 5530")
    asesoria = AsesoriaEspecializada("AS-01", 120000, "Ing. Alexander López", "Senior")
    sala_inactiva = ReservaSala("SR-02", 40000, 8, proyector=False)
    sala_inactiva.disponible = False

    # (descripción, función que ejecuta el escenario)
    simulaciones = [
        ("Registro exitoso de cliente", lambda: print("->", c1.obtener_detalles())),
        ("Documento inválido (letras)", lambda: Cliente("ABC123", "Prueba", "correo@valido.com", "3001112233")),
        ("Correo inválido (sin arroba)", lambda: Cliente("1095809999", "Mal Correo", "correo_sin_arroba.com", "3002223344")),
        ("Teléfono inválido (9 dígitos)", lambda: Cliente("1095809998", "Mal Teléfono", "ok@correo.com", "310456789")),
        ("Costo de sala: 3 h, proyector, 10 % dcto e IVA",
         lambda: print("-> $", sala.calcular_costo(horas=3, incluir_iva=True, descuento_porcentaje=10.0))),
        ("Costo de equipo: 4 días con seguro",
         lambda: print("-> $", equipo.calcular_costo(dias=4, seguro_incluido=True))),
        ("Costo de asesoría: 2 sesiones, paquete corporativo",
         lambda: print("-> $", asesoria.calcular_costo(sesiones=2, paquete_corporativo=True))),
        ("Confirmación exitosa de reserva de sala", lambda: _probar_confirmacion("RES-001", c1, sala, 2)),
        ("Confirmación exitosa de alquiler de equipo", lambda: _probar_confirmacion("RES-002", c2, equipo, 2)),
        ("Servicio no disponible", lambda: _probar_servicio_no_disponible(c1, sala_inactiva)),
        ("Duración de reserva inválida (negativa)", lambda: _probar_duracion_invalida(c2, asesoria)),
        ("Costo base negativo en un servicio", lambda: ReservaSala("SR-ERR", -1000, 5)),
        ("Cancelación manual de una reserva confirmada", lambda: _probar_cancelacion(c1, equipo)),
        ("Procesamiento exitoso de una reserva confirmada", lambda: _probar_procesamiento(c2, sala)),
        ("Procesar una reserva que sigue pendiente", lambda: _probar_procesar_sin_confirmar(c1, asesoria)),
        ("Excepción encadenada (parámetro de costo inesperado)", lambda: _probar_parametro_inesperado(c1, asesoria)),
    ]

    total = len(simulaciones)
    sin_error = 0
    controladas = 0

    for numero, (descripcion, escenario) in enumerate(simulaciones, 1):
        print(f"\n--- [{numero}/{total}] {descripcion} ---")
        try:
            escenario()
        except SoftwareFJError as error:
            controladas += 1
            print(f"Excepción del proyecto controlada: {type(error).__name__} -> {error}")
            if error.__cause__ is not None:   # muestra la causa si la excepción fue encadenada
                print(f"   Causa original: {type(error.__cause__).__name__} -> {error.__cause__}")
        except Exception as error:            # cualquier otro error inesperado tampoco detiene el programa
            controladas += 1
            print(f"Excepción general controlada: {type(error).__name__} -> {error}")
        else:
            sin_error += 1
            print("Resultado: ejecutado sin errores.")
        finally:
            print(f"Sistema estable tras la simulación {numero}.")

    print("\n" + "=" * 70)
    print(f" RESUMEN: {total} simulaciones | {sin_error} sin errores | {controladas} excepciones controladas")
    print(f" Eventos escritos en el log: {GestorLogs.eventos_escritos} | perdidos: {GestorLogs.eventos_perdidos}")
    print("=" * 70)


if __name__ == "__main__":
    ejecutar_simulaciones()
