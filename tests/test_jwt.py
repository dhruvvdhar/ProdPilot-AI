from app.services.auth.jwt_service import JWTService


jwt_service = JWTService()


def test_jwt():

    token = jwt_service.create_access_token(
        subject="dhruv@example.com"
    )

    payload = jwt_service.verify_access_token(
        token
    )

    assert payload["sub"] == "dhruv@example.com"