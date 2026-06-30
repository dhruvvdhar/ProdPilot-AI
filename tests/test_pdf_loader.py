from app.services.ingestion.pdf_loader import PDFLoaderService


def main():

    loader = PDFLoaderService()

    documents = loader.load("sample.pdf")

    print(f"Pages Loaded: {len(documents)}")

    print("\nFirst Page Content:\n")

    print(documents[0].page_content[:500])

    print("\nMetadata:\n")

    print(documents[0].metadata)


if __name__ == "__main__":
    main()