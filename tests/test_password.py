from app.services.auth.password import PasswordService


password_service = PasswordService()


def test_password_hashing():

    password = "Dhruv123"

    hashed = password_service.hash_password(password)

    assert password != hashed

    assert password_service.verify_password(
        password,
        hashed,
    )

    assert not password_service.verify_password(
        "WrongPassword",
        hashed,
    )