# Software FJ — Sistema integral de gestión de clientes, servicios y reservas

**Curso:** Programación (213023) — Universidad Nacional Abierta y a Distancia (UNAD)
**Actividad:** Fase 4 — Prácticas simuladas (manejo de excepciones)
**Estudiante:** Brayan Eduardo Torres Álvarez
**Docente:** Ing. Alexander López Téllez, MSc.

## Descripción
Aplicación en Python orientada a objetos, sin bases de datos, que gestiona clientes, servicios
especializados y reservas. Todos los errores se manejan con excepciones propias del proyecto y
cada evento se guarda en `registro_eventos.txt`, sin que la aplicación se detenga ante fallos.

## Estructura
| Archivo | Contenido |
|---|---|
| `main.py` | 16 simulaciones automáticas (válidas e inválidas) |
| `src/excepciones.py` | Jerarquía de excepciones propias (`SoftwareFJError` y derivadas) |
| `src/entidades_base.py` | Clase abstracta `EntidadSistema` |
| `src/cliente.py` | `Cliente` con propiedades y validación de documento, nombre, correo y teléfono |
| `src/servicio.py` | `Servicio` (abstracta) y `ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada` |
| `src/reserva.py` | `Reserva`: confirmar, procesar y cancelar, con control de estados |
| `src/gestor_logs.py` | Registro de eventos y errores en archivo de texto |

## Manejo de excepciones aplicado
- `try/except`: validaciones de `Cliente`, `Servicio` y `Reserva`.
- `try/except/else`: los setters solo asignan el valor en `else`, cuando la validación pasó.
- `try/finally`: `Reserva.cancelar_reserva` registra siempre el cierre del intento.
- `try/except/else/finally`: `Reserva.procesar_reserva` y `GestorLogs.registrar`.
- Encadenamiento: `raise ReservaInvalidaError(...) from causa` en `Reserva.confirmar_reserva`.

## Ejecución
Requiere Python 3.10 o superior:
```bash
python main.py
```
