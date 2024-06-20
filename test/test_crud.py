# import pytest
# from httpx import AsyncClient
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from app.main import app
# from app.database import get_db, Base
# from fastapi.testclient import TestClient

# SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# @pytest.fixture(scope="module")
# def test_db():
#     Base.metadata.create_all(bind=engine)
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#         Base.metadata.drop_all(bind=engine)


# @pytest.fixture(scope="module")
# def client():
#     client = TestClient(app)
#     yield client


# @pytest.fixture(scope="module")
# def async_client():
#     async with AsyncClient(app=app, base_url="http://test") as client:
#         yield client


# def override_get_db():
#     try:
#         db = TestingSessionLocal()
#         yield db
#     finally:
#         db.close()


# app.dependency_overrides[get_db] = override_get_db


# @pytest.mark.asyncio
# async def test_create_short_url(async_client, test_db):
#     response = await async_client.post(
#         "/url/shorten", json={"original_url": "http://example.com"}
#     )
#     assert response.status_code == 200
#     data = response.json()
#     assert "id" in data
#     assert data["original_url"] == "http://example.com"
#     assert "short_url" in data


# @pytest.mark.asyncio
# async def test_redirect_url(async_client, test_db):
#     response = await async_client.post(
#         "/url/shorten", json={"original_url": "http://example.com"}
#     )
#     assert response.status_code == 200
#     data = response.json()
#     short_url_id = data["short_url"]

#     response = await async_client.get(f"/url/{short_url_id}")
#     assert response.status_code == 200


# @pytest.mark.asyncio
# async def test_get_url_stats(async_client, test_db):
#     response = await async_client.post(
#         "/url/shorten", json={"original_url": "http://example.com"}
#     )
#     assert response.status_code == 200
#     data = response.json()
#     short_url_id = data["short_url"]

#     response = await async_client.get(f"/url/stats/{short_url_id}")
#     assert response.status_code == 200
#     data = response.json()
#     assert "original_url" in data
#     assert "short_url" in data
#     assert "stats" in data
