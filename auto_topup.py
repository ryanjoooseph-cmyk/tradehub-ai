# project/src/auto_topup.py
import os
MODE = os.getenv("AUTO_TOPUP", "off").lower()
if MODE not in ("on", "enabled", "1", "true"):
    print("[auto_topup] noop (disabled).")
else:
    # Hook your real top-up logic later.
    print("[auto_topup] placeholder — no action taken.")