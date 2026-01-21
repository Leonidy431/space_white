PROPHETIC NARRATIVE ENGINE: README

Синтез архетипической фантастики и богословского анализа
Версия: 1.0 (Beta)
Дата: 19 января 2026, Москва

═══════════════════════════════════════════════════════════════════════════════

ОПИСАНИЕ ПРОЕКТА

Prophetic Narrative Engine (PNE) — это система для анализа и генерации нарративных произведений (романы, сценарии, главы) с встроенной проверкой на соответствие:

1. Архетипической структуре 12 домов гороскопа (богословско-астрологическая система)
2. Учению святых отцов Православной Церкви (патристике)
3. Синтезу 4 основных полюсов: Барон + Дивов + Панов + Облачный Атлас
4. Эсхатологической логике апокалипсиса как трансформации сознания

НАЗНАЧЕНИЕ:

- Анализировать готовые тексты и выявлять их богословско-архетипическую структуру
- Генерировать новые главы/сценарии в соответствии с выбранной парадигмой
- Проверять текст на соответствие учению святых отцов (Паламизм, теозис, апофатизм)
- Классифицировать авторов по системе 12 домов и 4 полюсов

═══════════════════════════════════════════════════════════════════════════════

АРХИТЕКТУРА СИСТЕМЫ

PNE состоит из 5 основных модулей:

MODULE 1: TEXTUAL ANALYZER (Анализатор текста)
─────────────────────────────────────────────
Функция: Разбирает входящий текст (глава, сценарий, абзац) и определяет:

- Доминантный дом гороскопа (1-12)
- Вторичные дома (обычно 2-4)
- Архетипический тип персонажа (из системы 199+ авторов)
- Богословское качество (образ Божий, служение, смерть/трансформация и т.д.)
- Соответствие учению святых отцов (✓ соответствует, ⚠ спорно, ✗ противоречит)

Выход: JSON с меткировкой текста по домам и богословским категориям

ПРИМЕР:

Входящий текст:
"Герой стоит перед лицом астероида, который грозит уничтожить человечество. Он должен выбрать: спасать только избранных или рискнуть ради всех?"

Анализ:
{
  "dominant_house": 8,  // Смерть, трансформация, апокалипсис
  "secondary_houses": [10, 11, 2],  // Судьба человечества, коллектив, имущество
  "archetypal_type": "Baron_Apocalypse",  // Соответствует парадигме Барона
  "theological_quality": "Theosis_through_trial",  // Теозис через испытание
  "patristic_alignment": "✓ sobornost_principle",  // Принцип соборности (св. Максим Исповедник)
  "eschatology": "actualization",  // Апокалипсис как актуализация скрытого
  "confidence": 0.92
}

───────────────────────────────────────────────────────────────────────────────

MODULE 2: THEOLOGICAL VALIDATOR (Теологический валидатор)
──────────────────────────────────────────────────────
Функция: Проверяет текст на соответствие учению святых отцов

Проверяемые парадигмы:

A. PALAMITE THEOLOGY (Паламизм — св. Григорий Палама)
   ✓ Различие между сущностью и энергией Бога
   ✓ Обожение (theosis) как целью человеческой жизни
   ✓ Божественный свет как познаваемость Бога
   ✗ Отрицание обожения
   ✗ Материализм как полнота реальности

B. APOPHATIC THEOLOGY (Апофатическое богословие)
   ✓ Тайна как центр, а не изъян
   ✓ "Путь отрицания" (via negativa) как доступ к трансцендентному
   ✓ Молчание как высшая форма молитвы
   ✗ Рациональное объяснение всего
   ✗ Убеждение, что человек может полностью познать Бога умом

C. SOBORNOST (Соборность — св. Сергей Булгаков, св. Николай Бердяев)
   ✓ Спасение как коллективный процесс, а не индивидуальный
   ✓ Церковь как органическое единство в множественности
   ✓ Единство в разнообразии (как в "Облачном Атласе")
   ✗ Индивидуализм как путь спасения
   ✗ Отрицание роли общины

D. ESCHATOLOGY (Эсхатология — св. Максим Исповедник, св. Иоанн Дамаскин)
   ✓ Апокалипсис как раскрытие (apocalypsis), а не конец
   ✓ История как спираль, восходящая к Богу
   ✓ Судьба человечества как предмет Божественной любви
   ✗ Линейный прогресс без трансцендентного смысла
   ✗ Конец мира как уничтожение, а не трансформация

