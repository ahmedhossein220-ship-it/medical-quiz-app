import random
import json
import os

def run_quiz():
    # 1. Fragen aus der JSON-Datei laden
    file_path = 'blood.json'
    
    if not os.path.exists(file_path):
        print(f"Fehler: Die Datei '{file_path}' wurde nicht gefunden!")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        all_questions = json.load(f)

    current_round = all_questions.copy()
    round_no = 1
    streak = 0

    print("="*80)
    print("      BLOOD ULTIMATE TRAINER - JSON VERSION")
    print("="*80)
    print(f"{len(all_questions)} Fragen geladen. Viel Erfolg!")
    print("Tippe 'exit' zum Beenden.\n")

    while current_round:
        print(f"\n>>> RUNDE {round_no} ({len(current_round)} offene Fragen)")
        random.shuffle(current_round)
        wrong_pool = []

        for i, item in enumerate(current_round):
            print(f"\n[{i+1}/{len(current_round)}] {item['q']}")
            for opt in item["o"]:
                print(opt)
            
            ans = input("\nAntwort (A, B, C, D): ").strip().upper()
            
            if ans == 'EXIT':
                print("Programm beendet.")
                return

            if ans.upper() == item["a"].upper():
                streak += 1
                print(f"✅ KORREKT! | Streak: {streak}")
            else:
                streak = 0
                print(f"❌ FALSCH! Die Uni-Lösung ist: {item['a']}")
                wrong_pool.append(item)

        if not wrong_pool:
            print("\n" + "#"*80)
            print("HERZLICHEN GLÜCKWUNSCH Niggi! Du hast alle Fragen gemeistert!")
            print("#"*80)
            break
        else:
            print(f"\nEnde Runde Baka {round_no}. {len(wrong_pool)} Fehler werden wiederholt.")
            current_round = wrong_pool
            round_no += 1
            input("Drücke Enter für die nächste Runde...")

if __name__ == "__main__":
    run_quiz()
