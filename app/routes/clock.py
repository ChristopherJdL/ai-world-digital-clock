"""Clock rendering endpoint."""
from __future__ import annotations
import traceback 
from flask import Blueprint, Response, current_app, jsonify, make_response, request

clock_bp = Blueprint("clock", __name__)


@clock_bp.route("/clock/render")
def clock_render() -> Response:
    model_id = request.args.get("model", "").strip()
    allowed_models = current_app.config.get("ALLOWED_MODEL_IDS", set())
    if model_id not in allowed_models:
        return make_response(jsonify({"error": "Unsupported model"}), 400)

    provider = current_app.config.get("CLOCK_PROVIDER")
    if provider is None:
        return make_response(jsonify({"error": "Server missing Mammouth API key"}), 500)

    current_time = request.args.get("current_time", "").strip()
    lcd_mode_enabled = request.cookies.get("lcd_mode") == "1"
    base_prompt = current_app.config.get("CLOCK_PROMPT_TEMPLATE", "")
    lcd_prompt = current_app.config.get("LCD_CLOCK_PROMPT_TEMPLATE", "")
    prompt_template = lcd_prompt if lcd_mode_enabled else base_prompt

    try:
        html = provider.render_clock(
            model_id,
            current_time=current_time,
            prompt_template=prompt_template,
        )
    except Exception:  # noqa: BLE001
        current_app.logger.exception("Clock render failed for model %s", model_id)
        return make_response(jsonify({"error": "Unable to render clock: " + traceback.format_exc()}), 502)

    response = make_response(html)
    response.headers["Content-Type"] = "text/html; charset=utf-8"
    response.headers["Cache-Control"] = "no-store"
    return response