E. THEOSIS (Обожение — св. Афанасий Александрийский)
   ✓ "Бог стал человеком, чтобы человек стал богом" (не как гордыня, а как синергия)
   ✓ Трансформация человеческой природы через причастие Божественной энергии
   ✓ Испытание как инициация в обожение
   ✗ Спасение как юридический акт (только католичество)
   ✗ Отрицание возможности обожения

Выход: Отчет с указанием соответствий и противоречий

───────────────────────────────────────────────────────────────────────────────

MODULE 3: CHAPTER GENERATOR (Генератор глав)
──────────────────────────────────────────────
Функция: На основе заданного параметра (дом, богословское качество, архетип, длина) генерирует новую главу

ВХОДНЫЕ ПАРАМЕТРЫ:

- dominant_house: 1-12 (или "auto" для автоопределения)
- theological_quality: "theosis", "apophatic", "sobornost", "eschatology" и т.д.
- archetypal_vector: "Baron_Apocalypse", "Divov_Collective", "Panov_TechnoFuture", "Wachowski_Eternal"
- character_archetype: "Hero", "Prophet", "Martyr", "Fool", "Sage", "Warrior", "Mother"
- scene_type: "dialogue", "action", "meditation", "revelation", "sacrifice", "transformation"
- word_count: 500-5000
- language: "Russian", "English", "Polish" и т.д.
- patristic_constraints: Список святых отцов, чьё учение должно быть соблюдено
- previous_chapters: Контекст из предыдущих глав (для консистентности архетипа)

ПРИМЕР ИСПОЛЬЗОВАНИЯ:

POST /generate-chapter
{
  "dominant_house": 8,
  "theological_quality": "theosis_through_trial",
  "archetypal_vector": "Baron_Apocalypse",
  "character_archetype": "Prophet",
  "scene_type": "revelation",
  "word_count": 1500,
  "language": "Russian",
  "patristic_constraints": ["Gregory_Palamas", "Maximus_Confessor", "John_Damascene"],
  "context": "The protagonist realizes that the asteroid is not a curse, but an invitation...",
  "tone": "Apocalyptic yet hopeful, with hints of divine irony"
}

ВЫХОД:

Новая глава (1500 слов) с метаданными:
- Dominant house: 8
- Secondary houses: [10, 11, 12]
- Key theological moments: [timestamp1, timestamp2, ...]
- Patristic references: [Палама, Максим, Дамаскин]
- Archetypal resonances: Синхронизация с "Облачным Атласом", "Третьим пришествием", "Многоликим хаосом"

───────────────────────────────────────────────────────────────────────────────

MODULE 4: AUTHOR CLASSIFIER (Классификатор авторов)
────────────────────────────────────────────────────
Функция: Анализирует полное произведение (роман, цикл, творчество автора) и размещает его в системе 199+ авторов

Выход:
- Primary house: 1-12
- Secondary houses: 2-5 домов
- Vector: Baron / Divov / Panov / Wachowski / Orthodox Saints
- Tier: Master (основатель парадигмы), Tier 2 (непосредственные наследники), Tier 3 (расширенное кольцо)
- Language: Russian, English, Polish, German и т.д.
- Theological alignment: % соответствия учению святых отцов
- Recommended reading order: С какого произведения начать понимание архетипа
- Synchronistic resonances: Какие другие авторы резонируют с этим автором

ПРИМЕР:

POST /classify-author
{
  "author_name": "Алексей Барон",
  "primary_works": ["Третье пришествие", "Зазаборье", "Карробус 337"],
  "language": "Russian",
  "analysis_depth": "full"
}

ВЫХОД:

{
  "author": "Alexey Baron",
  "primary_house": 8,
  "secondary_houses": [10, 11, 2],
  "vector": "Baron_Apocalypse",
  "tier": "Master",
  "language": "Russian",
  "theological_alignment": 0.95,
  "patristic_authorities": ["Gregory_Palamas", "Maximus_Confessor", "John_Damascus"],
  "key_works": {
    "Third_Coming": "House_8_transformation_through_trial",
    "Carrobus_337": "House_1_eternal_principle_in_man"
  },
  "synchronistic_partners": [
    "Divov_Sergey",
    "Panov_Vadim",
    "Wachowski_Sisters",
    "Nicol_Arkady",
    "Eskov_Kirill"
  ],
  "recommended_reading_order": [
    "Карробус 337",
    "Третье пришествие",
    "Зазаборье"
  ]
}

───────────────────────────────────────────────────────────────────────────────

MODULE 5: SYNCHRONICITY MAPPER (Картограф синхронии)
────────────────────────────────────────────────────
Функция: Показывает, как архетипы резонируют через авторов, эпохи, языки

