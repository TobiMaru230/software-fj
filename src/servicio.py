"""Clase abstracta Servicio y sus tres servicios especializados."""
from abc import abstractmethod

from entidades_base import EntidadSistema
from excepciones import ParametroServicioInvalidoError
from gestor_logs import GestorLogs


class Servicio(EntidadSistema):
    """Servicio genérico. Cada hijo define cómo calcula su costo (polimorfismo)."""

    # Nombre del parámetro de duración que usa `calcular_costo` en cada servicio hijo.
    PARAM_DURACION = "unidades"

    def __init__(self, identificador: str, nombre_servicio: str, costo_base: float,
                 disponible: bool = True):
        super().__init__(identificador)
        self.nombre_servicio = nombre_servicio
        self.costo_base = costo_base        # pasa por el setter (validación)
        self.disponible = disponible

    @property
    def costo_base(self) -> float:
        return self._costo_base

    @costo_base.setter
    def costo_base(self, valor: float) -> None:
        try:
            if isinstance(valor, bool) or not isinstance(valor, (int, float)) or valor < 0:
                raise ParametroServicioInvalidoError(
                    f"El costo base debe ser un número mayor o igual a cero: {valor!r}")
        except ParametroServicioInvalidoError as error:
            GestorLogs.registrar("ERROR", "Costo base inválido en servicio", error)
            raise
        else:
            self._costo_base = float(valor)

    @abstractmethod
    def calcular_costo(self, *args, **kwargs) -> float:
        """Calcula el costo. Cada hijo lo 'sobrecarga' con parámetros opcionales distintos."""

    @abstractmethod
    def obtener_detalles(self) -> str:
        """Descripción legible del servicio."""


class ReservaSala(Servicio):
    """Servicio 1: reserva de salas de trabajo o conferencias (se cobra por hora)."""

    PARAM_DURACION = "horas"
    COSTO_PROYECTOR_HORA = 15000
    IVA = 1.19

    def __init__(self, identificador: str, costo_base: float, capacidad_personas: int,
                 proyector: bool = True):
        super().__init__(identificador, "Reserva de Sala", costo_base)
        self.capacidad_personas = capacidad_personas
        self.proyector = proyector

    def calcular_costo(self, horas: int = 1, incluir_iva: bool = True,
                       descuento_porcentaje: float = 0.0) -> float:
        """Variantes: solo horas, con/sin IVA y con descuento porcentual opcional."""
        try:
            if horas <= 0:
                raise ParametroServicioInvalidoError(
                    "El número de horas para reservar la sala debe ser mayor a cero.")
            if not 0 <= descuento_porcentaje <= 100:
                raise ParametroServicioInvalidoError(
                    "El descuento debe estar entre 0 y 100 por ciento.")
            subtotal = self.costo_base * horas
            if self.proyector:
                subtotal += self.COSTO_PROYECTOR_HORA * horas
            subtotal -= subtotal * (descuento_porcentaje / 100.0)
            if incluir_iva:
                subtotal *= self.IVA
            return round(subtotal, 2)
        except Exception as error:
            GestorLogs.registrar("ERROR", f"Error calculando costo de ReservaSala {self.identificador}", error)
            raise

    def obtener_detalles(self) -> str:
        return (f"[Sala] ID: {self.identificador} | Capacidad: {self.capacidad_personas} pers. | "
                f"Proyector: {'Sí' if self.proyector else 'No'} | Base/hora: ${self.costo_base}")


class AlquilerEquipo(Servicio):
    """Servicio 2: alquiler de equipos tecnológicos (se cobra por día de 8 horas)."""

    PARAM_DURACION = "dias"
    HORAS_POR_DIA = 8
    COSTO_SEGURO_DIA = 25000

    def __init__(self, identificador: str, costo_base: float, modelo_equipo: str):
        super().__init__(identificador, "Alquiler de Equipo", costo_base)
        self.modelo_equipo = modelo_equipo

    def calcular_costo(self, dias: int = 1, seguro_incluido: bool = False) -> float:
        """Variantes: solo días, o días con seguro opcional."""
        try:
            if dias <= 0:
                raise ParametroServicioInvalidoError("Los días de alquiler deben ser mayores a cero.")
            subtotal = self.costo_base * self.HORAS_POR_DIA * dias
            if seguro_incluido:
                subtotal += self.COSTO_SEGURO_DIA * dias
            return round(subtotal, 2)
        except Exception as error:
            GestorLogs.registrar("ERROR", f"Error calculando costo de AlquilerEquipo {self.identificador}", error)
            raise

    def obtener_detalles(self) -> str:
        return (f"[Equipo] ID: {self.identificador} | Modelo: {self.modelo_equipo} | "
                f"Base/hora: ${self.costo_base}")


class AsesoriaEspecializada(Servicio):
    """Servicio 3: asesorías en arquitectura de software y POO (se cobra por sesión)."""

    PARAM_DURACION = "sesiones"
    DESCUENTO_CORPORATIVO = 0.15

    def __init__(self, identificador: str, costo_base: float, especialista: str,
                 nivel_experiencia: str = "Senior"):
        super().__init__(identificador, "Asesoría Especializada", costo_base)
        self.especialista = especialista
        self.nivel_experiencia = nivel_experiencia

    def calcular_costo(self, sesiones: int = 1, paquete_corporativo: bool = False) -> float:
        """Variantes: solo sesiones, o paquete corporativo con 15 % de descuento."""
        try:
            if sesiones <= 0:
                raise ParametroServicioInvalidoError("El número de sesiones debe ser mayor a cero.")
            subtotal = self.costo_base * sesiones
            if paquete_corporativo:
                subtotal *= (1 - self.DESCUENTO_CORPORATIVO)
            return round(subtotal, 2)
        except Exception as error:
            GestorLogs.registrar("ERROR", f"Error calculando costo de AsesoriaEspecializada {self.identificador}", error)
            raise

    def obtener_detalles(self) -> str:
        return (f"[Asesoría] ID: {self.identificador} | Especialista: {self.especialista} "
                f"({self.nivel_experiencia}) | Base/sesión: ${self.costo_base}")
