"""
config.py
Patrones de preferencias, constantes del modelo y configuración general.
"""

# ---------------------------------------------------------------------------
# Parámetros del vectorizador TF-IDF
# ---------------------------------------------------------------------------

TFIDF_PARAMS = dict(
    max_features=4000,
    ngram_range=(1, 3),
    stop_words="english",
    min_df=3,
    max_df=0.7,
    sublinear_tf=True,
)

# ---------------------------------------------------------------------------
# Columnas para exportar
# ---------------------------------------------------------------------------

EXPORT_COLUMNS = [
    "original_title", "author", "avg_rating",
    "ratings_count", "num_pages", "original_publication_year", "match_percentage",
]

# ---------------------------------------------------------------------------
# Patrones de preferencias
# Cada entrada tiene: keywords (para TF-IDF), weight, description e icon
# ---------------------------------------------------------------------------

VIBES_PATTERNS = {
    "Mysterious yet Cozy": {
        "keywords": ["mysterious", "cozy", "atmospheric", "intimate", "secrets", "warm", "comfort", "puzzle", "intrigue", "homey"],
        "weight": 1.5,
        "description": "Books that wrap you in intrigue but feel like coming home.",
        "icon": "fas fa-house-chimney-user",
    },
    "Tense yet Amusing": {
        "keywords": ["suspenseful", "witty", "entertaining", "thrilling", "humor", "fast paced", "exciting", "clever", "amusing", "engaging"],
        "weight": 1.3,
        "description": "Reads that keep you on the edge of your seat, but still make you chuckle.",
        "icon": "fas fa-face-grin-squint-tears",
    },
    "Profound yet Approachable": {
        "keywords": ["profound", "accessible", "thoughtful", "readable", "philosophical", "meaningful", "simple", "clear", "insightful", "gentle"],
        "weight": 1.4,
        "description": "Books that delve into deep themes without being a heavy read.",
        "icon": "fas fa-lightbulb",
    },
    "Intense yet Hopeful": {
        "keywords": ["intense", "powerful", "hopeful", "uplifting", "emotional", "inspiring", "dramatic", "moving", "optimistic", "resilient"],
        "weight": 1.2,
        "description": "Stories that hit you hard but leave you with a sense of optimism.",
        "icon": "fas fa-sun",
    },
    "Romantic yet Realistic": {
        "keywords": ["romantic", "realistic", "authentic", "genuine", "love", "relationship", "believable", "honest", "mature", "contemporary"],
        "weight": 1.3,
        "description": "Love stories that feel authentic and truly possible.",
        "icon": "fas fa-heart-circle-check",
    },
    "Fantastic yet Believable": {
        "keywords": ["fantasy", "magical", "believable", "grounded", "imaginative", "realistic", "wonder", "enchanting", "plausible", "vivid"],
        "weight": 1.4,
        "description": "Imaginative tales that could almost exist in our world.",
        "icon": "fas fa-wand-magic-sparkles",
    },
}

ELEMENTOS_PATTERNS = {
    "Clever Dialogues": {
        "keywords": ["dialogue", "conversation", "witty", "sharp", "banter", "clever", "verbal", "exchange", "talk", "discussion"],
        "weight": 1.5,
        "description": "Books where the conversations alone captivate you.",
        "icon": "fas fa-comments",
    },
    "Unfolding Mysteries": {
        "keywords": ["mystery", "reveals", "secrets", "unraveling", "clues", "discovery", "unveiling", "hidden", "solving", "truth"],
        "weight": 1.4,
        "description": "Reads that slowly unveil their secrets, one revelation at a time.",
        "icon": "fas fa-magnifying-glass",
    },
    "Complex Characters": {
        "keywords": ["complex", "flawed", "nuanced", "developed", "multifaceted", "realistic", "depth", "layered", "human", "relatable"],
        "weight": 1.6,
        "description": "Stories with people who feel real, flawed, and deeply intricate.",
        "icon": "fas fa-user-tie",
    },
    "Immersive Worlds": {
        "keywords": ["world", "setting", "atmosphere", "immersive", "vivid", "detailed", "rich", "environment", "place", "landscape"],
        "weight": 1.3,
        "description": "Books that completely transport you to another time or place.",
        "icon": "fas fa-earth-americas",
    },
    "Unexpected Twists": {
        "keywords": ["twist", "unexpected", "surprise", "shocking", "revelation", "turn", "unpredictable", "plot", "stunning", "jaw dropping"],
        "weight": 1.2,
        "description": "Reads that shock you when you least expect it.",
        "icon": "fas fa-shuffle",
    },
    "Authentic Emotions": {
        "keywords": ["emotional", "heartfelt", "genuine", "moving", "touching", "authentic", "real", "feelings", "poignant", "affecting"],
        "weight": 1.4,
        "description": "Books that stir genuine feelings and resonate deeply.",
        "icon": "fas fa-face-grin-hearts",
    },
}

