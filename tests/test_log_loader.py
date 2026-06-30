from app.services.ingestion.log_loader import LogLoaderService


def main():
    loader = LogLoaderService()

    documents = loader.load("sample.log")

    print(documents[0].page_content)
    print(documents[0].metadata)


if __name__ == "__main__":
    main()