from app.services.rag.rag_service import RAGService


def main():

    rag = RAGService()

    while True:

        question = input("\nYou: ")

        if question.lower() == "exit":
            break

        answer = rag.ask(question)

        print(f"\nAssistant:\n{answer}")


if __name__ == "__main__":
    main()