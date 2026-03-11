# 📚 Summer Reading List Builder

A book recommendation app built entirely with Plotly Dash and Dash Mantine Components — no charts, just a full NLP-powered user experience. Designed to address the challenge of personalized book discovery, it empowers users to find literary works that precisely match their emotional and stylistic preferences through advanced text analysis and machine learning.

## What It Does

The Summer Reading List Builder lets users select their reading preferences across three dimensions — **Vibes**, **Elementos**, and **Depths** — and receive personalized book recommendations in real time.

Beyond recommendations, the app generates a **Reading DNA** profile: a reader archetype, a taste rarity indicator, a discovery potential score, and a mood map — all derived from the user's selections.

---

## How It Works

### NLP Engine — TF-IDF with Scikit-learn

Book descriptions are vectorized at app startup using `TfidfVectorizer` with parameters tuned for literary text:

- `ngram_range=(1, 3)` — captures multi-word concepts like "hidden meanings"
- `sublinear_tf=True` — applies log scaling to prevent long descriptions from dominating
- `max_df=0.7` — filters out generic editorial vocabulary

The resulting TF-IDF matrix is stored as a global app variable, making it instantly available to every callback without recalculation.

### Recommendation Engine — Cosine Similarity

When the user selects preferences, a Dash callback builds a weighted preference vector using the keyword patterns defined in `config.py`. The engine then:

1. Normalizes the user vector
2. Calculates cosine similarity against every book in the matrix
3. Filters results below a 0.05 threshold
4. Returns a ranked list with match percentages

Results are stored in a `dcc.Store` component — the single source of truth consumed by the recommendation cards, the Reading DNA panel, and the file exporter.

### Reading DNA

Two core functions analyze the user's selection pattern:

- `get_reader_personality` — maps trait combinations to reader archetypes (e.g., "The Literary Detective")
- `get_taste_rarity` — compares selections against frequency patterns to determine rarity (e.g., "Ultra Rare Unicorn")

---

## Project Structure

```
├── app.py                 # Dash app, layout, and callbacks
├── recommender.py         # NLP engine and Reading DNA functions
├── config.py              # Preference patterns, weights, and DNA data
├── books_works.csv        # Book dataset (~10 MB)
└── requirements.txt       # Python dependencies
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/summer-reading-list-builder.git
cd summer-reading-list-builder
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
python app.py
```

The app will be available at `http://127.0.0.1:8050`

---

## Requirements

```
dash
dash-mantine-components
scikit-learn
pandas
numpy
```

---

## Key Patterns

| Pattern | Description |
|---|---|
| Pre-calculate outside callbacks | The TF-IDF matrix is built once at startup — any Scikit-learn model works the same way |
| `dcc.Store` as shared truth | All components consume a single store; no redundant recalculation |
| DMC as a design system | `MantineProvider` + `Grid` + `Card` + `Modal` handles layout, consistency, and depth |

---