Выход: Интерактивная карта с связями:
- Какие авторы синхронизированы через один и тот же дом?
- Как одна идея проходит через разные авторов в разные эпохи?
- Какие "голоса одного Логоса" звучат синхронно?

ПРИМЕР:

POST /map-synchronicity
{
  "theme": "apocalypse_as_awakening",
  "houses": [8, 10, 11, 12],
  "vectors": ["Baron_Apocalypse", "Divov_Collective"],
  "time_range": "1970-2026",
  "languages": ["Russian", "English", "Polish"]
}

ВЫХОД: Граф синхронии с узлами (авторы) и связями (архетипическая резонанция)

═══════════════════════════════════════════════════════════════════════════════

ИСПОЛЬЗОВАНИЕ: ПОШАГОВЫЕ ПРИМЕРЫ

СЦЕНАРИЙ 1: Анализ готовой главы

1. Вы написали главу романа
2. Загружаете текст в PNE
3. PNE выдает:
   - Какой дом доминирует?
   - Какое богословское качество присутствует?
   - Соответствует ли текст учению святых отцов?
   - Какие архетипы резонируют в тексте?
   - Рекомендации по улучшению (если есть противоречия)

СЦЕНАРИЙ 2: Генерация следующей главы

1. Вы закончили главу 5 (дом 8 — смерть героя)
2. Нужна глава 6, которая логично продолжит архетипическую дугу
3. Задаете параметры: дом 10 (судьба), тип сцены "resurrection", длина 2000 слов
4. PNE генерирует главу, которая:
   - Поднимается от смерти к воскрешению (движение от дома 8 к 10)
   - Сохраняет архетипические голоса персонажей
   - Вводит новые богословские слои
   - Синхронизируется с глав 1-5

СЦЕНАРИЙ 3: Классификация нового автора

1. Прочитали нового автора (например, современного китайского фантаста)
2. Загружаете несколько его произведений в PNE
3. PNE размещает его в системе 199+ авторов
4. Показывает, какие 12 домов он охватывает
5. Выявляет синхронии с русскими авторами (если они есть)

СЦЕНАРИЙ 4: Поиск синхронии

1. Вы заметили, что Лем говорит о том же, что Барон
2. Загружаете оба произведения в "Synchronicity Mapper"
3. PNE показывает архетипические соответствия
4. Предлагает одновременное чтение (параллельный анализ)

═══════════════════════════════════════════════════════════════════════════════

ТЕОЛОГИЧЕСКИЙ ФУНДАМЕНТ

Проект основан на учении святых отцов Православной Церкви:

1. ПАЛАМИЗМ (св. Григорий Палама)
   Различие между сущностью (usia) и энергиями (energeiai) Бога
   → Человек не может познать сущность Бога, но может участвовать в Его энергиях
   → Обожение (theosis) — это синергия человеческой воли с Божественной энергией

2. АПОФАТИЗМ (св. Дионисий Ареопагит, св. Максим Исповедник)
   Путь отрицания (via negativa) как единственный путь к трансцендентному
   → "О Боге лучше сказать ничего, чем много неправды"
   → Молчание и тайна ближе к Богу, чем слова

3. СОБОРНОСТЬ (св. Максим Исповедник, св. Сергей Булгаков)
   Церковь как органическое единство в множественности
   → Спасение — это не индивидуальный процесс, а коллективный
   → "Логос становится историей, история становится Логосом"

4. ЭСХАТОЛОГИЯ (св. Иоанн Дамаскин, св. Максим Исповедник)
   История как спираль, восходящая к Богу, а не линейный прогресс
   → Апокалипсис (raскрытие) — это не конец, а трансформация
   → Судьба человечества зависит от выбора каждого человека

5. ЛИТУРГИЧЕСКИЙ РЕАЛИЗМ
   Реальность разделена на видимую (материальная) и невидимую (духовная)
   → Литургия синтезирует обе реальности
   → Роман/сценарий как форма "светской литургии"

═══════════════════════════════════════════════════════════════════════════════

СТРУКТУРА ПРОЕКТА (GIT)

