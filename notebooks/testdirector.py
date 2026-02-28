from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
import numpy as np

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0,
)

print("\n👔 DIRECTOR: Writing final report...")

# Define the Prompt
template = """You are the Sporting Director of a top football club.

GOAL: Write a scouting report recommending a replacement for: {target}

DATA FROM SCOUT (Statistical Match):
{stats}

DATA FROM RESEARCHER (Market/News):
{market}

INSTRUCTIONS:
1. Compare the options based on Stats AND Market feasibility.
2. Be professional, concise, and decisive.
3. Recommend ONE primary target and ONE backup.

FORMAT:
## Executive Summary
## Player Analysis
## Final Recommendation
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | llm

market_research = """

🔎 RESEARCHER: Checking market data for 4 players...
{'market_research': "--- Loïs Openda (RB Leipzig) ---\n# #20 Loïs **Openda**. German Super Cup winner 1. Belgian Super Cup Winner 1. Last update: Dec 23, 2025. ## Injury history. Injury history, suspensions and absences are based on a variety of media reports and are researched with the greatest of care. If you should notice an error regardless, please use the correction form. | Season | Injury | from | until | Days | Games missed |. | 24/25 | Knock | Oct 27, 2024 | Nov 1, 2024 | 6 days | RB Leipzig1 |. | Season | Days | Injuries | Games missed |. | 24/25 | 6 days | 1 | 1 |. Sie haben erfolgreich Ihre Einwilligung in die Nutzung von Transfermarkt mit Tracking und Cookies widerrufen. Sie können sich jetzt zwischen dem Contentpass-Abo und der Nutzung mit personalisierter Werbung, Cookies und Tracking entscheiden.\nLois Openda. Forward (Juventus). Age: 26 (16.02.2000). Market value: €37.4m. On loan from: RB Leipzig (Until: 30.06.2026). Juventus. SummaryTransfersInjury\n\n--- Patrick Cutrone (Como) ---\nPatrick Cutrone. Forward (Monza). Age: 28 (03.01.1998). Market value: €4.5m. On loan from: Como (Until: 30.06.2026). Monza. SummaryNewsTransfersInjury History.\nTransfermarkt estimates the forward's current market value to be €6.00m, and he has also attracted interest from Napoli. 179d ago. Shortlisted CFs. Parma.\n\n--- Michail Antonio (West Ham) ---\nMarket value: €655k. West Ham U21 · SummaryNewsTransfersInjury History. Last Matches. Premier League 2 (England). England. 23.02.26. PL2. West Ham U21.\nInjury history ; 24/25, Broken leg, 177 days, West Ham United · Jamaica 31 ; 23/24, Knee injury, 87 days, West Ham United · Jamaica 18.\n\n--- Benjamin Šeško (RB Leipzig) ---\nBenjamin Sesko's current transfer value is between €67.2M and €82.1M. His last transfer was from RB Leipzig to Man Utd in 2025. Man Utd paid RB Leipzig €76.5M\nRB Leipzig have put a price tag of €80m on Slovenian striker Benjamin Šeško with Newcastle United among the clubs monitoring the situation.\n\n"}
"""
players = [{'name': 'Loïs Openda', 'squad': 'RB Leipzig', 'age': 24, 'similarity': np.float64(87.4)},
           {'name': 'Patrick Cutrone', 'squad': 'Como', 'age': 26, 'similarity': np.float64(86.3)},
           {'name': 'Michail Antonio', 'squad': 'West Ham', 'age': 34, 'similarity': np.float64(86.1)},
           {'name': 'Benjamin Šeško', 'squad': 'RB Leipzig', 'age': 21, 'similarity': np.float64(85.6)}]
# Run the LLM
response = chain.invoke({
  "target": "Matthis Abline",
  "stats": players,
  "market": market_research
})


print(response.content)
