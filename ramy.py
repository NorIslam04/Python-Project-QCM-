from datetime import datetime
import json
import csv
from display import clear_console, display_header, display_message

def get_question_count(category: str) -> int:
    try:
        with open(f"QST/{category}.json", "r", encoding="utf-8") as f:
            questions = json.load(f)
            return len(questions)
    except:
        return 5  # fallback to default

def view_scores(username):
    clear_console()
    display_header("Historique des Scores")

    scores_found = False
    try:
        with open("resultats.csv", mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            j=0
            for i, row in enumerate(reader):
                if row["nom"] == username:
                    scores_found = True
                    j+=1
                    question_count = get_question_count(row['categorie'])
                    print(f"\033[92m{j}.\033[0m categorie: \033[92m{row['categorie']}\033[0m"
                          f" - Score: \033[92m({row['score']}/{question_count})\033[0m"
                          f" - Date: \033[92m{row['date']}\033[0m")

        if not scores_found:
            display_message("Aucun historique trouvé.", "info")
    except FileNotFoundError:
        display_message("Le fichier resultats.csv est introuvable.", "error")
    except KeyError:
        display_message("Le fichier resultats.csv ne contient pas les colonnes attendues.", "error")


def save_user_responses(username: str, category: str, responses: list, questions: list) -> None:
    # Calculer le score
    score = sum(1 for i, response in enumerate(responses) if response is not None and response == questions[i]["correctResponse"])

    # Prépare les données à sauvegarder
    user_data = {
        "username": username,
        "category": category,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "score": score,
        "questions": []
    }

    # Pour chaque question et réponse
    for i, (question, response) in enumerate(zip(questions, responses)):
        q_data = {
            "question": question["qst"],
            "user_response": "Pas de réponse" if response is None else question["arrayResponse"][response],
            "correct_response": question["arrayResponse"][question["correctResponse"]]
        }
        user_data["questions"].append(q_data)

    try:
        # Charge les données existantes
        existing_data = []
        try:
            with open("reponse_user.json", "r", encoding="utf-8") as f:
                existing_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_data = []

        # Ajoute les nouvelles données
        if not isinstance(existing_data, list):
            existing_data = []
        existing_data.append(user_data)

        # Sauvegarde dans le fichier
        with open("reponse_user.json", "w", encoding="utf-8") as f:
            json.dump(existing_data, f, indent=4, ensure_ascii=False)

    except Exception as e:
        display_message(f"Erreur lors de la sauvegarde des réponses: {e}", "error")