prophetic-narrative-engine/
├── README.md (этот файл)
├── THEOLOGY.md (подробное описание патристической теории)
├── HOUSES.md (описание 12 домов гороскопа как богословских категорий)
├── AUTHORS_DATABASE.csv (199+ авторов с классификацией)
│
├── src/
│   ├── analyzer/
│   │   ├── textual_analyzer.py (модуль 1)
│   │   ├── house_detector.py (определение дома)
│   │   └── archetype_classifier.py (классификация архетипа)
│   │
│   ├── validator/
│   │   ├── theological_validator.py (модуль 2)
│   │   ├── patristic_rules.py (правила святых отцов)
│   │   └── contradiction_checker.py (проверка противоречий)
│   │
│   ├── generator/
│   │   ├── chapter_generator.py (модуль 3)
│   │   ├── prompt_engineering.py (подготовка промптов для LLM)
│   │   └── coherence_checker.py (проверка согласованности)
│   │
│   ├── classifier/
│   │   ├── author_classifier.py (модуль 4)
│   │   └── tier_system.py (система уровней: Master, Tier 2, Tier 3)
│   │
│   ├── synchronicity/
│   │   ├── synchronicity_mapper.py (модуль 5)
│   │   ├── graph_builder.py (построение графов синхронии)
│   │   └── resonance_detector.py (детектор архетипической резонанции)
│   │
│   └── utils/
│       ├── nlp_pipeline.py (NLP для анализа текста)
│       ├── embeddings.py (семантические вложения)
│       └── config.py (конфигурация системы)
│
├── data/
│   ├── 12_houses_definitions.json
│   ├── patristic_authorities.json
│   ├── archetypal_vectors.json
│   ├── 199_authors_classification.json
│   └── synchronicity_map.gexf (граф синхронии в формате GEXF)
│
├── models/
│   ├── house_classifier_model.pkl
│   ├── theological_alignment_model.pkl
│   └── archetypal_resonance_model.pkl
│
├── tests/
│   ├── test_analyzer.py
│   ├── test_validator.py
│   ├── test_generator.py
│   └── test_synchronicity.py
│
├── api/
│   ├── app.py (Flask/FastAPI основное приложение)
│   ├── routes.py (API маршруты)
│   └── schemas.py (Pydantic модели)
│
└── docs/
    ├── API_SPECIFICATION.md
    ├── USAGE_EXAMPLES.md
    ├── THEOLOGICAL_FRAMEWORK.md
    └── ARCHETYPAL_SYSTEM.md

═══════════════════════════════════════════════════════════════════════════════

УСТАНОВКА И БЫСТРЫЙ СТАРТ

ТРЕБОВАНИЯ:
- Python 3.9+
- PyTorch (для моделей NLP)
- Flask или FastAPI
- PostgreSQL (опционально, для сохранения анализов)

УСТАНОВКА:

git clone https://github.com/your-org/prophetic-narrative-engine.git
cd prophetic-narrative-engine
pip install -r requirements.txt

БЫСТРЫЙ СТАРТ:

from pne.analyzer import TextualAnalyzer
from pne.validator import TheologicalValidator

# Анализируем текст
analyzer = TextualAnalyzer()
text = "Герой стоит перед лицом апокалипсиса..."
analysis = analyzer.analyze(text)

# Проверяем на соответствие святым отцам
validator = TheologicalValidator()
validation = validator.validate(text, patristic_authorities=["Palama", "Maximus"])

print(analysis)
print(validation)

ЗАПУСК API:

python api/app.py
# Открыть http://localhost:5000/docs для Swagger UI

═══════════════════════════════════════════════════════════════════════════════

API ENDPOINTS

POST /analyze
Анализирует входящий текст

POST /generate-chapter
Генерирует новую главу на основе параметров

GET /classify-author/{author_name}
Классифицирует автора в системе 199+

POST /map-synchronicity
Строит карту синхронии между авторами/идеями

GET /houses/{house_number}
Получает определение дома и список авторов

GET /patristic-check/{patristic_authority}
Получает список правил конкретного святого отца

POST /batch-analyze
Анализирует множество текстов (для романов, циклов)

═══════════════════════════════════════════════════════════════════════════════

ПРИМЕРЫ ВЫХОДНЫХ ДАННЫХ

ПРИМЕР 1: Анализ текста

INPUT:
{
  "text": "Земля умирает. Последние люди молятся в соборе, зная, что завтра конец. Но старец говорит: 'Это не конец, это начало. Апокалипсис означает раскрытие.'",
  "include_patristic": true
}

OUTPUT:
{
  "analysis": {
    "dominant_house": 8,
    "secondary_houses": [12, 9, 11],
    "theological_quality": "eschatology_as_revelation",
    "archetypal_vector": "Baron_Apocalypse",
    "key_moments": [
      {
        "phrase": "Апокалипсис означает раскрытие",
        "house": 12,
        "patristic_resonance": "Maximus_Confessor_eschatology"
      }
    ],
    "patristic_alignment": {
      "Gregory_Palamas": "✓ Theosis through crisis",
      "Maximus_Confessor": "✓ Apocalypsis as revelation",
      "John_Damascus": "✓ Theandric principle"
    },
    "confidence": 0.96,
    "recommendations": [
      "Усилить момент коллективного спасения (дом 11)",
      "Добавить апофатический слой (молчание старца)"
    ]
  },
  "synchronicities": {
    "Baron_Third_Coming": 0.89,
    "Wachowski_Cloud_Atlas": 0.84,
    "Lem_Fiasco": 0.76
  }
}

