from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(
    title="Organa",
    description="Human-centered workload and attention regulation system.",
    version="0.1.0",
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
            body {
                margin: 0;
                font-family: Arial, Helvetica, sans-serif;
                background: #f7f9fc;
                color: #17233c;
            }

            .container {
                max-width: 1000px;
                margin: 0 auto;
                padding: 60px 30px;
            }

            .brand {
                font-size: 22px;
                font-weight: 700;
                color: #173a75;
                margin-bottom: 70px;
            }

            h1 {
                font-size: 44px;
                margin-bottom: 8px;
            }

            .date {
                color: #667085;
                font-size: 18px;
            }

            .message {
                margin-top: 35px;
                padding: 28px;
                background: #eef8f1;
                border-radius: 18px;
            }

            .message h2 {
                color: #24734b;
                margin-top: 0;
            }

            .summary {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 18px;
                margin-top: 28px;
            }

            .card {
                background: white;
                padding: 24px;
                border-radius: 16px;
                box-shadow: 0 3px 14px rgba(20, 40, 80, 0.06);
            }

            .number {
                font-size: 36px;
                font-weight: 700;
                margin-bottom: 6px;
            }

            .attention {
                color: #b42318;
            }

            .advance {
                color: #b26a00;
            }

            .controlled {
                color: #175cd3;
            }

            .footer {
                margin-top: 70px;
                color: #667085;
                font-style: italic;
            }

            @media (max-width: 700px) {
                .summary {
                    grid-template-columns: 1fr;
                }

                h1 {
                    font-size: 34px;
                }
            }
        </style>
    </head>

    <body>
        <div class="container">

            <div class="brand">◈ Organa</div>

            <h1>Buen día, Christian</h1>
            <div class="date">19 de septiembre de 2026</div>

            <div class="message">
                <h2>Tu carga está bajo control.</h2>
                <p>
                    Organa mantiene vigilados tus frentes.
                    Sólo necesitas abrir aquellos que requieren atención ahora.
                </p>
            </div>

            <div class="summary">

                <div class="card">
                    <div class="number attention">3</div>
                    <strong>Requieren atención</strong>
                    <p>Necesitan movimiento durante los próximos días.</p>
                </div>

                <div class="card">
                    <div class="number advance">5</div>
                    <strong>Conviene avanzar</strong>
                    <p>No son urgentes. Avanzar ahora evita presión futura.</p>
                </div>

                <div class="card">
                    <div class="number controlled">18</div>
                    <strong>Bajo control</strong>
                    <p>No requieren tu atención en este momento.</p>
                </div>

            </div>

            <div class="footer">
                No se trata de hacer más, sino de avanzar en lo que importa.
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
        "version": "0.1.0"
    }
