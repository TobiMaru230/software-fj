"""Clase abstracta base de las entidades generales del sistema."""
from abc import ABC, abstractmethod


class EntidadSistema(ABC):
    """Representa cualquier entidad del sistema (clientes, servicios, etc.).

    Al ser abstracta no puede instanciarse directamente: obliga a las
    clases hijas a implementar `obtener_detalles`.
    """

    def __init__(self, identificador: str):
        # Atributo "protegido": se accede mediante la propiedad `identificador`.
        self._identificador = identificador

    @property
    def identificador(self) -> str:
        """Identificador único de la entidad (solo lectura)."""
        return self._identificador

    @abstractmethod
    def obtener_detalles(self) -> str:
        """Devuelve una descripción legible de la entidad."""
