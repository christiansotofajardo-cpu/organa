import json
from datetime import date
from pathlib import Path
from typing import List

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from models import Front
from regulator import determine_attention


app = FastAPI(
    title="Organa",
    description="Human-centered workload and attention regulation system.",
    version="0.3.0",
)


# ============================================================
# DATA
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
FRONTS_FILE = BASE_DIR / "data" / "fronts.json"


def load_fronts() -> List[Front]:
    """
    Lee los frentes desde fronts.json y los convierte
    en objetos Front validados por Pydantic.
    """
    with open(FRONTS_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    return [Front(**item) for item in data]


# ============================================================
# VISUAL HELPERS
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


def front_card(front: Front, today: date) -> str:
    """
    Construye visualmente un frente a partir del resultado
    producido por Regulator.
    """

    regulation = determine_attention(front, today)

    state = regulation["state"]
    label = regulation["label"]
    reason = regulation["reason"]
    pressure = regulation["pressure"]

    config = STATE_CONFIG[state]

    steps_html = ""

    for step in front.steps:
        symbol = "✓" if step.completed else "○"
        opacity = "0.55" if step.completed else "1"

        steps_html += f"""
        <div class="step" style="opacity:{opacity}">
            <span>{symbol}</span>
            <span>{step.title}</span>
        </div>
        """

    if not steps_html:
        steps_html = """
        <div class="muted">
            No hay pasos definidos todavía.
        </div>
        """

    deadline = (
        front.deadline.strftime("%d/%m/%Y")
        if front.deadline
        else "Sin fecha límite"
    )

    remaining_hours = (
        f"{front.estimated_hours_remaining:g} h"
        if front.estimated_hours_remaining is not None
        else "Por estimar"
    )

    session = (
        f"{front.suggested_session_minutes} min"
        if front.suggested_session_minutes
        else "Flexible"
    )

    next_action = front.next_action or "Sin próxima acción definida."

    return f"""
    <details class="front">

        <summary>

            <span
                class="dot"
                style="background:{config['color']}"
            ></span>

            <div class="front-main">
                <div class="front-title">{front.name}</div>
                <div class="front-reason">{reason}</div>
            </div>

            <div class="area">{front.area}</div>

            <span
                class="badge"
                style="
                    color:{config['color']};
                    background:{config['background']};
                "
            >
                {label.upper()}
            </span>

            <span class="arrow">⌄</span>

        </summary>


        <div class="detail">

            <div class="action-box">

                <div class="eyebrow">
                    PRÓXIMA ACCIÓN
                </div>

                <div class="next-action">
                    {next_action}
                </div>

                <div class="steps">
                    {steps_html}
                </div>

            </div>


            <div class="facts">

                <div class="fact">
                    <span>Hito / deadline</span>
                    <strong>{deadline}</strong>
                </div>

                <div class="fact">
                    <span>Trabajo restante</span>
                    <strong>{remaining_hours}</strong>
                </div>

                <div class="fact">
                    <span>Sesión sugerida</span>
                    <strong>{session}</strong>
                </div>

                <div class="fact">
                    <span>Avance</span>
                    <strong>{front.progress}%</strong>
                </div>

                <div class="fact">
                    <span>Presión actual</span>
                    <strong>{pressure}/100</strong>
                </div>

            </div>

        </div>

    </details>
    """


# ============================================================
# HOME
# ============================================================

@app.get("/", response_class=HTMLResponse)
def home():

    # Fecha fija durante esta fase de prueba.
    # Después usaremos automáticamente la fecha actual.
    today = date(2026, 9, 19)

    fronts = load_fronts()

    regulated = [
        (front, determine_attention(front, today))
        for front in fronts
    ]

    # --------------------------------------------------------
    # Separar aquello que merece atención de aquello que
    # Organa puede mantener cognitivamente cerrado.
    # --------------------------------------------------------

    attention_fronts = [
        (front, result)
        for front, result in regulated
        if result["requires_action"]
    ]

    controlled_fronts = [
        (front, result)
        for front, result in regulated
        if not result["requires_action"]
    ]

    # Mayor presión primero.
    attention_fronts.sort(
        key=lambda item: item[1]["pressure"],
        reverse=True
    )

    cards = "".join(
        front_card(front, today)
        for front, _ in attention_fronts
    )

    if not cards:
        cards = """
        <div class="empty">
            No hay frentes que necesiten movimiento ahora.
        </div>
        """

    attention_count = len(attention_fronts)
    controlled_count = len(controlled_fronts)

    # --------------------------------------------------------
    # HTML
    # --------------------------------------------------------

    html = f"""
<!DOCTYPE html>
<html lang="es">

<head>

<meta charset="UTF-8">
<meta
    name="viewport"
    content="width=device-width, initial-scale=1.0"
>

<title>Organa</title>

<style>

* {{
    box-sizing: border-box;
}}

body {{
    margin: 0;
    font-family:
        Inter,
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        sans-serif;

    background: #f6f8fc;
    color: #10213f;
}}

.container {{
    max-width: 1120px;
    margin: auto;
    padding: 32px 30px 70px;
}}


/* HEADER */

header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 55px;
}}

.brand {{
    color: #173a75;
    font-size: 23px;
    font-weight: 750;
}}

nav {{
    display: flex;
    gap: 8px;
}}

nav a {{
    text-decoration: none;
    color: #667085;
    font-weight: 600;
    padding: 9px 15px;
    border-radius: 10px;
}}

nav a.active {{
    background: white;
    color: #173a75;
    box-shadow: 0 2px 10px rgba(20,40,80,.06);
}}


/* INTRO */

h1 {{
    margin: 0 0 6px;
    font-size: 40px;
}}

.date {{
    color: #667085;
    font-size: 17px;
}}

.control {{
    margin-top: 27px;
    padding: 23px 27px;

    background: #edf8f0;
    border-radius: 17px;
}}

.control strong {{
    display: block;

    color: #24734b;
    font-size: 20px;

    margin-bottom: 5px;
}}


/* SUMMARY */

.summary {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;

    margin-top: 20px;
}}

.summary-card {{
    background: white;
    padding: 20px 22px;
    border-radius: 15px;

    box-shadow:
        0 2px 10px rgba(20,40,80,.04);
}}

.summary-number {{
    font-size: 30px;
    font-weight: 750;
}}

.summary-label {{
    margin-top: 3px;
    color: #667085;
    font-size: 13px;
}}


/* FOCUS */

.focus-header {{
    display: flex;
    justify-content: space-between;
    align-items: end;

    margin-top: 42px;
    margin-bottom: 14px;
}}

.focus-header h2 {{
    margin: 0;
    font-size: 22px;
}}

.focus-header span {{
    color: #667085;
    font-size: 14px;
}}


/* FRONT */

.front {{
    background: white;
    border-radius: 16px;

    margin-bottom: 11px;

    box-shadow:
        0 2px 12px rgba(20,40,80,.05);

    overflow: hidden;
}}

.front summary {{
    list-style: none;
    cursor: pointer;

    display: grid;
    grid-template-columns:
        12px
        1fr
        auto
        auto
        22px;

    align-items: center;
    gap: 14px;

    padding: 19px 22px;
}}

.front summary::-webkit-details-marker {{
    display: none;
}}

.dot {{
    width: 10px;
    height: 10px;
    border-radius: 50%;
}}

.front-title {{
    font-size: 16px;
    font-weight: 750;
}}

.front-reason {{
    color: #667085;
    font-size: 13px;
    margin-top: 4px;
}}

.area {{
    color: #667085;
    font-size: 12px;
}}

.badge {{
    padding: 6px 10px;
    border-radius: 20px;

    font-size: 10px;
    font-weight: 750;
}}

.arrow {{
    font-size: 18px;
    transition: transform .2s;
}}

details[open] .arrow {{
    transform: rotate(180deg);
}}


/* DETAIL */

.detail {{
    border-top: 1px solid #eef1f5;

    display: grid;
    grid-template-columns: 1.7fr 1fr;
    gap: 35px;

    padding: 22px 48px 28px;
}}

.eyebrow {{
    color: #98a2b3;
    font-size: 10px;
    font-weight: 750;

    letter-spacing: .7px;

    margin-bottom: 7px;
}}

.next-action {{
    font-size: 16px;
    font-weight: 700;

    margin-bottom: 17px;
}}

.steps {{
    display: flex;
    flex-direction: column;
    gap: 8px;
}}

.step {{
    display: flex;
    gap: 9px;

    font-size: 13px;
    color: #475467;
}}

.facts {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 13px;
}}

.fact {{
    background: #f8fafc;

    padding: 12px 14px;
    border-radius: 11px;
}}

.fact span {{
    display: block;

    color: #98a2b3;
    font-size: 10px;

    margin-bottom: 4px;
}}

.fact strong {{
    font-size: 13px;
}}

.muted {{
    color: #98a2b3;
    font-size: 13px;
}}


/* CONTROLLED */

.covered {{
    margin-top: 30px;

    background: #edf4ff;
    color: #1849a9;

    border-radius: 16px;
    padding: 20px 24px;
}}

.covered strong {{
    display: block;

    font-size: 17px;
    margin-bottom: 4px;
}}

.empty {{
    background: #edf4ff;
    color: #1849a9;

    padding: 25px;
    border-radius: 16px;
}}


/* FOOTER */

.footer {{
    margin-top: 45px;

    color: #667085;
    font-style: italic;
    font-size: 14px;
}}


@media(max-width:760px) {{

    header {{
        align-items: flex-start;
        gap: 20px;
        flex-direction: column;
    }}

    .summary {{
        grid-template-columns: 1fr;
    }}

    .front summary {{
        grid-template-columns:
            12px
            1fr
            22px;
    }}

    .area,
    .badge {{
        display: none;
    }}

    .detail {{
        grid-template-columns: 1fr;
        padding: 20px 25px;
    }}

}}

</style>

</head>


<body>

<div class="container">


<header>

    <div class="brand">
        ◇ Organa
    </div>

    <nav>
        <a class="active" href="/">Hoy</a>
        <a href="#">Horizonte</a>
        <a href="#">Frentes</a>
    </nav>

</header>


<h1>Buen día, Christian</h1>

<div class="date">
    19 de septiembre de 2026
</div>


<div class="control">

    <strong>
        Tu carga está bajo control.
    </strong>

    Organa distingue entre lo que merece movimiento
    y aquello que puede permanecer fuera de tu atención.

</div>


<div class="summary">

    <div class="summary-card">

        <div
            class="summary-number"
            style="color:#b54708"
        >
            {attention_count}
        </div>

        <div class="summary-label">
            frentes sugieren movimiento
        </div>

    </div>


    <div class="summary-card">

        <div
            class="summary-number"
            style="color:#175cd3"
        >
            {controlled_count}
        </div>

        <div class="summary-label">
            frentes pueden permanecer cerrados
        </div>

    </div>

</div>


<div class="focus-header">

    <h2>
        Dónde poner energía
    </h2>

    <span>
        Sólo lo que merece estar abierto ahora
    </span>

</div>


{cards}


<div class="covered">

    <strong>
        {controlled_count} frentes permanecen bajo control.
    </strong>

    No requieren tu atención ahora.
    Organa los mantiene vigilados
    y los volverá a abrir cuando corresponda.

</div>


<div class="footer">
    No necesitas mantener todo en la cabeza.
</div>


</div>

</body>
</html>
"""

    return HTMLResponse(content=html)


# ============================================================
# HEALTH
# ============================================================

@app.get("/health")
def health():

    fronts = load_fronts()

    return {{
        "status": "ok",
        "app": "organa",
        "version": "0.3.0",
        "fronts": len(fronts)
    }}
