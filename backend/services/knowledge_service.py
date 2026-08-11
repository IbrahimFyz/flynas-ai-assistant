from pathlib import Path


def load_knowledge():
    data_path = Path(__file__).parent.parent / "data" / "flynas_faq.txt"

    with open(data_path, "r", encoding="utf-8") as file:
        knowledge = file.read()

    return knowledge


def split_knowledge(knowledge):
    chunks = knowledge.split("\n\n")
    return chunks


def get_knowledge_chunks():
    knowledge = load_knowledge()
    chunks = split_knowledge(knowledge)

    return chunks


if __name__ == "__main__":
    knowledge = load_knowledge()
    chunks = split_knowledge(knowledge)

    for chunk in chunks:
        print("----- CHUNK -----")
        print(chunk)