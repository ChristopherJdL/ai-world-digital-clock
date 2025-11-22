"""Home page endpoint."""
from __future__ import annotations

from flask import Blueprint, Response, current_app, render_template, url_for

home_bp = Blueprint("home", __name__)


@home_bp.route("/")
@home_bp.route("/home")
def home() -> Response:
    app_title = current_app.config.get("APP_TITLE", "AI World Digital Clocks")
    refresh_interval = current_app.config.get("REFRESH_INTERVAL_MS", 60_000)
    clock_models = current_app.config.get("CLOCK_MODELS", [])

    app_config = {
        "title": app_title,
        "refreshInterval": refresh_interval,
        "models": [
            {
                "id": model["id"],
                "label": model["label"],
                "provider": model.get("provider", ""),
                "logo": url_for("static", filename=f"images/{model['logo']}")
                if model.get("logo")
                else "",
            }
            for model in clock_models
        ],
    }

    return render_template("home.html", app_title=app_title, app_config=app_config)
