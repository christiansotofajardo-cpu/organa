from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field


class Step(BaseModel):
    """
    Una acción concreta dentro de un frente.
    Ejemplo: revisar bases, preparar presupuesto, enviar propuesta.
    """
    title: str
    completed: bool = False


class Milestone(BaseModel):
    """
    Un hito relevante dentro del frente.
    Puede ser un deadline, entrega, revisión, resultado esperado, etc.
    """
    title: str
    date: Optional[date] = None
    completed: bool = False


class Front(BaseModel):
    """
    Unidad básica de trabajo de Organa.

    Un frente puede ser:
    - un paper
    - una licitación
    - un proyecto
    - una tesis
    - una clase
    - una tecnología
    - una prueba o trabajo escolar
    - cualquier compromiso que evolucione en el tiempo
    """

    # IDENTIDAD
    id: str
    name: str
    area: str
    description: Optional[str] = None

    # ESTADO GENERAL
    status: str = "active"
    importance: int = Field(default=3, ge=1, le=5)

    # TIEMPO
    start_date: Optional[date] = None
    deadline: Optional[date] = None
    next_review: Optional[date] = None
    last_touched: Optional[date] = None

    # CARGA Y AVANCE
    progress: int = Field(default=0, ge=0, le=100)
    estimated_hours_total: Optional[float] = None
    estimated_hours_remaining: Optional[float] = None

    # ACCIÓN
    next_action: Optional[str] = None
    suggested_session_minutes: Optional[int] = None

    # DESPLIEGUE DEL FRENTE
    steps: List[Step] = Field(default_factory=list)
    milestones: List[Milestone] = Field(default_factory=list)

    # MEMORIA EXTERNA
    notes: Optional[str] = None
    links: List[str] = Field(default_factory=list)

    # ESTADO REGULATORIO
    # Más adelante regulator.py calculará estos campos.
    attention_state: Optional[str] = None
    attention_reason: Optional[str] = None
