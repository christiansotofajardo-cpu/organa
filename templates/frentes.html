<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <title>Organa · Frentes</title>

    <link
        rel="stylesheet"
        href="/static/style.css"
    >
</head>


<body>

<div class="container">

    <header>

        <div class="brand">
            ◇ Organa
        </div>

        <nav>
            <a href="/">Hoy</a>
            <a href="/horizonte">Horizonte</a>
            <a class="active" href="/frentes">Frentes</a>
        </nav>

    </header>


    <h1>
        Frentes
    </h1>

    <div class="subtitle">

        Todo está aquí.
        No significa que todo necesite tu atención.

    </div>


    <div class="front-toolbar">

        <div class="filters">

            <span class="filter active">
                Todos
            </span>

            <span class="filter">
                Atención
            </span>

            <span class="filter">
                En curso
            </span>

            <span class="filter">
                En espera
            </span>

            <span class="filter">
                Dormidos
            </span>

        </div>


        <div class="total-fronts">
            {{ total_fronts }} frentes registrados
        </div>

    </div>


    {% for group in groups %}

    <section class="front-group">

        <div class="front-group-title">

            <h2>
                {{ group.title }}
            </h2>

            <span>
                {{ group.items|length }}
            </span>

        </div>


        {% for item in group.items %}

        <details class="front">

            <summary>

                <span
                    class="dot"
                    style="background:{{ item.color }}"
                ></span>


                <div>

                    <div class="front-title">
                        {{ item.front.name }}
                    </div>

                    <div class="front-reason">
                        {{ item.reason }}
                    </div>

                </div>


                <div class="area">
                    {{ item.front.area }}
                </div>


                <span
                    class="badge"
                    style="
                        color:{{ item.color }};
                        background:{{ item.background }};
                    "
                >
                    {{ item.label|upper }}
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
                        {{ item.front.next_action or "Sin próxima acción definida." }}
                    </div>


                    <div class="steps">

                        {% for step in item.front.steps %}

                        <div class="step {% if step.completed %}done{% endif %}">

                            <span>
                                {% if step.completed %}✓{% else %}○{% endif %}
                            </span>

                            <span>
                                {{ step.title }}
                            </span>

                        </div>

                        {% endfor %}

                    </div>

                </div>


                <div class="facts">

                    <div class="fact">
                        <span>Área</span>
                        <strong>{{ item.front.area }}</strong>
                    </div>

                    <div class="fact">
                        <span>Deadline</span>
                        <strong>{{ item.deadline_text }}</strong>
                    </div>

                    <div class="fact">
                        <span>Trabajo restante</span>
                        <strong>{{ item.hours_text }}</strong>
                    </div>

                    <div class="fact">
                        <span>Avance</span>
                        <strong>{{ item.front.progress }}%</strong>
                    </div>

                    <div class="fact">
                        <span>Próxima revisión</span>
                        <strong>{{ item.review_text }}</strong>
                    </div>

                    <div class="fact">
                        <span>Presión</span>
                        <strong>{{ item.pressure }}/100</strong>
                    </div>

                </div>

            </div>

        </details>

        {% endfor %}

    </section>

    {% endfor %}


    <div class="covered">

        <strong>
            Que un frente aparezca aquí no significa que debas abrirlo.
        </strong>

        Organa conserva el panorama completo para que tu memoria
        no tenga que hacerlo.

    </div>


    <div class="footer">
        Todo registrado. Sólo una parte necesita estar presente.
    </div>

</div>

</body>

</html>
