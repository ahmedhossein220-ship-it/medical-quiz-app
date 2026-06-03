import random
import json
import os
from datetime import datetime

def run_quiz():
    # 1. Fragen aus der JSON-Datei laden
    file_path = 'questions.json'
    stats_path = 'quiz_statistik.json'
    
    if not os.path.exists(file_path):
        print(f"Fehler: Die Datei '{file_path}' wurde nicht gefunden!")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        all_questions = json.load(f)

    current_round = all_questions.copy()
    total_questions_pool = len(all_questions)
    round_no = 1
    streak = 0
    
    # Speicher für die Statistik der ersten Runde
    round1_errors = []

    print("="*80)
    print("      CVS ULTIMATE TRAINER - JSON VERSION")
    print("="*80)
    print(f"{total_questions_pool} Fragen geladen. Viel Erfolg!")
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

            if ans == item["a"].upper():
                streak += 1
                print(f"✅ KORREKT! | Streak: {streak}")
            else:
                streak = 0
                print(f"❌ FALSCH! Die Uni-Lösung ist: {item['a']}")
                wrong_pool.append(item)
                
                # In der ersten Runde sammeln wir die Fehler für die Statistik
                if round_no == 1:
                    round1_errors.append({
                        "question": item['q'],
                        "options": item['o'],
                        "correct_answer": item['a']
                    })

        # Nach der allerersten Runde speichern wir das Ergebnis sofort ab
        if round_no == 1:
            fehler_anzahl = len(round1_errors)
            korrekt_anzahl = total_questions_pool - fehler_anzahl
            erfolgsquote = (korrekt_anzahl / total_questions_pool) * 100
            
            statistik_eintrag = {
                "zeitstempel": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "gesamt_fragen": total_questions_pool,
                "richtig_in_runde_1": korrekt_anzahl,
                "fehler_in_runde_1": fehler_anzahl,
                "erfolgsquote_runde_1_prozent": round(erfolgsquote, 2),
                "falsche_fragen_liste": round1_errors
            }
            
            # Bestehende Statistiken laden oder neue Liste erstellen
            if os.path.exists(stats_path):
                try:
                    with open(stats_path, 'r', encoding='utf-8') as sf:
                        verlauf = json.load(sf)
                        if not isinstance(verlauf, list):
                            verlauf = []
                except json.JSONDecodeError:
                    verlauf = []
            else:
                verlauf = []
                
            verlauf.append(statistik_eintrag)
            
            with open(stats_path, 'w', encoding='utf-8') as sf:
                json.dump(verlauf, sf, ensure_ascii=False, indent=4)
                
            print("\n" + "-"*40)
            print(f"📊 RUNDE 1 BEENDET – Statistik gespeichert in '{stats_path}'!")
            print(f"Quote: {round(erfolgsquote, 2)}% | Richtig: {korrekt_anzahl} | Fehler: {fehler_anzahl}")
            print("-"*40)

        if not wrong_pool:
            print("\n" + "#"*80)
            print("HERZLICHEN GLÜCKWUNSCH! Du hast alle Fragen gemeistert!")
            print("#"*80)
            break
        else:
            print(f"\nEnde Runde {round_no}. {len(wrong_pool)} Fehler werden wiederholt.")
            current_round = wrong_pool
            round_no += 1
            input("Drücke Enter für die nächste Runde...")

if __name__ == "__main__":
    run_quiz()
