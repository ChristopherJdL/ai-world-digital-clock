"""Application entry point."""
from __future__ import annotations

import os

from app import create_app

app = create_app()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 5003)))
