"""
Módulo de excepciones personalizadas del sistema Software FJ.

Todas las excepciones heredan de SoftwareFJError, de modo que el programa
principal pueda capturar cualquier error propio del proyecto con un solo
`except SoftwareFJError`, sin mezclarlo con errores genéricos de Python.
"""


class SoftwareFJError(Exception):
    """Clase base de todas las excepciones del sistema Software FJ."""


# ---------------------------- Errores de Cliente ----------------------------
class ClienteError(SoftwareFJError):
    """Error base para todo lo relacionado con clientes."""


class DocumentoInvalidoError(ClienteError):
    """El documento de identidad está vacío, no es numérico o es muy corto."""


class CorreoInvalidoError(ClienteError):
    """El correo electrónico no cumple el formato estándar."""


class TelefonoInvalidoError(ClienteError):
    """El teléfono no es un celular colombiano válido (10 dígitos, inicia en 3)."""


class NombreInvalidoError(ClienteError):
    """El nombre del cliente está vacío o contiene solo espacios."""


# ---------------------------- Errores de Servicio ---------------------------
class ServicioError(SoftwareFJError):
    """Error base para todo lo relacionado con servicios."""


class ServicioNoDisponibleError(ServicioError):
    """Se intentó contratar un servicio marcado como no disponible."""


class ParametroServicioInvalidoError(ServicioError):
    """Los parámetros de creación o de cálculo de costo de un servicio son inválidos."""


# ---------------------------- Errores de Reserva ----------------------------
class ReservaError(SoftwareFJError):
    """Error base para todo lo relacionado con reservas."""


class ReservaInvalidaError(ReservaError):
    """Los datos de la reserva (duración, cálculo de costo, etc.) son inválidos."""


class EstadoReservaInvalidoError(ReservaError):
    """Se intentó una transición de estado no permitida (p. ej. procesar una reserva pendiente)."""
