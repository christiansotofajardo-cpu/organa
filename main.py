import json
from datetime import date
from pathlib import Path
from typing import List, Dict, Any

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from models import Front
from regulator import determine_attention


# ============================================================
# ORGANA
# ============================================================

app = FastAPI(
    title="Organa",
    description="Human-centered workload and attention regulation system.",
    version="0.5.0",
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

FRONTS_FILE = DATA_DIR / "fronts.json"


# ============================================================
# STATIC + TEMPLATES
# ============================================================

app.mount(
    "/static",
    StaticFiles(directory=str(STATIC_DIR)),
    name="static",
)

templates = Jinja2Templates(
    directory=str(TEMPLATES_DIR)
)


# ============================================================
# TEMPORARY TEST DATE
# ------------------------------------------------------------
# Durante esta fase mantenemos la fecha fija para poder
# calibrar el regulador sobre los mismos datos.
#
# Después:
#
#     TEST_TODAY = date.today()
#
# ============================================================

TEST_TODAY = date(2026, 9, 19)


# ============================================================
# VISUAL CONFIG
# ============================================================

STATE_CONFIG = {
    "red": {
        "color": "#d92d20",
        "background": "#fdecec",
    },
    "orange": {
        "color": "#b54708",
        "background": "#fff0df",
    },
    "yellow": {
        "color": "#8a6500",
        "background": "#fff8d8",
    },
    "green": {
        "color": "#23734a",
        "background": "#eaf7ef",
    },
    "blue": {
        "color": "#175cd3",
        "background": "#eaf2ff",
    },
}


# ============================================================
# DATA
# ============================================================

def load_fronts() -> List[Front]:
    """
    Lee fronts.json y convierte cada registro
    en un objeto Front validado por Pydantic.
    """

    with open(
        FRONTS_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    return [
        Front(**item)
        for item in data
    ]


# ============================================================
# DATE HELPERS
# ============================================================

MONTHS_ES = {
    1: "enero",
    2: "febrero",
    3: "marzo",
    4: "abril",
    5: "mayo",
    6: "junio",
    7: "julio",
    8: "agosto",
    9: "septiembre",
    10: "octubre",
    11: "noviembre",
    12: "diciembre",
}


def long_date(value: date) -> str:
    """
    19 de septiembre de 2026
    """

    return (
        f"{value.day} de "
        f"{MONTHS_ES[value.month]} de "
        f"{value.year}"
    )


def full_date(value) -> str:

    if value is None:
        return "Sin fecha"

    return value.strftime("%d/%m/%Y")


def short_date(value) -> str:

    if value is None:
        return "—"

    return value.strftime("%d/%m")


# ============================================================
# PRESENTATION MODEL
# ------------------------------------------------------------
# Esta función transforma Front + Regulator en algo
# directamente utilizable por las vistas.
#
# Los templates NO necesitan entender el algoritmo.
# ============================================================

def present_front(
    front: Front,
    today: date
) -> Dict[str, Any]:

    regulation = determine_attention(
        front,
        today
    )

    state = regulation["state"]

    config = STATE_CONFIG.get(
        state,
        STATE_CONFIG["green"]
    )

    # --------------------------------------------------------
    # Horas
    # --------------------------------------------------------

    if front.estimated_hours_remaining is None:
        hours_text = "Por estimar"
    else:
        hours_text = (
            f"{front.estimated_hours_remaining:g} h"
        )

    # --------------------------------------------------------
    # Sesión sugerida
    # --------------------------------------------------------

    if front.suggested_session_minutes:
        session_text = (
            f"{front.suggested_session_minutes} min"
        )
    else:
        session_text = "Flexible"

    # --------------------------------------------------------
    # Progreso visual
    # --------------------------------------------------------

    visual_progress = max(
        min(front.progress, 100),
        5
    )

    return {
        "front": front,

        # Regulación
        "state": state,
        "label": regulation["label"],
        "reason": regulation["reason"],
        "pressure": regulation["pressure"],
        "requires_action": regulation[
            "requires_action"
        ],

        # Visual
        "color": config["color"],
        "background": config["background"],

        # Fechas
        "deadline_text": (
            full_date(front.deadline)
            if front.deadline
            else "Sin fecha límite"
        ),

        "deadline_short": short_date(
            front.deadline
        ),

        "review_text": (
            full_date(front.next_review)
            if front.next_review
            else "Sin revisión"
        ),

        "review_short": short_date(
            front.next_review
        ),

        # Carga
        "hours_text": hours_text,
        "session_text": session_text,

        # Horizonte
        "visual_progress": visual_progress,
    }


def prepare_fronts(
    today: date
) -> List[Dict[str, Any]]:
    """
    Carga y regula todos los frentes.
    """

    fronts = load_fronts()

    return [
        present_front(front, today)
        for front in fronts
    ]


# ============================================================
# HOY
# ============================================================

@app.get(
    "/",
    response_class=HTMLResponse
)
def home(request: Request):

    today = TEST_TODAY

    items = prepare_fronts(today)

    # --------------------------------------------------------
    # Sólo aquello que merece movimiento
    # --------------------------------------------------------

    attention_fronts = [
        item
        for item in items
        if item["requires_action"]
    ]

    # --------------------------------------------------------
    # Todo lo demás queda cognitivamente cerrado
    # --------------------------------------------------------

    controlled_fronts = [
        item
        for item in items
        if not item["requires_action"]
    ]

    # --------------------------------------------------------
    # Mayor presión primero
    # --------------------------------------------------------

    attention_fronts.sort(
        key=lambda item: item["pressure"],
        reverse=True
    )

    return templates.TemplateResponse(
        request=request,
        name="hoy.html",
        context={
            "date_text": long_date(today),

            "attention_fronts":
                attention_fronts,

            "controlled_fronts":
                controlled_fronts,

            "attention_count":
                len(attention_fronts),

            "controlled_count":
                len(controlled_fronts),
        },
    )


# ============================================================
# HORIZONTE
# ============================================================

@app.get(
    "/horizonte",
    response_class=HTMLResponse
)
def horizonte(request: Request):

    today = TEST_TODAY

    items = prepare_fronts(today)

    # --------------------------------------------------------
    # Orden temporal:
    #
    # 1. deadline próximo
    # 2. frentes sin deadline
    # --------------------------------------------------------

    items.sort(
        key=lambda item: (
            item["front"].deadline is None,
            item["front"].deadline or date.max
        )
    )

    return templates.TemplateResponse(
        request=request,
        name="horizonte.html",
        context={
            "date_text": long_date(today),
            "fronts": items,
        },
    )


# ============================================================
# FRENTES
# ============================================================

@app.get(
    "/frentes",
    response_class=HTMLResponse
)
def frentes(request: Request):

    today = TEST_TODAY

    items = prepare_fronts(today)

    # --------------------------------------------------------
    # Agrupación conceptual.
    #
    # Esto no depende del color solamente.
    # Diferenciamos:
    #
    # - merece atención
    # - activo pero tranquilo
    # - esperando
    # - dormido
    # - cerrado
    # --------------------------------------------------------

    attention = []
    active = []
    waiting = []
    sleeping = []
    closed = []

    for item in items:

        front = item["front"]

        if front.status == "closed":
            closed.append(item)

        elif front.status == "sleeping":
            sleeping.append(item)

        elif front.status == "waiting":
            waiting.append(item)

        elif item["requires_action"]:
            attention.append(item)

        else:
            active.append(item)

    # --------------------------------------------------------
    # Los frentes que requieren atención se ordenan
    # por presión.
    # --------------------------------------------------------

    attention.sort(
        key=lambda item: item["pressure"],
        reverse=True
    )

    # --------------------------------------------------------
    # Los activos tranquilos se ordenan por importancia.
    # --------------------------------------------------------

    active.sort(
        key=lambda item: item["front"].importance,
        reverse=True
    )

    # --------------------------------------------------------
    # Sólo enviamos grupos que contienen algo.
    # --------------------------------------------------------

    groups = []

    if attention:
        groups.append({
            "title": "Merecen atención",
            "items": attention,
        })

    if active:
        groups.append({
            "title": "En curso",
            "items": active,
        })

    if waiting:
        groups.append({
            "title": "En espera",
            "items": waiting,
        })

    if sleeping:
        groups.append({
            "title": "Dormidos",
            "items": sleeping,
        })

    if closed:
        groups.append({
            "title": "Cerrados",
            "items": closed,
        })

    return templates.TemplateResponse(
        request=request,
        name="frentes.html",
        context={
            "groups": groups,
            "total_fronts": len(items),
        },
    )


# ============================================================
# HEALTH
# ============================================================

@app.get("/health")
def health():

    fronts = load_fronts()

    return {
        "status": "ok",
        "app": "organa",
        "version": "0.5.0",
        "fronts": len(fronts),
        "regulator": "active",
        "templates": "active",
    }
