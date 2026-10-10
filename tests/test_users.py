def test_register_user(client):
    response = client.post(
        "/users/register",
        json={
            "email": "test@example.com",
            "password": "password12345",
        },
    )

    assert response.status_code == 201

    data = response.json()
    assert data["id"] == 1
    assert data["email"] == "test@example.com"
    assert "password" not in data
    assert "hashed_password" not in data


def test_register_duplicate_email(client):
    user_data = {
        "email": "duplicate@example.com",
        "password": "password12345",
    }

    first_response = client.post("/users/register", json=user_data)
    second_response = client.post("/users/register", json=user_data)

    assert first_response.status_code == 201
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == (
        "An account with this email already exists"
    )


def test_login_user(client):
    client.post(
        "/users/register",
        json={
            "email": "login@example.com",
            "password": "password12345",
        },
    )

    response = client.post(
        "/users/login",
        data={
            "username": "login@example.com",
            "password": "password12345",
        },
    )

    assert response.status_code == 200

    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_with_wrong_password(client):
    client.post(
        "/users/register",
        json={
            "email": "wrongpassword@example.com",
            "password": "password12345",
        },
    )

    response = client.post(
        "/users/login",
        data={
            "username": "wrongpassword@example.com",
            "password": "incorrect-password",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"


def test_get_and_update_my_profile(client):
    client.post(
        "/users/register",
        json={
            "email": "profile@example.com",
            "password": "password12345",
        },
    )

    login_resp = client.post(
        "/users/login",
        data={
            "username": "profile@example.com",
            "password": "password12345",
        },
    )
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    get_resp = client.get("/users/me", headers=headers)
    assert get_resp.status_code == 200
    data = get_resp.json()
    assert data["email"] == "profile@example.com"
    assert data["linkedin_url"] is None
    assert data["github_url"] is None

    patch_resp = client.patch(
        "/users/me",
        headers=headers,
        json={
            "linkedin_url": "https://linkedin.com/in/testuser",
            "github_url": "https://github.com/testuser",
        },
    )
    assert patch_resp.status_code == 200
    updated_data = patch_resp.json()
    assert updated_data["linkedin_url"] == "https://linkedin.com/in/testuser"
    assert updated_data["github_url"] == "https://github.com/testuser"