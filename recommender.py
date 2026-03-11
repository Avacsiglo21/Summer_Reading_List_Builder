"""
recommender.py
Carga de datos, recomendación de libros y análisis de Reading DNA.
Todo como funciones simples
"""

import re
from collections import Counter

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from config import (
    TFIDF_PARAMS,
    VIBES_PATTERNS, ELEMENTOS_PATTERNS, DEPTHS_PATTERNS,
    DNA_PERSONALITY_INDICATORS, DNA_PERSONALITY_TYPES,
    DNA_RARITY_PATTERNS, DNA_DISCOVERY_SIGNALS,
    DNA_FLEXIBILITY_SCORES, DNA_MOOD_MAPPINGS,
)


# ---------------------------------------------------------------------------
# Carga y preprocesamiento
# ---------------------------------------------------------------------------

def clean_text(text):
    """Limpia HTML, saltos de línea y caracteres especiales."""
    if pd.isna(text):
        return ""
    text = re.sub(r"<.*?>", "", text)
    text = re.sub(r"\n+", " ", text)
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.lower().strip()


def load_data(csv_path="books_works.csv"):
    """
    Carga el CSV, limpia descripciones y ajusta el vectorizador TF-IDF.
    Devuelve df, tfidf_matrix, vectorizer.
    """
    df = pd.read_csv(csv_path)
    df["num_pages"] = pd.to_numeric(df["num_pages"], errors="coerce").fillna(0)
    df["clean_description"] = df["description"].apply(clean_text)

    vectorizer = TfidfVectorizer(**TFIDF_PARAMS)
    tfidf_matrix = vectorizer.fit_transform(df["clean_description"])

    return df, tfidf_matrix, vectorizer


# ---------------------------------------------------------------------------
# Motor de recomendaciones
# ---------------------------------------------------------------------------

def build_preference_vector(tfidf_matrix, vectorizer, vibes, elementos, depths):
    """
    Construye un vector de preferencias pesado combinando
    los patrones seleccionados de las tres categorías.
    """
    vector = np.zeros(tfidf_matrix.shape[1])

    for patterns, selected in [
        (VIBES_PATTERNS,    vibes),
        (ELEMENTOS_PATTERNS, elementos),
        (DEPTHS_PATTERNS,   depths),
    ]:
        for name in selected:
            if name in patterns:
                keywords_text = " ".join(patterns[name]["keywords"])
                keyword_vector = vectorizer.transform([keywords_text]).toarray().flatten()
                vector += keyword_vector * patterns[name]["weight"]

    return vector


def find_books(df, tfidf_matrix, vectorizer, vibes, elementos, depths, n=8):
    """
    Recomienda n libros según las preferencias seleccionadas.
    Usa similitud coseno entre el vector de preferencias y las descripciones.
    """
    if not any([vibes, elementos, depths]):
        return df.sort_values("avg_rating", ascending=False).head(n).to_dict("records")

    preference_vector = build_preference_vector(tfidf_matrix, vectorizer, vibes, elementos, depths)

    norm = np.linalg.norm(preference_vector)
    if norm == 0:
        return []
    preference_vector /= norm

    scores = cosine_similarity([preference_vector], tfidf_matrix).flatten()
    top_indices = scores.argsort()[::-1]

    results = []
    for idx in top_indices:
        if scores[idx] <= 0.05:
            break
        book = df.iloc[idx].copy()
        book["similarity_score"]  = scores[idx]
        book["match_percentage"]  = min(100, scores[idx] * 100 * 8)
        results.append(book)
        if len(results) >= n:
            break

    return results


# ---------------------------------------------------------------------------
# Reading DNA
# ---------------------------------------------------------------------------

def get_reader_personality(vibes, elementos, depths):
    """Determina el tipo de lector según los rasgos dominantes."""
    traits = []
    for category, selections in [("vibes", vibes), ("elementos", elementos), ("depths", depths)]:
        for s in selections:
            traits.extend(DNA_PERSONALITY_INDICATORS[category].get(s, []))

    if not traits:
        return {"type": "Curious Explorer 🧭", "confidence": 50}

    counts  = Counter(traits)
    top     = counts.most_common(3)
    p_type  = DNA_PERSONALITY_TYPES.get(top[0][0], "The Unique Reader 🦄")

    return {
        "type":            p_type,
        "dominant_traits": [t for t, _ in top],
        "confidence":      min(100, top[0][1] * 25),
    }


