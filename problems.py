# ============================================
# problems.py - Problemas de Métodos Numéricos del búnker
# ============================================
# Día 1: Interpolación (Lineal o Lagrange)
# Día 2: Ecuaciones No Lineales (Punto Fijo o Falsa Posición)
# Día 3: Ecuaciones Lineales (Gauss-Seidel o Jacobi) — aleatorio
# Día 4: Ecuaciones Lineales (el método que NO se eligió en el día 3)

import random


# ============================================
#  DEFINICIÓN DE PROBLEMAS POR TEMA
# ============================================

# --- DÍA 1: INTERPOLACIÓN ---

INTERPOLACION_LINEAL = {
    "day": 1,
    "topic": "Interpolación Lineal",
    "text": (
        "Estimar el Ln de 3 mediante interpolación lineal.\n"
        "- Realice el cálculo entre Ln 2 y Ln 5."
    ),
    "fields": [
        {"label": "g(x)=", "answer": "0.998577424"},
        {"label": "Є=", "answer": "0.100034865"},
    ],
    "hints": {
        "green":  "Pista: Usa f(x0) + [f(x1)-f(x0)]/(x1-x0) * (x-x0)",
        "red":    "Pista: x0=2, x1=5, f(x0)=ln(2), f(x1)=ln(5)",
        "blue":   "Pista: ln(2)=0.6931, ln(5)=1.6094",
        "purple": "Pista: Error = |valor real - valor aprox| / valor real",
    },
}

LAGRANGE = {
    "day": 1,
    "topic": "Lagrange",
    "text": (
        "Obtener g(x) para x=3\n"
        "\n"
        "Xi    Yi\n"
        " 1.7  0.35\n"
        " 2.4  0.87\n"
        " 3.1  1.03"
    ),
    "fields": [
        {"label": "g(x)=", "answer": "1.072040816"},
    ],
    "hints": {
        "green":  "Pista: g(x) = Σ yi * Li(x)",
        "red":    "Pista: Li(x) = Π (x-xj)/(xi-xj) para j≠i",
        "blue":   "Pista: Hay 3 puntos, usa L0, L1, L2",
        "purple": "Pista: Calcula cada Li evaluado en x=3",
    },
}

# --- DÍA 2: ECUACIONES NO LINEALES ---

PUNTO_FIJO = {
    "day": 2,
    "topic": "Punto Fijo",
    "text": (
        "Localizar la raíz de f(x) = e^(-x) – x,\n"
        "la función se puede separar directamente y\n"
        "expresarse en la forma xi+1 = g(xi).\n"
        "\n"
        "X i+1 = e^(-xi) empezando con un valor\n"
        "inicial X0 = 0. Se aplica esta ecuación\n"
        "iterativa para calcular.\n"
        " f(x) = e^(-x) – x"
    ),
    "fields": [
        {"label": "Iteraciones=", "answer": "22"},
        {"label": "Margen de Error(Є)=", "answer": "0.0000069328"},
    ],
    "hints": {
        "green":  "Pista: Itera xi+1 = e^(-xi) desde x0=0",
        "red":    "Pista: Calcula |xi+1 - xi| en cada paso",
        "blue":   "Pista: Continúa hasta convergencia",
        "purple": "Pista: La raíz está cerca de 0.5671",
    },
}

FALSA_POSICION = {
    "day": 2,
    "topic": "Método de la Falsa Posición",
    "text": (
        "Calcule la raíz para\n"
        "f(x)= 3x³ – 2x – 3"
    ),
    "fields": [
        {"label": "Iteraciones=", "answer": "7"},
        {"label": "Margen de Error(Є)=", "answer": "0.0016"},
    ],
    "hints": {
        "green":  "Pista: Busca un intervalo [a,b] donde f cambie de signo",
        "red":    "Pista: xr = b - f(b)*(a-b) / (f(a)-f(b))",
        "blue":   "Pista: Evalúa f(xr) para elegir nuevo intervalo",
        "purple": "Pista: Repite hasta que el error sea pequeño",
    },
}

# --- DÍA 3-4: ECUACIONES LINEALES ---

GAUSS_SEIDEL = {
    "day": 3,
    "topic": "Gauss-Seidel",
    "text": (
        "1) 3a – 0.1b – 0.2c = 7.85\n"
        "2) 0.1a + 7b – 0.3c = -19.3\n"
        "3) 0.3a – 0.2b + 10c = 71.4"
    ),
    "fields": [
        {"label": "Iteración=", "answer": "4"},
        {"label": "a=", "answer": "3.000000352"},
        {"label": "b=", "answer": "-2.500000036"},
        {"label": "c=", "answer": "6.999999989"},
        {"label": "Margen de Error(Є,a)=", "answer": "0.000031545"},
        {"label": "Margen de Error(Є,b)=", "answer": "0.000012043"},
        {"label": "Margen de Error(Є,c)=", "answer": "0.00000070"},
    ],
    "hints": {
        "green":  "Pista: Despeja a, b, c de cada ecuación",
        "red":    "Pista: Usa los valores más recientes",
        "blue":   "Pista: a=(7.85+0.1b+0.2c)/3",
        "purple": "Pista: Itera hasta que el error sea pequeño",
    },
}

