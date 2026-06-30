from app.services.vectorstore.chroma_service import ChromaService


def main():
    chroma = ChromaService(
        ChromaService(
        collection_name="production_assistant_test"
        )
    )

    print("Collection Name:")
    print(chroma.collection.name)


if __name__ == "__main__":
    main()