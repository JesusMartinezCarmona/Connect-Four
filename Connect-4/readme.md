# Práctica: Agente de Q-Learning para Conecta 4

**Materia/Proyecto:** Inteligencia Artificial
**Profesor(a):** María de Lourdes Aguillón Ruiz
**Alumno:** Jesús Arturo Martínez Carmona
**Institución:** Instituto Tecnológico de Ensenada

---

## 1. Reglas del Juego y Cómo Jugarlo

El entorno de este proyecto es una simulación del clásico juego de mesa "Conecta 4".

**Objetivo:**
Ser el primer jugador en alinear exactamente 4 fichas de su propio color de forma consecutiva. La línea puede ser:
* Horizontal ($\leftrightarrow$)
* Vertical ($\updownarrow$)
* Diagonal ($\nearrow$ o $\searrow$)

**Tablero y Mecánicas:**
* El juego se desarrolla en una cuadrícula vertical de 7 columnas por 6 filas.
* Participan dos jugadores, alternando turnos (Agente vs. Oponente).
* En cada turno, el jugador selecciona una columna (del 0 al 6). La ficha "cae" por efecto de gravedad hasta ocupar la posición vacía más baja de esa columna.
* No es posible insertar fichas en una columna que ya está llena.

**Condiciones de Fin de Partida:**
* **Victoria:** Un jugador forma una línea de 4.
* **Empate:** Las 42 celdas del tablero se llenan sin que ningún jugador logre la condición de victoria.

---

## 2. Dificultades en el Desarrollo

Durante la implementación del entorno gráfico (`game.py`) y el agente de aprendizaje (`q_agent.py`), se presentaron los siguientes retos técnicos:

1.  **Explosión Combinatoria del Espacio de Estados:** La mayor dificultad conceptual y de hardware fue dimensionar el tamaño del problema. Un tablero de 7x6 tiene aproximadamente $4.5 \times 10^{12}$ estados posibles. Manejar esta "memoria" utilizando un diccionario de Python (`Q-Table`) guardado en un archivo `.pkl` requiere un uso eficiente de la memoria RAM, especialmente cuando los entrenamientos superan las miles de iteraciones.
2.  **Representación del Estado:** Hubo que transformar la matriz bidimensional de `numpy` en una tupla unidimensional inmutable para que Python pudiera utilizarla como clave o "llave" hash dentro del diccionario de la Q-Table.
3.  **Diseño de la Función de Recompensa:** Inicialmente, el agente no aprendía a bloquear al oponente. Se tuvo que ajustar la recompensa para penalizar fuertemente (-100) perder la partida, premiar la victoria (+100) y dar un castigo minúsculo por cada turno extra (-0.1) para obligar al agente a buscar ganar lo más rápido posible.

---

## 3. Reporte de Entrenamiento y Análisis de Estados

Para evaluar el rendimiento de la Q-Table, se sometió al agente a distintos volúmenes de iteraciones contra un bot de movimientos aleatorios. El procesamiento se llevó a cabo aprovechando la capacidad de cálculo rápido del equipo de cómputo local.

### Comparativa de Entrenamientos (Episodios)

* **10 Juegos:** El agente solo exploró una cantidad insignificante de estados (menos de 300). La Q-Table quedó prácticamente vacía. No hubo aprendizaje real; los movimientos fueron erráticos y perdió la mayoría de las veces.
* **1,000 Juegos:** La base de conocimiento creció a unos miles de estados. El agente comenzó a reconocer el valor de jugar en la columna central (columna 3), ya que estadísticamente participa en más combinaciones ganadoras. Se observó una mejora en su tasa de victoria, pero seguía cayendo en trampas diagonales simples.
* **10,000 Juegos:** La Q-Table capturó una cantidad masiva de estados tempranos del tablero. Los estados con mayor prioridad (mayor valor Q) convergieron claramente en dominar las columnas 2, 3 y 4. El agente aprendió a bloquear ataques verticales inminentes.

### Comportamiento Esperado vs. No Sucedido
* **Esperado:** Se esperaba que, a mayor número de partidas, el agente aprendiera a ganar más rápido y bloqueara el 100% de los ataques del oponente.
* **No Sucedido:** A pesar de 10,000 entrenamientos, el agente no se volvió invencible. Continuó cometiendo errores de omisión en bloqueos diagonales. Esto ocurre porque 10,000 juegos apenas representan una fracción microscópica de los billones de estados posibles, por lo que el agente se enfrentaba constantemente a tableros que "jamás había visto" en su memoria.

---

## 4. Análisis del Parámetro Epsilon ($\epsilon$)

El parámetro Epsilon controla el equilibrio entre **Exploración** (tomar decisiones aleatorias para descubrir nuevas estrategias) y **Explotación** (usar la Q-Table para tomar la mejor decisión conocida). Se entrenó al agente modificando este valor:

* **$\epsilon = 1$:** El agente jugó de forma 100% aleatoria. No consultó su memoria en absoluto. Es útil solo al inicio ("estado cero") para poblar la Q-Table con situaciones variadas.
* **$\epsilon = 0.8$ y $0.5$:** Se observó un equilibrio. El agente tomaba decisiones lógicas la mitad del tiempo, pero seguía experimentando. Esto permitió que encontrara nuevas formas de ganar sin estancarse en una sola jugada.
* **$\epsilon = 0.2$ y $0.1$:** El agente se volvió altamente competitivo, confiando casi por completo en su aprendizaje previo y solo desviándose ocasionalmente para probar variaciones. Fue el mejor parámetro para entrenamientos largos.
* **$\epsilon = 0.01$:** Exploración casi nula (1%). El agente explotó estrictamente su conocimiento. **Observación crítica:** Si la Q-Table no estaba bien entrenada antes de usar este valor, el agente se volvía predecible y repetía el mismo error partida tras partida, demostrando estancamiento en mínimos locales.

---

## 5. Conclusión General

El desarrollo de este agente demostró físicamente cómo la ecuación de Bellman actualiza los valores de decisión en un entorno dinámico. El agente comenzó desde la ignorancia absoluta y, mediante el esquema de recompensas y castigos, logró estructurar un archivo de memoria (`.pkl`) capaz de dictar estrategias ofensivas.

Tras someterlo al entrenamiento máximo (10,000 iteraciones con un $\epsilon$ decreciente), el agente logró registrar decenas de miles de estados y alcanzó una **tasa de victoria superior al 80%** frente al oponente aleatorio. Sin embargo, el proyecto deja como lección de ingeniería que el Q-Learning tabular tiene un límite físico dictado por la memoria RAM; para resolver por completo juegos de esta magnitud, sería imperativo migrar hacia redes neuronales profundas (Deep Q-Networks) que aproximen las funciones en lugar de memorizar cada tablero exacto.