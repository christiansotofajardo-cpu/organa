from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field


# ============================================================
# ORGANA · DATA MODELS
# ============================================================


class Step(BaseModel):
    """
    Paso concreto dentro de un frente.

    Permite desplegar un frente y ver qué acciones
    específicas contiene.
    """

    title: str
    completed: bool = False


class Milestone(BaseModel):
    """
    Hito temporal relevante dentro de un frente.

    Ejemplos:
    - fecha de postulación
    - entrega
    - reunión
    - resultado esperado
    - revisión
    """

    title: str

    # IMPORTANTE:
    # Debe aceptar fechas reales del JSON como:
    # "2026-09-23"
    #
    # Pydantic convierte automáticamente ese string
    # ISO a datetime.date.
    date: Optional[date] = None

    completed: bool = False


class Front(BaseModel):
    """
    Unidad central de Organa.

    Un frente representa cualquier asunto que debe
    mantenerse organizado sin necesidad de mantenerlo
    permanentemente en la memoria operativa.

    Puede ser:
    - proyecto
    - licitación
    - paper
    - tecnología
    - tesis
    - docencia
    - consultoría
    - actividad personal
    - oportunidad futura
    """

    # --------------------------------------------------------
    # IDENTIDAD
    # --------------------------------------------------------

    id: str

    name: str

    area: str = "General"

    description: Optional[str] = None


    # --------------------------------------------------------
    # ESTADO
    # --------------------------------------------------------

    # Valores esperados, por ejemplo:
    #
    # active
    # waiting
    # sleeping
    # closed

    status: str = "active"


    # --------------------------------------------------------
    # IMPORTANCIA
    # --------------------------------------------------------

    importance: int = Field(
        default=3,
        ge=1,
        le=5
    )


    # --------------------------------------------------------
    # PROGRESO
    # --------------------------------------------------------

    progress: int = Field(
        default=0,
        ge=0,
        le=100
    )


    # --------------------------------------------------------
    # CARGA ESTIMADA
    # --------------------------------------------------------

    estimated_hours_remaining: Optional[float] = Field(
        default=None,
        ge=0
    )

    suggested_session_minutes: Optional[int] = Field(
        default=None,
        ge=5
    )


    # --------------------------------------------------------
    # FECHAS
    # --------------------------------------------------------

    deadline: Optional[date] = None

    next_review: Optional[date] = None

    start_date: Optional[date] = None

    last_touched: Optional[date] = None


    # --------------------------------------------------------
    # ACCIÓN
    # --------------------------------------------------------

    next_action: Optional[str] = None

    steps: List[Step] = Field(
        default_factory=list
    )


    # --------------------------------------------------------
    # HITOS
    # --------------------------------------------------------

    milestones: List[Milestone] = Field(
        default_factory=list
    )


    # --------------------------------------------------------
    # REGULACIÓN
    # --------------------------------------------------------

    # Estos campos permiten guardar eventualmente
    # una decisión regulatoria explícita.
    #
    # El regulator.py puede calcularla dinámicamente,
    # pero mantenemos estos campos porque forman parte
    # del modelo original de Organa.

    attention_state: Optional[str] = None

    attention_reason: Optional[str] = None


    # --------------------------------------------------------
    # INFORMACIÓN COMPLEMENTARIA
    # --------------------------------------------------------

    notes: Optional[str] = None

    links: List[str] = Field(
        default_factory=list
    )

    tags: List[str] = Field(
        default_factory=list
    )
