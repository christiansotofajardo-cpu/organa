from datetime import date as Date
from typing import List, Optional

from pydantic import BaseModel, Field


# ============================================================
# ORGANA · DATA MODELS
# ============================================================


class Step(BaseModel):
    """
    Paso concreto dentro de un frente.
    """

    title: str
    completed: bool = False


class Milestone(BaseModel):
    """
    Hito temporal relevante dentro de un frente.
    """

    title: str
    date: Optional[Date] = None
    completed: bool = False


class Front(BaseModel):
    """
    Unidad central de Organa.

    Un frente representa cualquier asunto que debe
    mantenerse organizado sin necesidad de mantenerlo
    permanentemente en la memoria operativa.
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

    deadline: Optional[Date] = None

    next_review: Optional[Date] = None

    start_date: Optional[Date] = None

    last_touched: Optional[Date] = None

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