JACOBI = {
    "day": 3,
    "topic": "Jacobi",
    "text": (
        "1) 3a – 0.1b – 0.2c = 7.85\n"
        "2) 0.1a + 7b – 0.3c = -19.3\n"
        "3) 0.3a – 0.2b + 10c = 71.4"
    ),
    "fields": [
        {"label": "Iteración=", "answer": "4"},
        {"label": "a=", "answer": "3.000015844"},
        {"label": "b=", "answer": "-2.500001424"},
        {"label": "c=", "answer": "6.999985592"},
        {"label": "Margen de Error(Є,a)=", "answer": "0.000566696"},
        {"label": "Margen de Error(Є,b)=", "answer": "0.000154825"},
        {"label": "Margen de Error(Є,c)=", "answer": "0.00017536"},
    ],
    "hints": {
        "green":  "Pista: Despeja a, b, c de cada ecuación",
        "red":    "Pista: Usa los valores de la iteración anterior",
        "blue":   "Pista: No uses valores actualizados como Gauss-Seidel",
        "purple": "Pista: Itera hasta convergencia",
    },
}


# ============================================
#  SELECCIÓN DE PROBLEMAS PARA EL BÚNKER
# ============================================

def get_bunker_problems():
    """
    Genera la lista de 4 problemas para los 4 días del búnker.
    - Día 1: Interpolación Lineal o Lagrange (aleatorio)
    - Día 2: Punto Fijo o Falsa Posición (aleatorio)
    - Día 3: Gauss-Seidel o Jacobi (aleatorio)
    - Día 4: el método que NO se eligió en el día 3

    Retorna una lista de 4 diccionarios de problemas.
    """
    # Día 1: Interpolación (aleatorio)
    day1 = random.choice([INTERPOLACION_LINEAL, LAGRANGE])

    # Día 2: Ecuaciones No Lineales (aleatorio)
    day2 = random.choice([PUNTO_FIJO, FALSA_POSICION])

    # Día 3 y 4: Ecuaciones Lineales (uno aleatorio, el otro el opuesto)
    linear_methods = [GAUSS_SEIDEL, JACOBI]
    random.shuffle(linear_methods)
    day3 = linear_methods[0]
    day4 = linear_methods[1]

    # Asignar el día correcto a day4
    day3_copy = dict(day3)
    day3_copy["day"] = 3
    day4_copy = dict(day4)
    day4_copy["day"] = 4

    return [day1, day2, day3_copy, day4_copy]


# ============================================
#  VALIDACIÓN DE RESPUESTAS
# ============================================

def check_field_answer(expected_str, user_str):
    """
    Verifica si la respuesta del usuario es correcta según las reglas:
    - Si el valor esperado es entero (sin punto o '.0'), comparación exacta.
    - Si es decimal, se requieren al menos los primeros 4 caracteres
      después del punto decimal correctos.
    - Se permiten dígitos adicionales (hasta 10 después del punto).
    - No importa lo que haya antes del punto decimal.

    Parámetros:
        expected_str: string con la respuesta correcta (ej: "0.998577424")
        user_str: string con la respuesta del usuario

    Retorna True si es correcta.
    """
    if user_str is None or user_str.strip() == "":
        return False

    user_str = user_str.strip()
    expected_str = expected_str.strip()

    # --- Caso entero (ej: Iteraciones = 22, 7, 4) ---
    if "." not in expected_str:
        try:
            return int(user_str) == int(expected_str)
        except (ValueError, TypeError):
            return False

    # --- Caso decimal ---
    # Verificar que el usuario ingresó un punto decimal
    if "." not in user_str:
        return False

    try:
        # Validar que sea un número válido
        float(user_str)
        float(expected_str)
    except (ValueError, TypeError):
        return False

    # Extraer la parte después del punto decimal
    expected_decimal = expected_str.split(".")[1]
    user_decimal = user_str.split(".")[1]

    # Se requieren al menos 4 caracteres después del punto
    min_digits = min(4, len(expected_decimal))
    if len(user_decimal) < min_digits:
        return False

    # Verificar que los primeros 4 dígitos después del punto coincidan
    expected_prefix = expected_decimal[:min_digits]
    user_prefix = user_decimal[:min_digits]

    if expected_prefix != user_prefix:
        return False

    # Verificar el signo (positivo/negativo)
    expected_negative = expected_str.startswith("-")
    user_negative = user_str.startswith("-")
    if expected_negative != user_negative:
        return False

    return True


def check_all_fields(problem, user_answers):
    """
    Verifica todas las respuestas de un problema con múltiples campos.

    Parámetros:
        problem: diccionario del problema con "fields"
        user_answers: lista de strings con las respuestas del usuario

    Retorna True si TODAS las respuestas son correctas.
    """
    fields = problem.get("fields", [])
    if len(user_answers) != len(fields):
        return False

    for field, user_ans in zip(fields, user_answers):
        if not check_field_answer(field["answer"], user_ans):
            return False

    return True


# ============================================
#  FUNCIONES LEGACY (compatibilidad)
# ============================================

def get_random_problems(count=4):
    """
    Función legacy — redirige a get_bunker_problems().
    """
    return get_bunker_problems()


def check_answer(problem, user_answer):
    """
    Función legacy para problemas de un solo campo.
    """
    if "fields" in problem and len(problem["fields"]) > 0:
        # Nuevo formato: usar check_field_answer con el primer campo
        return check_field_answer(problem["fields"][0]["answer"], str(user_answer) if user_answer is not None else "")
    return False
