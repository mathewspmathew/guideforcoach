import os
from src.agents.graph import build_app
import webbrowser
from pathlib import Path
from datetime import datetime
import re
from resultfilecreate import create_file

def main():
    # here it builds the Agent System
    app = build_app()

    target = input("Enter the player you want to replace (e.g., 'Rodri'): ")

    inputs = {"target_player": target}

    print(f"\n🚀 STARTING AGENT WORKFLOW FOR: {target}")

    # Run the Graph
    # We iterate through the stream to see steps happening in real-time
    for output in app.stream(inputs):
        for key, value in output.items():
            print(f"✅ Finished Node: {key}")

    # final step: Get Final State
    # Rerunning just to fetch the final state object for printing
    # In production, we can use .invoke() for avoiding streaming

    final_state = app.invoke(inputs)
    print("\n\n" + "="*40)
    print("       FINAL SCOUTING REPORT       ")
    print("="*40)
    print(final_state['final_report'])
    final_report = final_state["final_report"]
    target_player = final_state["target_player"]
    create_file(final_result=final_report, target_player=target_player)


if __name__ == "__main__":
    main()