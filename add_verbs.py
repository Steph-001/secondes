import json
import os

FILE_PATH = "static/data/irregular-verbs.json"

def load_verbs():
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_verbs(verbs):
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(verbs, f, indent=2, ensure_ascii=False)

def main():
    verbs = load_verbs()

    print("Enter irregular verbs (leave base form empty to stop):\n")
    while True:
        base = input("Base form: ").strip()
        if not base:
            break
        past = input("Past tense: ").strip()
        participle = input("Past participle: ").strip()

        verbs.append({
            "base": base,
            "past": past,
            "participle": participle
        })
        print(f"✔ Added: {base} – {past} – {participle}\n")

    save_verbs(verbs)
    print(f"\n✅ {len(verbs)} total verbs saved to {FILE_PATH}")

if __name__ == "__main__":
    main()

