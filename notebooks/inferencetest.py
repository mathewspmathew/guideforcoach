import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.model import SimilarityEngine
from src.config import DB_PATH

# print(DB_PATH)

ml_engine = SimilarityEngine()

result = ml_engine.inference("Matthis Abline")

# if "error" in result:
#     # Fallback if player not found
#     print ("error")

# # 2. Return the list of matches to the State
# print (result)
# if not os.path.exists(DB_PATH):
#     print('yes')
print(result)