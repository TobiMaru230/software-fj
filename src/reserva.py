"""Clase Reserva: integra cliente, servicio, duración y estado."""
from cliente import Cliente
from excepciones import (EstadoReservaInvalidoError, ReservaInvalidaError,
                         ServicioNoDisponibleError)
from gestor_logs import GestorLogs
from servicio import Servicio


class Reserva:
    """Ciclo de vida: Pendiente -> Confirmada -> Procesada, o Cancelada en cualquier punto previo."""

    ESTADOS_VALIDOS = ("Pendiente", "Confirmada", "Cancelada", "Procesada")

    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio, duracion_unidades: int):
        self.id_reserva = id_reserva
        self.cliente = cliente
        self.servicio = servicio
        self.duracion_unidades = duracion_unidades   # pasa por el setter (validación)
        self._estado = "Pendiente"
        self.costo_total = 0.0
        self.comprobante = None

    # ------------------------------ duración ------------------------------
    @property
    def duracion_unidades(self) -> int:
        return self._duracion_unidades

    @duracion_unidades.setter
    def duracion_unidades(self, valor: int) -> None:
        try:
            if isinstance(valor, bool) or not isinstance(valor, int) or valor <= 0:
                raise ReservaInvalidaError(
                    f"La duración de la reserva debe ser un entero mayor a 0. Valor recibido: {valor!r}")
        except ReservaInvalidaError as error:
            GestorLogs.registrar("ERROR", "Duración de reserva inválida", error)
            raise
        else:
            self._duracion_unidades = valor

    # ------------------------------- estado -------------------------------
    @property
    def estado(self) -> str:
        return self._estado

    @estado.setter
    def estado(self, valor: str) -> None:
        if valor not in self.ESTADOS_VALIDOS:
            raise EstadoReservaInvalidoError(f"Estado desconocido: '{valor}'.")
        self._estado = valor

    def _exigir_estado(self, permitidos: tuple, accion: str) -> None:
        """Verifica que la reserva esté en un estado desde el cual se puede ejecutar la acción."""
        if self.estado not in permitidos:
            error = EstadoReservaInvalidoError(
                f"No se puede {accion} la reserva {self.id_reserva} en estado '{self.estado}'. "
                f"Estados permitidos: {', '.join(permitidos)}.")
            GestorLogs.registrar("ERROR", f"Transición de estado no permitida al {accion}", error)
            raise error

    # --------------------------- confirmar reserva ---------------------------
    def confirmar_reserva(self, **opciones_costo) -> None:
        """Confirma la reserva: valida disponibilidad y calcula el costo total.

        `opciones_costo` se reenvía a `calcular_costo` del servicio (p. ej. incluir_iva=False).
        """
        self._exigir_estado(("Pendiente",), "confirmar")
        try:
            if not self.servicio.disponible:
                raise ServicioNoDisponibleError(
                    f"El servicio '{self.servicio.nombre_servicio}' "
                    f"(ID: {self.servicio.identificador}) no se encuentra disponible.")
            # Polimorfismo: cada servicio indica cómo se llama su parámetro de duración.
            duracion = {self.servicio.PARAM_DURACION: self.duracion_unidades}
            costo = self.servicio.calcular_costo(**duracion, **opciones_costo)
        except ServicioNoDisponibleError as error:
            self.estado = "Cancelada"
            GestorLogs.registrar("ERROR", f"Fallo al confirmar reserva {self.id_reserva}", error)
            raise                                       # se propaga tal cual
        except Exception as causa:
            # Encadenamiento: se envuelve el error original en uno propio del proyecto.
            self.estado = "Cancelada"
            envuelta = ReservaInvalidaError(f"No fue posible calcular la reserva {self.id_reserva}.")
            envuelta.__cause__ = causa                  # para que el log registre la causa
            GestorLogs.registrar("ERROR", "Error en confirmación de reserva", envuelta)
            raise envuelta from causa
        else:
            # Solo si no hubo ninguna excepción se confirma la reserva.
            self.costo_total = costo
            self.estado = "Confirmada"
            GestorLogs.registrar("INFO", f"Reserva {self.id_reserva} confirmada. Costo total: ${self.costo_total}")

    # --------------------------- procesar reserva ---------------------------
    def procesar_reserva(self) -> None:
        """Procesa una reserva confirmada y genera su comprobante."""
        self._exigir_estado(("Confirmada",), "procesar")
        try:
            if self.costo_total <= 0:
                raise ReservaInvalidaError(f"La reserva {self.id_reserva} no tiene un costo total válido.")
            comprobante = f"CMP-{self.id_reserva}-{self.cliente.documento}"
        except ReservaInvalidaError as error:
            GestorLogs.registrar("ERROR", f"Fallo al procesar reserva {self.id_reserva}", error)
            raise
        else:
            self.comprobante = comprobante
            self.estado = "Procesada"
            GestorLogs.registrar("INFO", f"Reserva {self.id_reserva} procesada. Comprobante: {comprobante}")
        finally:
            # Se ejecuta siempre, haya o no error.
            GestorLogs.registrar("INFO", f"Finalizó el intento de procesar la reserva {self.id_reserva}")

    # --------------------------- cancelar reserva ---------------------------
    def cancelar_reserva(self) -> None:
        """Cancela una reserva pendiente o confirmada (try/finally: el cierre se registra siempre)."""
        try:
            self._exigir_estado(("Pendiente", "Confirmada"), "cancelar")
            self.estado = "Cancelada"
            GestorLogs.registrar("INFO", f"Reserva {self.id_reserva} cancelada manualmente.")
        finally:
            GestorLogs.registrar("INFO", f"Finalizó el intento de cancelar la reserva {self.id_reserva} "
                                         f"(estado actual: {self.estado})")

    def obtener_resumen(self) -> str:
        return (f"Reserva [{self.id_reserva}] | Estado: {self.estado} | Cliente: {self.cliente.nombre} | "
                f"Servicio: {self.servicio.nombre_servicio} | Duración: {self.duracion_unidades} | "
                f"Total: ${self.costo_total}")
