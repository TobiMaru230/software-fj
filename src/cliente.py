"""Clase Cliente: datos personales encapsulados y validados."""
import re

from entidades_base import EntidadSistema
from excepciones import (CorreoInvalidoError, DocumentoInvalidoError,
                         NombreInvalidoError, TelefonoInvalidoError)
from gestor_logs import GestorLogs


class Cliente(EntidadSistema):
    """Cliente del sistema. Cada atributo se valida en su setter (encapsulación)."""

    def __init__(self, identificador: str, nombre: str, correo: str, telefono: str):
        super().__init__(identificador)
        # Se asigna mediante las propiedades para que SIEMPRE pasen por la validación.
        self.documento = identificador
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    # ------------------------------ documento ------------------------------
    @property
    def documento(self) -> str:
        return self._identificador

    @documento.setter
    def documento(self, valor: str) -> None:
        try:
            texto = str(valor).strip()
            if not texto.isdigit() or len(texto) < 6:
                raise DocumentoInvalidoError(
                    f"Documento inválido: '{valor}'. Debe tener solo dígitos y al menos 6 caracteres.")
        except DocumentoInvalidoError as error:
            GestorLogs.registrar("ERROR", "Fallo en validación de documento de cliente", error)
            raise                           # se propaga para que el llamador decida
        else:
            self._identificador = texto     # solo se guarda si la validación fue exitosa

    # -------------------------------- nombre --------------------------------
    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        try:
            if not valor or not str(valor).strip():
                raise NombreInvalidoError("El nombre del cliente no puede estar vacío.")
        except NombreInvalidoError as error:
            GestorLogs.registrar("ERROR", "Fallo en validación de nombre de cliente", error)
            raise
        else:
            self._nombre = str(valor).strip()

    # -------------------------------- correo --------------------------------
    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor: str) -> None:
        try:
            patron = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
            if not valor or not re.match(patron, valor):
                raise CorreoInvalidoError(f"Formato de correo electrónico inválido: '{valor}'.")
        except CorreoInvalidoError as error:
            GestorLogs.registrar("ERROR", "Fallo en validación de correo electrónico", error)
            raise
        else:
            self._correo = valor

    # ------------------------------- teléfono -------------------------------
    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        try:
            # Celular colombiano: 10 dígitos y el primero es 3.
            if not valor or not re.fullmatch(r"3\d{9}", str(valor).strip()):
                raise TelefonoInvalidoError(
                    f"Teléfono inválido: '{valor}'. Debe ser un celular de 10 dígitos que inicie en 3.")
        except TelefonoInvalidoError as error:
            GestorLogs.registrar("ERROR", "Fallo en validación de teléfono de cliente", error)
            raise
        else:
            self._telefono = str(valor).strip()

    def obtener_detalles(self) -> str:
        return (f"Cliente: {self.nombre} | Documento: {self.documento} | "
                f"Correo: {self.correo} | Teléfono: {self.telefono}")
