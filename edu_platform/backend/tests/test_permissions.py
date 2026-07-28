import types

import pytest
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient
from permissions.enums import Permission, Role
from permissions.dependencies import RequirePermissions, get_current_user

# Setup a test FastAPI app
app = FastAPI()


# A mock function to simulate get_current_user since we just want to test RequirePermissions
def override_get_current_user_factory(role: Role):
    async def _override():
        return types.SimpleNamespace(role=role, id=None)
    return _override


# Test endpoints
@app.get("/finance", dependencies=[Depends(RequirePermissions([Permission.VIEW_FINANCE]))])
def view_finance():
    return {"status": "ok"}


@app.get("/dashboard", dependencies=[Depends(RequirePermissions([Permission.VIEW_DASHBOARD]))])
def view_dashboard():
    return {"status": "ok"}


@app.get("/admin-only", dependencies=[Depends(RequirePermissions([Permission.MANAGE_SETTINGS]))])
def view_settings():
    return {"status": "ok"}


client = TestClient(app)


def test_student_cannot_view_finance():
    app.dependency_overrides[get_current_user] = override_get_current_user_factory(Role.STUDENT)

    response = client.get("/finance")
    assert response.status_code == 403
    assert "Not enough permissions" in response.json()["detail"]


def test_student_can_view_dashboard():
    app.dependency_overrides[get_current_user] = override_get_current_user_factory(Role.STUDENT)

    response = client.get("/dashboard")
    assert response.status_code == 200


def test_manager_can_view_finance():
    app.dependency_overrides[get_current_user] = override_get_current_user_factory(Role.MANAGER)

    response = client.get("/finance")
    assert response.status_code == 200


def test_admin_can_access_anything():
    app.dependency_overrides[get_current_user] = override_get_current_user_factory(Role.ADMIN)

    response = client.get("/admin-only")
    assert response.status_code == 200

    response = client.get("/finance")
    assert response.status_code == 200
