from typing import List, Optional
from pydantic import BaseModel, Field


class Milestone(BaseModel):
    """
    Hito relevante dentro de un frente.

    Puede representar una fecha límite, una entrega,
    una postulación, un resultado esperado, una reunión
    u otro momento que Organa deba mantener vigilado.
    """

    title: str
    date: Optional[str] = None
    kind: str = "milestone"
    completed: bool = False


class NextStep(BaseModel):
    """
    Acción concreta asociada a un frente.

    La idea es que cada frente pueda desplegarse
    y mostrar qué hay que hacer realmente.
    """

    title: str
    completed: bool = False
    estimated_minutes: Optional[int] = None


class Front(BaseModel):
    """
    Unidad central de Organa.

    Un Front representa algo que ocupa o podría ocupar
    atención: proyecto, paper, tesis, clase, licitación,
    desarrollo tecnológico, actividad personal, etc.

    Organa no pretende mostrar todo permanentemente.
    El regulador decide qué merece estar abierto ahora
    y qué puede permanecer bajo vigilancia.
    """

    id: str
    title: str

    # Clasificación general
    category: str = "general"
    description: Optional[str] = None

    # Estado del frente
    status: str = "active"

    # Importancia estratégica
    importance: int = Field(default=3, ge=1, le=5)

    # Presión subjetiva o externa
    pressure: int = Field(default=1, ge=0, le=5)

    # Energía necesaria para trabajar en él
    energy_required: int = Field(default=2, ge=1, le=5)

    # Tiempo estimado de una sesión útil
    suggested_session_minutes: int = Field(default=30, ge=5)

    # Fechas principales
    deadline: Optional[str] = None
    start_date: Optional[str] = None

    # Última vez que hubo movimiento
    last_touched: Optional[str] = None

    # Momento recomendado para volver a abrirlo
    reopen_date: Optional[str] = None

    # Permite distinguir cosas que simplemente
    # deben permanecer vigiladas
    waiting: bool = False
    sleeping: bool = False

    # Hitos internos
    milestones: List[Milestone] = Field(default_factory=list)

    # Próximas acciones concretas
    next_steps: List[NextStep] = Field(default_factory=list)

    # Información libre para el futuro motor semántico
    notes: Optional[str] = None

    # Etiquetas flexibles
    tags: List[str] = Field(default_factory=list)
