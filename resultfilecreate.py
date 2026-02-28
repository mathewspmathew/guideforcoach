import webbrowser
from pathlib import Path
from datetime import datetime
import re

def create_file(final_result, target_player):
  # return ""
# final_report = final_state["final_report"]
# target_player = final_state["target_player"]  # coming from state

# 1️⃣ Clean the player name (safe for filename)
  safe_name = re.sub(r"[^\w\s-]", "", target_player).strip().replace(" ", "_")

  # 2️⃣ Create timestamp
  timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

  # 3️⃣ Create reports folder
  reports_dir = Path("reports")
  reports_dir.mkdir(exist_ok=True)

  # 4️⃣ Build file name
  file_name = f"{safe_name}_{timestamp}.md"
  file_path = reports_dir / file_name

  # 5️⃣ Write file
  with open(file_path, "w", encoding="utf-8") as f:
      f.write(final_result)

  print(f"\n📄 Report saved to {file_path}")

  # 6️⃣ Auto open in browser
  webbrowser.open(file_path.resolve().as_uri())