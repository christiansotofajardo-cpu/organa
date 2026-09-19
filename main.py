import json
from datetime import date
from pathlib import Path
from typing import List

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from models import Front
from regulator import determine_attention


# ============================================================
# ORGANA
# ============================================================

app = FastAPI(
    title="Organa",
    description="Human-centered workload and attention regulation system.",
    version="0.4.0",
)


# ============================================================
# DATA
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
FRONTS_FILE = BASE_DIR / "data" / "fronts.json"

# Fecha fija sólo durante esta etapa de calibración.
# Más adelante será date.today().
TEST_TODAY = date(2026, 9, 19)


def load_fronts() -> List[Front]:
    with open(FRONTS_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    return [Front(**item) for item in data]


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
# SHARED STYLES
# ============================================================

SHARED_STYLE = """
<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family:
        Inter,
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        sans-serif;

    background: #f6f8fc;
    color: #10213f;
}

.container {
    max-width: 1160px;
    margin: auto;
    padding: 32px 30px 70px;
}


/* HEADER */

header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 55px;
}

.brand {
    color: #173a75;
    font-size: 23px;
    font-weight: 750;
}

nav {
    display: flex;
    gap: 8px;
}

nav a {
    text-decoration: none;
    color: #667085;
    font-weight: 600;
    padding: 9px 15px;
    border-radius: 10px;
}

nav a.active {
    background: white;
    color: #173a75;
    box-shadow: 0 2px 10px rgba(20,40,80,.06);
}


/* GENERAL */

h1 {
    margin: 0 0 6px;
    font-size: 40px;
}

.subtitle {
    color: #667085;
    font-size: 16px;
    line-height: 1.5;
}

.control {
    margin-top: 27px;
    padding: 23px 27px;
    background: #edf8f0;
    border-radius: 17px;
}

.control strong {
    display: block;
    color: #24734b;
    font-size: 20px;
    margin-bottom: 5px;
}

.summary {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
    margin-top: 20px;
}

.summary-card {
    background: white;
    padding: 20px 22px;
    border-radius: 15px;
    box-shadow: 0 2px 10px rgba(20,40,80,.04);
}

.summary-number {
    font-size: 30px;
    font-weight: 750;
}

.summary-label {
    margin-top: 3px;
    color: #667085;
    font-size: 13px;
}


/* FOCUS */

.focus-header {
    display: flex;
    justify-content: space-between;
    align-items: end;
    margin-top: 42px;
    margin-bottom: 14px;
}

.focus-header h2 {
    margin: 0;
    font-size: 22px;
}

.focus-header span {
    color: #667085;
    font-size: 14px;
}


/* FRONT CARDS */

.front {
    background: white;
    border-radius: 16px;
    margin-bottom: 11px;
    box-shadow: 0 2px 12px rgba(20,40,80,.05);
    overflow: hidden;
}

.front summary {
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
}

.front summary::-webkit-details-marker {
    display: none;
}

.dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
}

.front-title {
    font-size: 16px;
    font-weight: 750;
}

.front-reason {
    color: #667085;
    font-size: 13px;
    margin-top: 4px;
}

.area {
    color: #667085;
    font-size: 12px;
}

.badge {
    padding: 6px 10px;
    border-radius: 20px;
    font-size: 10px;
    font-weight: 750;
}

.arrow {
    font-size: 18px;
    transition: transform .2s;
}

details[open] .arrow {
    transform: rotate(180deg);
}


/* FRONT DETAIL */

.detail {
    border-top: 1px solid #eef1f5;

    display: grid;
    grid-template-columns: 1.7fr 1fr;
    gap: 35px;

    padding: 22px 48px 28px;
}

.eyebrow {
    color: #98a2b3;
    font-size: 10px;
    font-weight: 750;
    letter-spacing: .7px;
    margin-bottom: 7px;
}

.next-action {
    font-size: 16px;
    font-weight: 700;
    margin-bottom: 17px;
}

.steps {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.step {
    display: flex;
    gap: 9px;
    font-size: 13px;
    color: #475467;
}

.facts {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 13px;
}

.fact {
    background: #f8fafc;
    padding: 12px 14px;
    border-radius: 11px;
}

.fact span {
    display: block;
    color: #98a2b3;
    font-size: 10px;
    margin-bottom: 4px;
}

.fact strong {
    font-size: 13px;
}


/* CONTROLLED */

.covered {
    margin-top: 30px;
    background: #edf4ff;
    color: #1849a9;
    border-radius: 16px;
    padding: 20px 24px;
}

.covered strong {
    display: block;
    font-size: 17px;
    margin-bottom: 4px;
}

.empty {
    background: #edf4ff;
    color: #1849a9;
    padding: 25px;
    border-radius: 16px;
}


/* HORIZON */

.time-selector {
    display: flex;
    gap: 8px;
    margin-top: 28px;
    margin-bottom: 28px;
}

.time-selector span {
    background: white;
    color: #667085;
    font-weight: 650;
    font-size: 13px;
    padding: 9px 15px;
    border-radius: 20px;
}

.time-selector span.active {
    background: #173a75;
    color: white;
}

.future {
    background: #fff8e8;
    padding: 20px 24px;
    border-radius: 16px;
    margin-bottom: 28px;
}

.future strong {
    display: block;
    color: #8a6500;
    font-size: 17px;
    margin-bottom: 5px;
}

.future span {
    color: #667085;
    font-size: 14px;
}

.horizon {
    display: flex;
    flex-direction: column;
    gap: 9px;
}

.horizon-row {
    display: grid;

    grid-template-columns:
        1.45fr
        1.7fr
        .55fr
        .65fr
        .7fr
        .65fr;

    gap: 18px;
    align-items: center;

    background: white;
    padding: 17px 20px;
    border-radius: 14px;

    box-shadow: 0 2px 10px rgba(20,40,80,.04);
}

.horizon-name {
    display: flex;
    align-items: center;
    gap: 12px;
}

.horizon-name strong {
    display: block;
    font-size: 14px;
}

.horizon-name span {
    display: block;
    color: #98a2b3;
    font-size: 11px;
    margin-top: 3px;
}

.trajectory {
    height: 9px;
    background: #eef1f5;
    border-radius: 20px;
    overflow: hidden;
}

.trajectory-bar {
    height: 100%;
    border-radius: 20px;
}

.mini span {
    display: block;
    color: #98a2b3;
    font-size: 9px;
    margin-bottom: 3px;
}

.mini strong {
    font-size: 12px;
}


/* LEGEND */

.legend {
    display: flex;
    flex-wrap: wrap;
    gap: 18px;
    margin-top: 27px;
    color: #667085;
    font-size: 12px;
}

.legend-item {
    display: flex;
    align-items: center;
    gap: 6px;
}

.legend-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
}


/* FOOTER */

.footer {
    margin-top: 45px;
    color: #667085;
    font-style: italic;
    font-size: 14px;
}


/* MOBILE */

@media(max-width:850px) {

    header {
        flex-direction: column;
        align-items: flex-start;
        gap: 20px;
    }

    .summary {
        grid-template-columns: 1fr;
    }

    .front summary {
        grid-template-columns:
            12px
            1fr
            22px;
    }

    .area,
    .badge {
        display: none;
    }

    .detail {
        grid-template-columns: 1fr;
        padding: 20px 25px;
    }

    .horizon-row {
        grid-template-columns: 1fr;
        gap: 10px;
    }
}

</style>
"""


# ============================================================
# SHARED HEADER
# ============================================================

def header_html(active: str) -> str:

    hoy_class = "active" if active == "hoy" else ""
    horizonte_class = "active" if active == "horizonte" else ""
    frentes_class = "active" if active == "frentes" else ""

    return f"""
    <header>

        <div class="brand">
            ◇ Organa
        </div>

        <nav>
            <a class="{hoy_class}" href="/">Hoy</a>

            <a
                class="{horizonte_class}"
                href="/horizonte"
            >
                Horizonte
            </a>

            <a
                class="{frentes_class}"
                href="#"
            >
                Frentes
            </a>
        </nav>

    </header>
    """


# ============================================================
# FRONT CARD
# ============================================================

def front_card(front: Front, today: date) -> str:

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
        <div
            class="step"
            style="opacity:{opacity}"
        >
            <span>{symbol}</span>
            <span>{step.title}</span>
        </div>
        """

    if not steps_html:
        steps_html = """
        <div style="color:#98a2b3;font-size:13px;">
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

    next_action = (
        front.next_action
        or "Sin próxima acción definida."
    )

    return f"""
    <details class="front">

        <summary>

            <span
                class="dot"
                style="background:{config['color']}"
            ></span>

            <div>

                <div class="front-title">
                    {front.name}
                </div>

                <div class="front-reason">
                    {reason}
                </div>

            </div>

            <div class="area">
                {front.area}
            </div>

            <span
                class="badge"
                style="
                    color:{config['color']};
                    background:{config['background']};
                "
            >
                {label.upper()}
            </span>

            <span class="arrow">
                ⌄
            </span>

        </summary>


        <div class="detail">

            <div>

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
# HOY
# ============================================================

@app.get("/", response_class=HTMLResponse)
def home():

    today = TEST_TODAY

    fronts = load_fronts()

    regulated = [
        (front, determine_attention(front, today))
        for front in fronts
    ]

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

    html = f"""
<!DOCTYPE html>

<html lang="es">

<head>

<meta charset="UTF-8">

<meta
    name="viewport"
    content="width=device-width, initial-scale=1.0"
>

<title>Organa · Hoy</title>

{SHARED_STYLE}

</head>


<body>

<div class="container">

{header_html("hoy")}


<h1>
    Buen día, Christian
</h1>

<div class="subtitle">
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
# HORIZONTE
# ============================================================

@app.get("/horizonte", response_class=HTMLResponse)
def horizonte():

    today = TEST_TODAY

    fronts = load_fronts()

    regulated = [
        (front, determine_attention(front, today))
        for front in fronts
    ]

    # Primero los que tienen deadline.
    # Después los que no tienen fecha.
    regulated.sort(
        key=lambda item: (
            item[0].deadline is None,
            item[0].deadline or date.max
        )
    )

    rows = ""

    for front, result in regulated:

        state = result["state"]
        config = STATE_CONFIG[state]

        deadline = (
            front.deadline.strftime("%d/%m")
            if front.deadline
            else "—"
        )

        review = (
            front.next_review.strftime("%d/%m")
            if front.next_review
            else "—"
        )

        hours = (
            f"{front.estimated_hours_remaining:g} h"
            if front.estimated_hours_remaining is not None
            else "—"
        )

        rows += f"""
        <div class="horizon-row">

            <div class="horizon-name">

                <span
                    class="dot"
                    style="background:{config['color']}"
                ></span>

                <div>

                    <strong>
                        {front.name}
                    </strong>

                    <span>
                        {front.area}
                    </span>

                </div>

            </div>


            <div class="trajectory">

                <div
                    class="trajectory-bar"
                    style="
                        width:{max(front.progress, 5)}%;
                        background:{config['color']};
                    "
                ></div>

            </div>


            <div class="mini">

                <span>
                    AVANCE
                </span>

                <strong>
                    {front.progress}%
                </strong>

            </div>


            <div class="mini">

                <span>
                    PENDIENTE
                </span>

                <strong>
                    {hours}
                </strong>

            </div>


            <div class="mini">

                <span>
                    DEADLINE
                </span>

                <strong>
                    {deadline}
                </strong>

            </div>


            <div class="mini">

                <span>
                    REVISAR
                </span>

                <strong>
                    {review}
                </strong>

            </div>

        </div>
        """


    html = f"""
<!DOCTYPE html>

<html lang="es">

<head>

<meta charset="UTF-8">

<meta
    name="viewport"
    content="width=device-width, initial-scale=1.0"
>

<title>Organa · Horizonte</title>

{SHARED_STYLE}

</head>


<body>

<div class="container">

{header_html("horizonte")}


<h1>
    Horizonte
</h1>

<div class="subtitle">

    Mira lo que viene sin convertir todo el futuro
    en una preocupación presente.

</div>


<div class="time-selector">

    <span class="active">
        4 semanas
    </span>

    <span>
        3 meses
    </span>

    <span>
        6 meses
    </span>

</div>


<div class="future">

    <strong>
        Organa vigila la carga futura.
    </strong>

    <span>

        Los frentes pueden permanecer tranquilos mientras
        su trayectoria siga siendo compatible con sus plazos
        y trabajo pendiente.

    </span>

</div>


<div class="horizon">

    {rows}

</div>


<div class="legend">

    <div class="legend-item">

        <span
            class="legend-dot"
            style="background:#d92d20"
        ></span>

        Requiere atención

    </div>


    <div class="legend-item">

        <span
            class="legend-dot"
            style="background:#b54708"
        ></span>

        Atención próxima

    </div>


    <div class="legend-item">

        <span
            class="legend-dot"
            style="background:#eaaa08"
        ></span>

        Conviene avanzar

    </div>


    <div class="legend-item">

        <span
            class="legend-dot"
            style="background:#32a060"
        ></span>

        Trayectoria adecuada

    </div>


    <div class="legend-item">

        <span
            class="legend-dot"
            style="background:#2e70d1"
        ></span>

        Bajo control

    </div>

</div>


<div class="footer">
    Ver el futuro no significa cargarlo hoy.
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

    return {
        "status": "ok",
        "app": "organa",
        "version": "0.4.0",
        "fronts": len(fronts)
    }
