from app.services.ingestion.text_loader import TextLoaderService


def main():

    loader = TextLoaderService()

    documents = loader.load("sample.txt")

    print(f"Documents Loaded: {len(documents)}")

    print("\nContent:\n")

    print(documents[0].page_content)

    print("\nMetadata:\n")

    print(documents[0].metadata)


if __name__ == "__main__":
    main()