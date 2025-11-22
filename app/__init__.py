"""Flask application factory."""
from __future__ import annotations

from flask import Flask

from .config import (
    ALLOWED_MODEL_IDS,
    APP_TITLE,
    CLOCK_MODELS,
    CLOCK_PROMPT_TEMPLATE,
    MAMMOUTH_API_KEY,
    MAMMOUTH_BASE_URL,
    REFRESH_INTERVAL_MS,
    SYSTEM_PROMPT,
)
from .providers import MammouthClockProvider
from .routes import clock_bp, home_bp


def create_app() -> Flask:
    app = Flask(__name__)

    app.config["APP_TITLE"] = APP_TITLE
    app.config["REFRESH_INTERVAL_MS"] = REFRESH_INTERVAL_MS
    app.config["CLOCK_MODELS"] = CLOCK_MODELS
    app.config["ALLOWED_MODEL_IDS"] = ALLOWED_MODEL_IDS

    provider = None
    if MAMMOUTH_API_KEY:
        provider = MammouthClockProvider(
            api_key=MAMMOUTH_API_KEY,
            base_url=MAMMOUTH_BASE_URL,
            system_prompt=SYSTEM_PROMPT,
            clock_prompt_template=CLOCK_PROMPT_TEMPLATE,
        )
    app.config["CLOCK_PROVIDER"] = provider

    app.register_blueprint(clock_bp)
    app.register_blueprint(home_bp)

    return app
