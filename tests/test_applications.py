def register_and_get_token(client, email: str, password: str = "password12345"):
    register_response = client.post(
        "/users/register",
        json={
            "email": email,
            "password": password,
        },
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/users/login",
        data={
            "username": email,
            "password": password,
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


def test_application_requires_login(client):
    response = client.get("/applications/")

    assert response.status_code == 401


def test_create_and_list_own_applications(client):
    headers = register_and_get_token(client, "owner@example.com")

    create_response = client.post(
        "/applications/",
        headers=headers,
        json={
            "company": "TCS",
            "role": "Python Developer",
            "status": "Applied",
            "notes": "Created by automated test",
        },
    )

    assert create_response.status_code == 201

    created = create_response.json()
    assert created["id"] == 1
    assert created["company"] == "TCS"
    assert created["user_id"] == 1

    list_response = client.get(
        "/applications/",
        headers=headers,
    )

    assert list_response.status_code == 200

    applications = list_response.json()
    assert len(applications) == 1
    assert applications[0]["company"] == "TCS"


def test_user_cannot_access_another_users_application(client):
    user_one_headers = register_and_get_token(
        client,
        "userone@example.com",
    )

    create_response = client.post(
        "/applications/",
        headers=user_one_headers,
        json={
            "company": "Infosys",
            "role": "Backend Developer",
            "status": "Applied",
        },
    )

    application_id = create_response.json()["id"]

    user_two_headers = register_and_get_token(
        client,
        "usertwo@example.com",
    )

    response = client.get(
        f"/applications/{application_id}",
        headers=user_two_headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Job application not found"


def test_update_and_delete_own_application(client):
    headers = register_and_get_token(
        client,
        "update@example.com",
    )

    create_response = client.post(
        "/applications/",
        headers=headers,
        json={
            "company": "Wipro",
            "role": "Python Developer",
            "status": "Applied",
        },
    )

    application_id = create_response.json()["id"]

    update_response = client.patch(
        f"/applications/{application_id}",
        headers=headers,
        json={
            "status": "Interview",
            "notes": "Interview is scheduled",
        },
    )

    assert update_response.status_code == 200
    assert update_response.json()["status"] == "Interview"

    delete_response = client.delete(
        f"/applications/{application_id}",
        headers=headers,
    )

    assert delete_response.status_code == 200

    get_response = client.get(
        f"/applications/{application_id}",
        headers=headers,
    )

    assert get_response.status_code == 404