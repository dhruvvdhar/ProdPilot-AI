from app.services.ingestion.ingestion_service import (
    IngestionService,
)


def main():

    ingestion = IngestionService()

    # ingestion.clear_database()

    ingestion.ingest_directory(
        "documents"
    )


if __name__ == "__main__":
    main()