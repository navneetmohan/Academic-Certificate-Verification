import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app
from app.utils.pdf_generator import generate_certificate_pdf
from app.utils.hashing import compute_sha256

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "Blockchain Academic Certificate Verification API"
    assert data["status"] == "online"

def test_auth_login_successful():
    response = client.post(
        "/api/auth/login",
        json={"email": "admin@university.edu", "password": "adminpassword123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["institution"]["email"] == "admin@university.edu"

def test_auth_login_invalid_password():
    response = client.post(
        "/api/auth/login",
        json={"email": "admin@university.edu", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]

def test_get_current_user_authenticated():
    # 1. Login
    login_res = client.post(
        "/api/auth/login",
        json={"email": "admin@university.edu", "password": "adminpassword123"}
    )
    token = login_res.json()["access_token"]

    # 2. Get profile
    res = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert res.json()["email"] == "admin@university.edu"

@patch("app.services.verification_service.blockchain_service.get_certificate_status")
def test_verify_non_existent_certificate(mock_get_status):
    mock_get_status.return_value = {
        "exists": False,
        "certificate_hash": None,
        "issuer": None,
        "issued_at": 0,
        "revoked": False
    }
    res = client.get("/api/verify/CERT-9999-9999")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "NOT_FOUND"
    assert data["is_authentic"] is False

@patch("app.services.verification_service.blockchain_service.get_certificate_status")
def test_verify_revoked_certificate(mock_get_status):
    mock_get_status.return_value = {
        "exists": True,
        "certificate_hash": "0x3a7bd117c2445e994917462ec5ab2eeae3c85bb049e3bf8e2a3962d3a39e7b23",
        "issuer": "0x70997970C51812dc3A010C7d01b50e0d17dc79C8",
        "issued_at": 1727180000,
        "revoked": True
    }
    res = client.get("/api/verify/CERT-2026-0001")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "REVOKED"
    assert data["is_revoked"] is True
    assert data["is_authentic"] is False

@patch("app.services.verification_service.blockchain_service.get_certificate_status")
def test_verify_valid_certificate(mock_get_status):
    mock_get_status.return_value = {
        "exists": True,
        "certificate_hash": "0x3a7bd117c2445e994917462ec5ab2eeae3c85bb049e3bf8e2a3962d3a39e7b23",
        "issuer": "0x70997970C51812dc3A010C7d01b50e0d17dc79C8",
        "issued_at": 1727180000,
        "revoked": False
    }
    res = client.get("/api/verify/CERT-2026-0001")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "VALID"
    assert data["is_authentic"] is True
    assert data["issuer_address"] == "0x70997970C51812dc3A010C7d01b50e0d17dc79C8"

def test_pdf_generation_magic_bytes():
    pdf_bytes = generate_certificate_pdf(
        certificate_id="CERT-TEST-0001",
        student_name="Alexander Hamilton",
        student_id="STU-88219",
        degree="Master of Science in Information Security",
        department="Computer Science",
        institution_name="Metropolitan State University",
        graduation_year=2026,
        issue_date="2026-09-24"
    )
    assert pdf_bytes is not None
    assert len(pdf_bytes) > 1000
    # PDF specification magic bytes header
    assert pdf_bytes.startswith(b"%PDF-")

    # Hash of generated PDF should be a valid 66-character 0x hex string
    cert_hash = compute_sha256(pdf_bytes)
    assert cert_hash.startswith("0x")
    assert len(cert_hash) == 66
