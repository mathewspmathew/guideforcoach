import webbrowser
from pathlib import Path
from datetime import datetime
import re

def create_file(final_result, target_player):
  # return ""
# final_report = final_state["final_report"]
# target_player = final_state["target_player"]  # which is coming from state

# Clean the player name for filename
  safe_name = re.sub(r"[^\w\s-]", "", target_player).strip().replace(" ", "_")

  timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

  # Create reports folder
  reports_dir = Path("reports")
  reports_dir.mkdir(exist_ok=True)

  # Buildng the file name
  file_name = f"{safe_name}_{timestamp}.md"
  file_path = reports_dir / file_name

  with open(file_path, "w", encoding="utf-8") as f:
      f.write(final_result)

  print(f"\n📄 Report saved to {file_path}")

  webbrowser.open(file_path.resolve().as_uri())