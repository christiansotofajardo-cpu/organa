from datetime import date
from typing import Optional, Dict, Any

from models import Front


# ============================================================
# ORGANA REGULATOR
# ------------------------------------------------------------
# Primera versión transparente del motor regulador.
#
# Su objetivo NO es maximizar productividad.
#
# Intenta responder:
#
# "¿Cuánta atención necesita este frente AHORA?"
#
# Estados:
#
# RED     -> requiere atención
# ORANGE  -> atención próxima
# YELLOW  -> conviene avanzar preventivamente
# GREEN   -> trayectoria adecuada
# BLUE    -> bajo control / puede salir de la atención
#
# Esta V1 utiliza reglas explícitas y comprensibles.
# Posteriormente podremos incorporar modelos más sofisticados.
# ============================================================


ATTENTION_RED = "red"
ATTENTION_ORANGE = "orange"
ATTENTION_YELLOW = "yellow"
ATTENTION_GREEN = "green"
ATTENTION_BLUE = "blue"


def days_until(target: Optional[date], today: date) -> Optional[int]:
    """
    Días desde hoy hasta una fecha.
    Devuelve None cuando no existe fecha.
    """
    if target is None:
        return None

    return (target - today).days


def days_since(target: Optional[date], today: date) -> Optional[int]:
    """
    Días transcurridos desde una fecha.
    """
    if target is None:
        return None

    return (today - target).days


def calculate_pressure(front: Front, today: Optional[date] = None) -> float:
    """
    Calcula una presión operativa aproximada entre 0 y 100.

    IMPORTANTE:
    presión != importancia

    Un frente puede ser extremadamente importante y tener
    presión actual muy baja.

    Esta función considera:
    - proximidad del deadline
    - horas pendientes
    - importancia
    - tiempo sin intervención
    - avance
    """

    if today is None:
        today = date.today()

    # --------------------------------------------------------
    # Los frentes esperando o dormidos no generan presión
    # antes de su fecha de revisión.
    # --------------------------------------------------------

    if front.status in {"waiting", "sleeping"}:

        if front.next_review is None:
            return 0.0

        if today < front.next_review:
            return 0.0

    pressure = 0.0

    # --------------------------------------------------------
    # 1. PRESIÓN POR DEADLINE
    # Máximo aproximado: 40 puntos
    # --------------------------------------------------------

    deadline_days = days_until(front.deadline, today)

    if deadline_days is not None:

        if deadline_days < 0:
            pressure += 45

        elif deadline_days <= 2:
            pressure += 40

        elif deadline_days <= 5:
            pressure += 32

        elif deadline_days <= 10:
            pressure += 24

        elif deadline_days <= 21:
            pressure += 14

        elif deadline_days <= 45:
            pressure += 7

    # --------------------------------------------------------
    # 2. TRABAJO RESTANTE
    # Máximo aproximado: 20 puntos
    # --------------------------------------------------------

    hours = front.estimated_hours_remaining

    if hours is not None:

        if hours >= 20:
            pressure += 20

        elif hours >= 10:
            pressure += 15

        elif hours >= 5:
            pressure += 10

        elif hours > 0:
            pressure += 5

    # --------------------------------------------------------
    # 3. IMPORTANCIA
    # Máximo: 15 puntos
    # --------------------------------------------------------

    pressure += front.importance * 3

    # --------------------------------------------------------
    # 4. TIEMPO SIN TOCAR EL FRENTE
    # Máximo aproximado: 15 puntos
    #
    # Esto protege especialmente los proyectos importantes
    # que todavía no son urgentes.
    # --------------------------------------------------------

    untouched_days = days_since(front.last_touched, today)

    if untouched_days is not None:

        if untouched_days >= 21:
            pressure += 15

        elif untouched_days >= 14:
            pressure += 11

        elif untouched_days >= 7:
            pressure += 7

        elif untouched_days >= 3:
            pressure += 3

    # --------------------------------------------------------
    # 5. AVANCE
    # Máximo aproximado: 10 puntos
    # --------------------------------------------------------

    if front.progress < 20:
        pressure += 10

    elif front.progress < 40:
        pressure += 7

    elif front.progress < 70:
        pressure += 4

    # --------------------------------------------------------
    # Si ya está completado, eliminamos presión.
    # --------------------------------------------------------

    if front.progress >= 100 and front.status != "active":
        pressure = 0

    return min(round(pressure, 1), 100.0)


