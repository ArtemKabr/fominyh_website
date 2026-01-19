# backend/app/services/services_marketing.py
# Назначение: загрузка маркетинговых описаний услуг из JSON

import json
from pathlib import Path


DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "services_marketing.json"


def load_services_marketing() -> list[dict]:
    """Загрузить маркетинговые описания услуг из JSON."""  # (я добавил)
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
