# Remarka — backend platform

Рабочая реализация архитектуры: очереди, векторное хранилище, подключаемый AI-провайдер, RSS-новости, сборка образов.

[![CI](https://github.com/ivanm696/GitHub-Actions/actions/workflows/ci.yml/badge.svg)](https://github.com/ivanm696/GitHub-Actions/actions/workflows/ci.yml)

## Статус реализации

| Компонент | Статус | Где |
|---|---|---|
| Очереди: Celery + Redis | ✅ Работает | `apps/api/app/core/celery_app.py`, `app/tasks/` |
| Хранилище артефактов (S3/R2) | ✅ Работает | `apps/api/app/core/storage.py` |
| Векторное хранилище (Qdrant) | ✅ Работает | `apps/api/app/rag/vector_store.py` |
| AI-провайдер (подключаемый) | ✅ Работает | `apps/api/app/ai/provider.py` — Anthropic / OpenAI / локальный |
| Новости: RSS + robots.txt | ✅ Работает | `apps/api/app/news/rss.py` |
| Новости: NewsAPI | 🔜 Заглушка (phase 2) | `fetch_from_newsapi()` в `rss.py` |
| Образы: Packer + QEMU + cloud-init | ✅ Конфиг готов | `infra/packer/` |
| pgvector (альтернатива Qdrant) | 🔜 Не реализовано | — |
| Buildroot/Yocto (кастомные ISO) | 🔜 Не реализовано | — |
| CI/CD: GitHub Actions | ✅ Работает | `.github/workflows/ci.yml` |

## Быстрый старт

```bash
git clone https://github.com/ivanm696/GitHub-Actions.git remarka
cd remarka
cp apps/api/.env.example apps/api/.env
# впиши свой ANTHROPIC_API_KEY или OPENAI_API_KEY в apps/api/.env

docker compose up -d
```

Проверить, что всё живо:
```bash
curl http://localhost:8000/health
curl http://localhost:8000/health/ready
```

## Архитектура

```
remarka/
├── apps/api/                  # FastAPI backend
│   ├── app/
│   │   ├── core/
│   │   │   ├── config.py      # pydantic-settings, всё через .env
│   │   │   ├── celery_app.py  # Celery + Redis broker/backend
│   │   │   └── storage.py     # S3/R2 клиент (boto3, endpoint настраивается)
│   │   ├── ai/
│   │   │   └── provider.py    # AIProvider ABC + Anthropic/OpenAI/Local реализации
│   │   ├── rag/
│   │   │   └── vector_store.py # Qdrant — upsert/search
│   │   ├── news/
│   │   │   └── rss.py         # RSS-фетчер, проверяет robots.txt перед запросом
│   │   ├── tasks/              # Celery-задачи (news_tasks, ai_tasks)
│   │   └── main.py             # FastAPI роуты
│   ├── tests/                  # pytest — реально проверяются в CI
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── infra/packer/
│   ├── remarka-base.pkr.hcl    # QEMU builder + cloud-init
│   └── cloud-init/
├── docker-compose.yml          # api, worker, beat, redis, postgres, qdrant, minio
└── .github/workflows/ci.yml    # 4 джоба: тесты, docker build, compose validate, packer validate
```

## Переключение AI-провайдера

Одна переменная окружения — весь остальной код не меняется:

```bash
AI_PROVIDER=anthropic   # или: openai | local
```

```python
from app.ai.provider import get_ai_provider

provider = get_ai_provider()
reply = await provider.complete("Напиши хайку про очереди Celery")
```

## S3 vs R2

По умолчанию — AWS S3. Для Cloudflare R2 просто заполни:
```env
S3_ENDPOINT_URL=https://<account_id>.r2.cloudflarestorage.com
```
API полностью совместим (используется тот же `boto3`).

## Локальная разработка без Docker

```bash
cd apps/api
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Для Celery worker понадобится локальный Redis:
```bash
celery -A app.core.celery_app worker --loglevel=info
```

## Тесты

```bash
cd apps/api
python -m pytest tests/ -v
```

7 тестов, все проходят в CI при каждом push.

## Что дальше (не реализовано)

- Интеграция NewsAPI как второго источника (структура готова — `fetch_from_newsapi()`)
- pgvector как альтернатива Qdrant
- Buildroot/Yocto для кастомных встраиваемых образов (Packer покрывает облачные ISO/IMG)
- Модели БД для персистентности новостей/документов (сейчас RSS fetch возвращает данные, но не сохраняет)

## License

MIT
