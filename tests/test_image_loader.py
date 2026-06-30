from app.services.ingestion.image_loader import ImageLoaderService
from app.services.ocr.paddle_ocr_service import PaddleOCRService


def main():

    ocr_service = PaddleOCRService()

    loader = ImageLoaderService(
        ocr_service=ocr_service
    )

    documents = loader.load("sample_image.png")

    print("\nPage Content:\n")
    print(documents[0].page_content)

    print("\nMetadata:\n")
    print(documents[0].metadata)


if __name__ == "__main__":
    main()