def determine_attention(
    front: Front,
    today: Optional[date] = None
) -> Dict[str, Any]:
    """
    Traduce el estado del frente a una recomendación regulatoria.

    Devuelve:
    - state
    - label
    - reason
    - pressure
    - requires_action
    """

    if today is None:
        today = date.today()

    # ========================================================
    # CIERRE COGNITIVO
    # ========================================================

    if front.status == "closed":
        return {
            "state": ATTENTION_BLUE,
            "label": "Cerrado",
            "reason": "Este frente está cerrado.",
            "pressure": 0,
            "requires_action": False
        }

    # ========================================================
    # ESPERA
    # ========================================================

    if front.status == "waiting":

        if front.next_review and today < front.next_review:

            remaining = (front.next_review - today).days

            return {
                "state": ATTENTION_BLUE,
                "label": "Bajo control",
                "reason": (
                    f"Está en espera. No requiere atención durante "
                    f"los próximos {remaining} días."
                ),
                "pressure": 0,
                "requires_action": False
            }

    # ========================================================
    # DORMIDO
    # ========================================================

    if front.status == "sleeping":

        if front.next_review and today < front.next_review:

            return {
                "state": ATTENTION_BLUE,
                "label": "Dormido",
                "reason": (
                    f"No corresponde retomarlo hasta "
                    f"{front.next_review.strftime('%d/%m/%Y')}."
                ),
                "pressure": 0,
                "requires_action": False
            }

    # ========================================================
    # CALCULAR PRESIÓN
    # ========================================================

    pressure = calculate_pressure(front, today)

    deadline_days = days_until(front.deadline, today)

    # ========================================================
    # ROJO
    # ========================================================

    if pressure >= 70:

        return {
            "state": ATTENTION_RED,
            "label": "Atender",
            "reason": (
                "La combinación de plazo, carga pendiente y estado "
                "del frente requiere atención."
            ),
            "pressure": pressure,
            "requires_action": True
        }

    # ========================================================
    # NARANJA
    # ========================================================

    if pressure >= 50:

        return {
            "state": ATTENTION_ORANGE,
            "label": "Atención próxima",
            "reason": (
                "Conviene intervenir pronto para evitar una "
                "concentración futura de carga."
            ),
            "pressure": pressure,
            "requires_action": True
        }

    # ========================================================
    # AMARILLO
    #
    # Aquí vive uno de los principios centrales de Organa:
    # trabajar ANTES de que algo sea urgente.
    # ========================================================

    if pressure >= 30:

        return {
            "state": ATTENTION_YELLOW,
            "label": "Conviene avanzar",
            "reason": (
                "No existe urgencia inmediata, pero un avance "
                "preventivo mantiene una trayectoria saludable."
            ),
            "pressure": pressure,
            "requires_action": True
        }

    # ========================================================
    # DEADLINE LEJANO + TRAYECTORIA CONTROLADA
    # ========================================================

    if deadline_days is not None and deadline_days > 21:

        return {
            "state": ATTENTION_GREEN,
            "label": "Trayectoria adecuada",
            "reason": (
                "El plazo permite mantener el ritmo actual "
                "sin aumentar la carga."
            ),
            "pressure": pressure,
            "requires_action": False
        }

    # ========================================================
    # VERDE GENERAL
    # ========================================================

    return {
        "state": ATTENTION_GREEN,
        "label": "Trayectoria adecuada",
        "reason": (
            "El frente se encuentra en una trayectoria compatible "
            "con su carga actual."
        ),
        "pressure": pressure,
        "requires_action": False
    }


def regulate_front(
    front: Front,
    today: Optional[date] = None
) -> Front:
    """
    Aplica la regulación a un frente y devuelve el mismo
    objeto con attention_state y attention_reason actualizados.
    """

    result = determine_attention(front, today)

    front.attention_state = result["state"]
    front.attention_reason = result["reason"]

    return front
