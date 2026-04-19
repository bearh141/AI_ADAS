import datetime
from pathlib import Path

CHANGELOG_PATH = Path("CHANGELOG.md")

def add_entry(version: str, description: str):
    print("[INFO] Updating CHANGELOG.md ...")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"""
## 🏷️ Version {version} - {timestamp}

{description.strip()}

---
"""
    if not CHANGELOG_PATH.exists():
        CHANGELOG_PATH.write_text("# 📜 CHANGELOG\n\n", encoding="utf-8")

    with open(CHANGELOG_PATH, "a", encoding="utf-8") as f:
        f.write(entry)

    print(f"[OK] Added changelog entry for version {version}.")

if __name__ == "__main__":
    # Ví dụ sử dụng
    add_entry("0.0.0", "Initial version of AI_ADAS server with lane detection and config.yaml support.")
