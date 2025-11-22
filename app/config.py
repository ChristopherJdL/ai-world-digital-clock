"""Application configuration constants."""
from __future__ import annotations

import os
from typing import Dict, List

APP_TITLE = "AI World Digital Clocks"
MAMMOUTH_BASE_URL = os.getenv("MAMMOUTH_BASE_URL", "https://api.mammouth.ai/v1")
MAMMOUTH_API_KEY = os.getenv("MAMMOUTH_API_KEY")
REFRESH_INTERVAL_MS = 60_000

CLOCK_MODELS: List[Dict[str, str]] = [
    {
        "id": "grok-4-fast",
        "label": "Grok 4 Fast",
        "logo": "grok-4-fast.png",
        "provider": "xAI",
    },
    {
        "id": "deepseek-v3.2-exp",
        "label": "DeepSeek V3.2 Experimental",
        "logo": "deepseek-v3-2-exp.png",
        "provider": "DeepSeek",
    },
    {
        "id": "mistral-medium-3.1",
        "label": "Mistral Medium 3.1",
        "logo": "mistral-medium.png",
        "provider": "Mistral AI",
    },
    {
        "id": "gemini-2.5-flash",
        "label": "Gemini 2.5 Flash",
        "logo": "gemini-2-5-flash.png",
        "provider": "Google",
    },
    {
        "id": "llama-4-scout",
        "label": "Llama 4 Scout",
        "logo": "llama-4-scout.png",
        "provider": "Meta",
    },
    {
        "id": "claude-3-5-haiku-20241022",
        "label": "Claude 3.5 Haiku",
        "logo": "claude-3-5-haiku.png",
        "provider": "Anthropic",
    },
]

ALLOWED_MODEL_IDS = {model["id"] for model in CLOCK_MODELS}

SYSTEM_PROMPT = (
    "You render futuristic digital clock components strictly as standalone HTML and CSS snippets. "
    "You MUST NOT include backticks, explanations, markdown code fences, or JavaScript."
    "All clocks must be responsive, centered, and fill the container elegantly with a black background."
)

CLOCK_PROMPT_TEMPLATE = (
    "Client reports `{current_time}` as the current local time. "
    "Create a single digital clock that displays HH:MM:SS with clearly ticking seconds. "
    "Load the Digital-7 Mono font using <link href=\"https://fonts.cdnfonts.com/css/digital-7-mono\" rel=\"stylesheet\"> "
    "and render the digits using that font at a bold, oversized scale. "
    "Use HTML and CSS for layout and styling, but you may add a small inline <script> if needed to advance the seconds accurately. "
    "Choose a vivid neon-like color for the digits that is not turquoise, keep the background strictly #000, and keep the composition centered, responsive, and contained so it fits inside any iframe without overflowing. "
    "Return only the clock's HTML plus inline <style> rules scoped to the component."
)

LCD_CLOCK_PROMPT_TEMPLATE = (
    "Client reports `{current_time}` as the current local time. "
    "Create a single HH:MM:SS digital clock styled like a classic reflective LCD display. "
    "Use the Digital-7 Mono font via <link href=\"https://fonts.cdnfonts.com/css/digital-7-mono\" rel=\"stylesheet\"> "
    "and keep all digits crisp, high-contrast, and aligned to a tight grid. "
    "Render the background with a subtle greenish-gray (pale olive/grayish-beige) tint reminiscent of passive LCD panels, "
    "and use deep charcoal digits with minimal neon glow so it feels like ambient light reflecting on LCD film. "
    "You may include a small inline <script> to advance the seconds accurately, but keep everything iframe friendly and centered. "
    "Return only the clock's HTML plus inline <style> rules scoped to the component."
)
