from app.services.ocr.paddle_ocr_service import PaddleOCRService


def main():

    ocr = PaddleOCRService()

    text = ocr.extract_text("sample_image.png")

    print(text)


if __name__ == "__main__":
    main()