DEPTHS_PATTERNS = {
    "Quietly Profound": {
        "keywords": ["subtle", "understated", "quiet", "contemplative", "reflective", "meditative", "nuanced", "gentle wisdom", "soft insights", "unspoken"],
        "weight": 1.4,
        "description": "Books that offer deep insights without dramatic flourishes.",
        "icon": "fas fa-dove",
    },
    "Layered Storytelling": {
        "keywords": ["layered", "multiple levels", "beneath surface", "hidden meanings", "symbolic", "metaphorical", "allegory", "subtext", "deeper meaning", "interconnected"],
        "weight": 1.5,
        "description": "Narratives that reveal new meanings with each reading.",
        "icon": "fas fa-layer-group",
    },
    "Understated Intensity": {
        "keywords": ["tension beneath", "quiet intensity", "simmering", "restrained", "controlled", "implicit", "unspoken tension", "subtle power", "contained emotion"],
        "weight": 1.3,
        "description": "Stories where the most powerful moments whisper rather than shout.",
        "icon": "fas fa-compress",
    },
    "Philosophical Undertones": {
        "keywords": ["philosophical", "existential", "moral questions", "ethical", "meaning of life", "human condition", "deeper questions", "thoughtful exploration", "wisdom"],
        "weight": 1.4,
        "description": "Books that explore life's big questions through compelling stories.",
        "icon": "fas fa-brain",
    },
    "Psychological Nuance": {
        "keywords": ["psychological", "mental landscape", "inner life", "consciousness", "psyche", "emotional complexity", "mental state", "introspection", "self awareness"],
        "weight": 1.5,
        "description": "Deep dives into the intricacies of human psychology.",
        "icon": "fas fa-head-side-virus",
    },
    "Subtle Social Commentary": {
        "keywords": ["social commentary", "society", "cultural critique", "social issues", "class", "inequality", "human nature", "civilization", "community", "social dynamics"],
        "weight": 1.3,
        "description": "Elegant examination of society and human relationships.",
        "icon": "fas fa-users",
    },
}

# ---------------------------------------------------------------------------
# Datos para el análisis de Reading DNA
# ---------------------------------------------------------------------------

DNA_PERSONALITY_INDICATORS = {
    "vibes": {
        "Mysterious yet Cozy":       ["introspective", "comfort_seeker"],
        "Tense yet Amusing":         ["thrill_seeker", "humor_lover"],
        "Profound yet Approachable": ["wisdom_seeker", "accessible_learner"],
        "Intense yet Hopeful":       ["emotional_processor", "optimist"],
        "Romantic yet Realistic":    ["relationship_focused", "authenticity_seeker"],
        "Fantastic yet Believable":  ["imagination_balanced", "grounded_dreamer"],
    },
    "elementos": {
        "Clever Dialogues":   ["conversation_lover", "wit_appreciator"],
        "Unfolding Mysteries":["puzzle_solver", "patience_rewarded"],
        "Complex Characters": ["psychology_interested", "depth_seeker"],
        "Immersive Worlds":   ["escapist", "detail_oriented"],
        "Unexpected Twists":  ["surprise_lover", "flexible_mindset"],
        "Authentic Emotions": ["empathy_driven", "emotional_intelligence"],
    },
    "depths": {
        "Quietly Profound":         ["contemplative_soul", "subtle_appreciator"],
        "Layered Storytelling":     ["analytical_reader", "meaning_seeker"],
        "Understated Intensity":    ["sophisticated_taste", "nuance_detector"],
        "Philosophical Undertones": ["deep_thinker", "question_asker"],
        "Psychological Nuance":     ["mind_explorer", "complexity_lover"],
        "Subtle Social Commentary": ["society_observer", "critical_thinker"],
    },
}