def get_taste_rarity(df, vibes, elementos, depths):
    """Calcula qué tan poco común es la combinación de preferencias."""
    all_selections = vibes + elementos + depths
    if not all_selections:
        return {"rarity": "Explorer", "percentile": 50,
                "description": "Charting new territories!"}

    avg_matches  = np.mean([len(df) * DNA_RARITY_PATTERNS.get(s, 0.15) for s in all_selections])
    rarity_score = (len(df) - avg_matches) / len(df) * 100

    if rarity_score > 85:
        return {"rarity": "Ultra Rare Unicorn 🦄", "percentile": int(rarity_score),
                "description": "You have exquisitely unique taste!"}
    elif rarity_score > 70:
        return {"rarity": "Sophisticated Connoisseur 🍷", "percentile": int(rarity_score),
                "description": "You appreciate the finer nuances that most readers miss."}
    elif rarity_score > 50:
        return {"rarity": "Discerning Reader 🎭", "percentile": int(rarity_score),
                "description": "You know what you like and have refined preferences."}
    elif rarity_score > 30:
        return {"rarity": "Popular Taste 📈", "percentile": int(rarity_score),
                "description": "You enjoy books that resonate with many readers."}
    else:
        return {"rarity": "Universal Appeal 🌟", "percentile": int(rarity_score),
                "description": "You love the classics and crowd favorites!"}


def get_discovery_potential(vibes, elementos, depths):
    """Predice el tipo de descubrimiento literario del lector."""
    all_selections = set(vibes + elementos + depths)
    total = len(all_selections)
    if total == 0:
        return {"type": "Open Explorer", "likelihood": 50, "prediction": "Expect variety!"}

    hidden     = sum(1 for s in all_selections if s in DNA_DISCOVERY_SIGNALS["hidden_gem"]) / total
    literary   = sum(1 for s in all_selections if s in DNA_DISCOVERY_SIGNALS["literary"])   / total
    mainstream = sum(1 for s in all_selections if s in DNA_DISCOVERY_SIGNALS["mainstream"]) / total

    if hidden > 0.5:
        return {"type": "Hidden Gem Hunter 💎", "likelihood": 85,
                "prediction": "Expect 2-3 underrated masterpieces others overlook!"}
    elif literary > 0.4:
        return {"type": "Literary Archaeologist 📚", "likelihood": 75,
                "prediction": "Award-winning literary fiction awaits you."}
    elif mainstream > 0.6:
        return {"type": "Crowd Pleaser Finder 🎯", "likelihood": 60,
                "prediction": "Bestsellers and highly-rated fiction will dominate your list."}
    else:
        return {"type": "Genre Boundary Crosser 🌈", "likelihood": 70,
                "prediction": "Expect surprising cross-genre combinations!"}


def get_genre_flexibility(vibes, elementos, depths):
    """Mide qué tan flexible es el lector entre géneros."""
    all_selections = vibes + elementos + depths
    if not all_selections:
        return {"flexibility": "Unknown Explorer", "score": 50, "recommendation": "Try anything!"}

    avg_flex = np.mean([DNA_FLEXIBILITY_SCORES.get(s, 0.5) for s in all_selections])

    if avg_flex > 0.8:
        return {"flexibility": "Genre Shapeshifter 🦋", "score": int(avg_flex * 100),
                "recommendation": "Try books tagged with multiple genres!"}
    elif avg_flex > 0.6:
        return {"flexibility": "Adventurous Reader 🎢", "score": int(avg_flex * 100),
                "recommendation": "Mix in 1-2 books from unfamiliar genres!"}
    else:
        return {"flexibility": "Comfort Zone Dweller 🏠", "score": int(avg_flex * 100),
                "recommendation": "We'll find the best within your preferred style."}


def get_mood_map(vibes, elementos, depths):
    """Mapea las selecciones a estados de ánimo de lectura."""
    all_moods = []
    for s in vibes + elementos + depths:
        all_moods.extend(DNA_MOOD_MAPPINGS.get(s, []))

    if not all_moods:
        return {"primary_moods": ["Exploration"], "description": "Ready for any reading adventure!"}

    top_moods = Counter(all_moods).most_common(3)
    return {
        "primary_moods": [m.replace("_", " ").title() for m, _ in top_moods],
        "description":   f"Your books serve {len(set(all_moods))} different emotional needs!",
    }


def analyze_reading_dna(df, vibes, elementos, depths):
    """
    Combina todas las funciones de DNA en un único perfil.
    Punto de entrada principal para el análisis.
    """
    return {
        "personality":  get_reader_personality(vibes, elementos, depths),
        "rarity":       get_taste_rarity(df, vibes, elementos, depths),
        "discovery":    get_discovery_potential(vibes, elementos, depths),
        "flexibility":  get_genre_flexibility(vibes, elementos, depths),
        "mood_map":     get_mood_map(vibes, elementos, depths),
    }