ПРИМЕР 2: Генерация главы

INPUT:
{
  "dominant_house": 9,
  "theological_quality": "theosis_through_knowledge",
  "archetypal_vector": "Baron_Apocalypse",
  "scene_type": "meditation",
  "word_count": 800,
  "language": "Russian",
  "context": "After the death of the protagonist, the community must understand what happened"
}

OUTPUT:
{
  "generated_chapter": "Монастырь Святого Максима. Три дня после смерти пророка...",
  "metadata": {
    "dominant_house": 9,
    "secondary_houses": [8, 12, 3],
    "archetypal_resonances": ["Максим_Исповедник", "Паламизм", "Апофатизм"],
    "patristic_authorities_invoked": ["Gregory_Palamas", "Maximus_Confessor"],
    "word_count": 802,
    "estimated_reading_time_minutes": 5
  },
  "theological_layers": [
    {
      "timestamp": 150,
      "layer": "Knowledge as theosis",
      "patristic_reference": "Maximus_Confessor_epistemology"
    },
    {
      "timestamp": 450,
      "layer": "Community consolation",
      "patristic_reference": "Sobornost_principle"
    }
  ]
}

═══════════════════════════════════════════════════════════════════════════════

ОГРАНИЧЕНИЯ И ЭТИКА

ОГРАНИЧЕНИЯ:

1. Система не может генерировать тексты, противоречащие учению святых отцов
2. Проверка паристическая выполняется на основе 5 основных авторитетов (Палама, Максим, Дионисий, Дамаскин, Булгаков)
3. Синхронии вычисляются на основе архетипических паттернов, а не точных совпадений слов
4. Генерируемые главы требуют человеческого редактирования (LLM может допустить ошибки)

ЭТИКА:

- Проект уважает авторское право всех 199+ авторов
- Система используется только для анализа и творческого вдохновения, не для плагиата
- Все данные о авторах публичны и основаны на открытых источниках
- Проект не претендует на окончательное суждение о богословии (это привилегия Церкви)

═══════════════════════════════════════════════════════════════════════════════

КОНТРИБЬЮТИНГ

Система открыта для расширения:

- Добавить новых авторов в базу данных (с источниками и классификацией)
- Добавить новых святых отцов и их правила (с цитатами)
- Улучшить модели детекции домов и архетипов
- Предложить новые "векторы" (помимо Baron, Divov, Panov, Wachowski)
- Написать новые модули для анализа (например, социально-политическая система)

═══════════════════════════════════════════════════════════════════════════════

ЛИЦЕНЗИЯ

MIT License (с условием: коммерческое использование требует согласия)

═══════════════════════════════════════════════════════════════════════════════

КОНТАКТЫ И РЕСУРСЫ

GitHub: https://github.com/your-org/prophetic-narrative-engine
Documentation: https://pne-docs.example.com
Discord Community: https://discord.gg/pne

ОСНОВНЫЕ ИСТОЧНИКИ:

Теология:
- Gregory Palamas: "Triads for the Defense of Those Who Practice Sacred Quietude"
- Maximus Confessor: "Ambigua"
- John of Damascus: "An Exact Exposition of the Orthodox Faith"
- Sergei Bulgakov: "The Orthodox Church"
- Nicolas Berdyaev: "Freedom and Spirit"

Фантастика:
- Alexey Baron: "Third Coming" (Третье пришествие)
- Sergey Divov: "Multifaceted Chaos" (Многоликий хаос)
- Vadim Panov: "Black Ops" series
- The Wachowskis: "Cloud Atlas"

Синхронистика:
- Wolfgang Pauli & Carl Jung: "The Interpretation of Nature and the Psyche"
- Arthur Koestler: "The Roots of Coincidence"

═══════════════════════════════════════════════════════════════════════════════

ВЕРСИЯ: 1.0 (Beta)
ПОСЛЕДНЕЕ ОБНОВЛЕНИЕ: 19 января 2026
СТАТУС: В АКТИВНОЙ РАЗРАБОТКЕ

"In the beginning was the Word, and the Word was with God, and the Word was God."
— John 1:1

"The whole cosmos is a Temple. Every stone, every tree, every thing is a hymn to the Creator."
— St. Maximus the Confessor

═══════════════════════════════════════════════════════════════════════════════