DNA_PERSONALITY_TYPES = {
    "introspective":        "The Contemplative Reader 🧘",
    "thrill_seeker":        "The Adrenaline Reader ⚡",
    "wisdom_seeker":        "The Philosophical Explorer 🎯",
    "emotional_processor":  "The Heart-Centered Reader 💝",
    "conversation_lover":   "The Social Intellect 🗣️",
    "puzzle_solver":        "The Literary Detective 🔍",
    "psychology_interested":"The Human Nature Scholar 🧠",
    "escapist":             "The World Traveler 🌍",
    "contemplative_soul":   "The Quiet Wisdom Seeker 🕯️",
    "deep_thinker":         "The Philosophy Explorer 💭",
}

DNA_RARITY_PATTERNS = {
    "Mysterious yet Cozy": 0.15,    "Tense yet Amusing": 0.25,
    "Profound yet Approachable": 0.12, "Intense yet Hopeful": 0.20,
    "Romantic yet Realistic": 0.30, "Fantastic yet Believable": 0.18,
    "Clever Dialogues": 0.22,       "Unfolding Mysteries": 0.28,
    "Complex Characters": 0.16,     "Immersive Worlds": 0.35,
    "Unexpected Twists": 0.32,      "Authentic Emotions": 0.24,
    "Quietly Profound": 0.08,       "Layered Storytelling": 0.10,
    "Understated Intensity": 0.06,  "Philosophical Undertones": 0.12,
    "Psychological Nuance": 0.14,   "Subtle Social Commentary": 0.09,
}

DNA_DISCOVERY_SIGNALS = {
    "hidden_gem": ["Quietly Profound", "Understated Intensity", "Mysterious yet Cozy", "Complex Characters"],
    "mainstream": ["Tense yet Amusing", "Unexpected Twists", "Intense yet Hopeful", "Immersive Worlds"],
    "literary":   ["Philosophical Undertones", "Subtle Social Commentary", "Layered Storytelling"],
}

DNA_FLEXIBILITY_SCORES = {
    "Fantastic yet Believable": 0.9, "Profound yet Approachable": 0.8,
    "Romantic yet Realistic": 0.7,  "Complex Characters": 0.8,
    "Immersive Worlds": 0.9,        "Layered Storytelling": 0.9,
    "Philosophical Undertones": 0.7,"Psychological Nuance": 0.8,
}

DNA_MOOD_MAPPINGS = {
    "Mysterious yet Cozy":       ["contemplative_evening", "rainy_afternoon", "bedtime_reading"],
    "Tense yet Amusing":         ["commute_entertainment", "weekend_adventure", "stress_relief"],
    "Profound yet Approachable": ["personal_growth", "quiet_morning", "life_transition"],
    "Intense yet Hopeful":       ["emotional_processing", "need_inspiration", "difficult_times"],
    "Romantic yet Realistic":    ["relationship_reflection", "emotional_connection", "heart_warming"],
    "Fantastic yet Believable":  ["imagination_escape", "wonder_seeking", "creative_inspiration"],
    "Clever Dialogues":          ["intellectual_stimulation", "social_energy", "wit_appreciation"],
    "Unfolding Mysteries":       ["puzzle_solving_mood", "patient_discovery", "mental_engagement"],
    "Complex Characters":        ["human_understanding", "empathy_building", "psychological_insight"],
    "Immersive Worlds":          ["complete_escape", "world_building_love", "transportation_need"],
    "Unexpected Twists":         ["surprise_seeking", "mind_bending", "predictability_escape"],
    "Authentic Emotions":        ["emotional_validation", "feeling_connection", "heart_opening"],
}
