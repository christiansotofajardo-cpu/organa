from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(
    title="Organa",
    description="Human-centered workload and attention regulation system.",
    version="0.2.0",
)


@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Organa</title>

<style>
* { box-sizing: border-box; }

body {
    margin: 0;
    font-family: Inter, Arial, Helvetica, sans-serif;
    background: #f6f8fc;
    color: #10213f;
}

.container {
    max-width: 1120px;
    margin: auto;
    padding: 30px 30px 70px;
}

/* HEADER */

header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 55px;
}

.brand {
    font-size: 23px;
    font-weight: 750;
    color: #173a75;
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

/* INTRO */

h1 {
    font-size: 40px;
    margin: 0 0 5px;
}

.date {
    color: #667085;
    font-size: 17px;
}

.control {
    margin-top: 27px;
    background: #edf8f0;
    padding: 22px 27px;
    border-radius: 17px;
}

.control strong {
    display: block;
    color: #24734b;
    font-size: 20px;
    margin-bottom: 5px;
}

/* WEEK */

.section-title {
    margin: 38px 0 15px;
    font-size: 19px;
}

.week {
    display: grid;
    grid-template-columns: repeat(7,1fr);
    gap: 9px;
}

.day {
    background: white;
    border-radius: 14px;
    padding: 15px 10px;
    min-height: 105px;
    text-align: center;
    box-shadow: 0 2px 10px rgba(20,40,80,.04);
}

.day.today {
    outline: 2px solid #173a75;
}

.day-name {
    color: #667085;
    font-size: 13px;
    font-weight: 700;
}

.day-number {
    font-size: 22px;
    font-weight: 750;
    margin: 4px 0 10px;
}

.load {
    display: inline-block;
    padding: 5px 8px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 700;
}

.red    { background:#fdecec; color:#b42318; }
.orange { background:#fff0df; color:#b54708; }
.yellow { background:#fff8d8; color:#8a6500; }
.green  { background:#eaf7ef; color:#23734a; }
.blue   { background:#eaf2ff; color:#175cd3; }

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
    padding: 19px 22px;
    display: grid;
    grid-template-columns: 12px 1fr auto auto 22px;
    align-items: center;
    gap: 14px;
}

.front summary::-webkit-details-marker {
    display: none;
}

.dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
}

.dot-red { background:#d92d20; }
.dot-yellow { background:#eaaa08; }
.dot-green { background:#32a060; }
.dot-blue { background:#2e70d1; }

.front-title {
    font-weight: 750;
    font-size: 16px;
}

.reason {
    color: #667085;
    font-size: 13px;
    margin-top: 3px;
}

.time {
    color: #344054;
    font-size: 13px;
    font-weight: 650;
}

.badge {
    padding: 6px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 750;
}

.arrow {
    font-size: 18px;
    transition: transform .2s;
}

details[open] .arrow {
    transform: rotate(180deg);
}

.front-detail {
    border-top: 1px solid #eef1f5;
    padding: 18px 22px 22px 48px;
    display: grid;
    grid-template-columns: 2fr 1fr 1fr;
    gap: 25px;
}

.label {
    color: #98a2b3;
    text-transform: uppercase;
    font-size: 10px;
    font-weight: 750;
    letter-spacing: .6px;
    margin-bottom: 5px;
}

.value {
    font-size: 14px;
    line-height: 1.4;
}

/* CLOSURE */

.covered {
    margin-top: 30px;
    background: #edf4ff;
    border-radius: 16px;
    padding: 20px 24px;
    color: #1849a9;
}

.covered strong {
    display: block;
    font-size: 17px;
    margin-bottom: 4px;
}

.footer {
    margin-top: 45px;
    color: #667085;
    font-style: italic;
    font-size: 14px;
}

@media(max-width:760px) {
    header {
        align-items:flex-start;
        gap:20px;
        flex-direction:column;
    }

    .week {
        grid-template-columns: repeat(4,1fr);
    }

    .front summary {
        grid-template-columns: 12px 1fr 22px;
    }

    .time, .badge {
        display:none;
    }

    .front-detail {
        grid-template-columns:1fr;
    }
}
</style>
</head>

<body>
<div class="container">

<header>
    <div class="brand">◇ Organa</div>
    <nav>
        <a class="active" href="#">Hoy</a>
        <a href="#">Horizonte</a>
        <a href="#">Frentes</a>
    </nav>
</header>

<h1>Buen día, Christian</h1>
<div class="date">19 de septiembre de 2026</div>

<div class="control">
    <strong>Tu carga está bajo control.</strong>
    Hay 3 frentes que merecen atención.
    El resto permanece vigilado por Organa.
</div>

<h2 class="section-title">Esta semana</h2>

<div class="week">

    <div class="day today">
        <div class="day-name">SÁB</div>
        <div class="day-number">19</div>
        <span class="load yellow">Avance</span>
    </div>

    <div class="day">
        <div class="day-name">DOM</div>
        <div class="day-number">20</div>
        <span class="load blue">Sin presión</span>
    </div>

    <div class="day">
        <div class="day-name">LUN</div>
        <div class="day-number">21</div>
        <span class="load orange">Atención</span>
    </div>

    <div class="day">
        <div class="day-name">MAR</div>
        <div class="day-number">22</div>
        <span class="load yellow">Avance</span>
    </div>

    <div class="day">
        <div class="day-name">MIÉ</div>
        <div class="day-number">23</div>
        <span class="load green">Equilibrado</span>
    </div>

    <div class="day">
        <div class="day-name">JUE</div>
        <div class="day-number">24</div>
        <span class="load yellow">Avance</span>
    </div>

    <div class="day">
        <div class="day-name">VIE</div>
        <div class="day-number">25</div>
        <span class="load blue">Sin presión</span>
    </div>

</div>

<div class="focus-header">
    <h2>Dónde poner energía</h2>
    <span>Sólo lo que merece estar abierto ahora</span>
</div>


<details class="front">
    <summary>
        <span class="dot dot-red"></span>

        <div>
            <div class="front-title">UNGM · Visualization</div>
            <div class="reason">Plazo próximo y trabajo relevante pendiente.</div>
        </div>

        <div class="time">≈ 2 h</div>
        <span class="badge red">ATENDER</span>
        <span class="arrow">⌄</span>
    </summary>

    <div class="front-detail">
        <div>
            <div class="label">Próxima acción</div>
            <div class="value">
                Avanzar en la estructura de la propuesta técnica.
            </div>
        </div>

        <div>
            <div class="label">Hito</div>
            <div class="value">Postulación</div>
        </div>

        <div>
            <div class="label">Por qué ahora</div>
            <div class="value">Evitar concentración de carga al acercarse el cierre.</div>
        </div>
    </div>
</details>


<details class="front">
    <summary>
        <span class="dot dot-yellow"></span>

        <div>
            <div class="front-title">Paper · Evalia</div>
            <div class="reason">No es urgente; conviene mantener continuidad.</div>
        </div>

        <div class="time">≈ 1 h</div>
        <span class="badge yellow">AVANZAR</span>
        <span class="arrow">⌄</span>
    </summary>

    <div class="front-detail">
        <div>
            <div class="label">Próxima acción</div>
            <div class="value">
                Retomar estructura y definir siguiente bloque de trabajo.
            </div>
        </div>

        <div>
            <div class="label">Ritmo</div>
            <div class="value">Continuidad semanal</div>
        </div>

        <div>
            <div class="label">Por qué ahora</div>
            <div class="value">
                Un avance pequeño evita convertirlo posteriormente en urgencia.
            </div>
        </div>
    </div>
</details>


<details class="front">
    <summary>
        <span class="dot dot-green"></span>

        <div>
            <div class="front-title">Tesis · Parvularia</div>
            <div class="reason">Trayectoria adecuada.</div>
        </div>

        <div class="time">≈ 30 min</div>
        <span class="badge green">MANTENER</span>
        <span class="arrow">⌄</span>
    </summary>

    <div class="front-detail">
        <div>
            <div class="label">Próxima acción</div>
            <div class="value">
                Continuar procesamiento cuando corresponda al próximo bloque.
            </div>
        </div>

        <div>
            <div class="label">Estado</div>
            <div class="value">En curso</div>
        </div>

        <div>
            <div class="label">Necesidad actual</div>
            <div class="value">
                No requiere aumentar su carga.
            </div>
        </div>
    </div>
</details>


<div class="covered">
    <strong>18 frentes permanecen bajo control.</strong>
    No requieren tu atención ahora. Organa los mantiene vigilados
    y los volverá a abrir cuando corresponda.
</div>

<div class="footer">
    No necesitas mantener todo en la cabeza.
</div>

</div>
</body>
</html>
"""


@app.get("/health")
def health():
    return {
        "status": "ok",
        "app": "organa",
        "version": "0.2.0"
    }
