# ============================================
# problems.py - Problemas matemáticos del búnker
# ============================================
# Por ahora: sumas y restas simples.
# Luego se reemplazarán con problemas de Métodos Numéricos.

import random

# Cada problema: (enunciado, respuesta_correcta, pista_por_color)
# pista_por_color: {color: texto_pista}

PROBLEMS = [
    {
        "text": "¿Cuánto es 147 + 285?",
        "answer": 432,
        "tolerance": 0.01,
        "hints": {
            "green":  "Pista: Suma las unidades primero (7+5=12)",
            "red":    "Pista: Lleva 1 a las decenas",
            "blue":   "Pista: 147 + 285 = 147 + 300 - 15",
            "purple": "Pista: Descompón: 100+200=300, 47+85=132",
        }
    },
    {
        "text": "¿Cuánto es 523 - 187?",
        "answer": 336,
        "tolerance": 0.01,
        "hints": {
            "green":  "Pista: Resta por partes: 523-200+13",
            "red":    "Pista: 523 - 187 = 523 - 200 + 13",
            "blue":   "Pista: Pide prestado de las centenas",
            "purple": "Pista: Verifica: 336 + 187 = 523",
        }
    },
    {
        "text": "¿Cuánto es 89 + 234 + 57?",
        "answer": 380,
        "tolerance": 0.01,
        "hints": {
            "green":  "Pista: Primero suma 89+234=323",
            "red":    "Pista: Luego 323+57=380",
            "blue":   "Pista: Agrupa: (89+57)+234 = 146+234",
            "purple": "Pista: Redondea: 90+234+57-1",
        }
    },
    {
        "text": "¿Cuánto es 1000 - 367?",
        "answer": 633,
        "tolerance": 0.01,
        "hints": {
            "green":  "Pista: 1000 - 367 = 999 - 367 + 1",
            "red":    "Pista: 999-367 = 632, luego +1",
            "blue":   "Pista: Resta por partes: 1000-300-60-7",
            "purple": "Pista: Verifica: 633+367=1000",
        }
    },
    {
        "text": "¿Cuánto es 456 + 789?",
        "answer": 1245,
        "tolerance": 0.01,
        "hints": {
            "green":  "Pista: 6+9=15, lleva 1",
            "red":    "Pista: 5+8+1=14, lleva 1",
            "blue":   "Pista: 4+7+1=12",
            "purple": "Pista: 456+800-11",
        }
    },
    {
        "text": "¿Cuánto es 2048 - 999?",
        "answer": 1049,
        "tolerance": 0.01,
        "hints": {
            "green":  "Pista: 2048-1000+1",
            "red":    "Pista: Resta 1000 y suma 1",
            "blue":   "Pista: 2048-999 = 2049-1000",
            "purple": "Pista: Verifica: 1049+999=2048",
        }
    },
    {
        "text": "¿Cuánto es 375 + 625?",
        "answer": 1000,
        "tolerance": 0.01,
        "hints": {
            "green":  "Pista: Son complementos a 1000",
            "red":    "Pista: 375 + 625 = 375 + 600 + 25",
            "blue":   "Pista: 5+5=10, 7+2+1=10, 3+6+1=10",
            "purple": "Pista: El resultado es un número redondo",
        }
    },
    {
        "text": "¿Cuánto es 843 - 456?",
        "answer": 387,
        "tolerance": 0.01,
        "hints": {
            "green":  "Pista: 843-456: pide prestado en unidades",
            "red":    "Pista: 13-6=7, 13-5=8 (con préstamo), 7-4=3",
            "blue":   "Pista: 843-400-50-6",
            "purple": "Pista: Verifica: 387+456=843",
        }
    },
    {
        "text": "¿Cuánto es 1234 + 4321?",
        "answer": 5555,
        "tolerance": 0.01,
        "hints": {
            "green":  "Pista: 4+1=5, 3+2=5, 2+3=5, 1+4=5",
            "red":    "Pista: Observa el patrón de las sumas",
            "blue":   "Pista: Todos los dígitos del resultado son iguales",
            "purple": "Pista: El resultado es un número repetitivo",
        }
    },
    {
        "text": "¿Cuánto es 5000 - 1738?",
        "answer": 3262,
        "tolerance": 0.01,
        "hints": {
            "green":  "Pista: 5000-1738 = 4999-1738+1",
            "red":    "Pista: 4999-1738 = 3261",
            "blue":   "Pista: Resta por partes: 5000-1700-38",
            "purple": "Pista: Verifica: 3262+1738=5000",
        }
    },
]


def get_random_problems(count=4):
    """
    Selecciona 'count' problemas aleatorios sin repetición.
    Retorna una lista de diccionarios con los problemas.
    """
    selected = random.sample(PROBLEMS, min(count, len(PROBLEMS)))
    return selected


def check_answer(problem, user_answer):
    """
    Verifica si la respuesta del usuario es correcta.
    Compara con tolerancia.
    Retorna True si es correcta.
    """
    if user_answer is None:
        return False

    try:
        expected = float(problem["answer"])
        given = float(user_answer)
        tolerance = problem.get("tolerance", 0.01)
        return abs(expected - given) <= tolerance
    except (ValueError, TypeError):
        return False
