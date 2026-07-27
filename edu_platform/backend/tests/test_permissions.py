import pytest
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient
from permissions.enums import Permission, Role
from permissions.dependencies import RequirePermissions

# Setup a test FastAPI app
app = FastAPI()

# A mock function to simulate get_current_user_role since we just want to test RequirePermissions
def override_get_current_user_role_factory(role: Role):
    async def _override():
        return role
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
    # Override dependency to return STUDENT role
    app.dependency_overrides[RequirePermissions] = None # Clear if any
    from permissions.dependencies import get_current_user_role
    app.dependency_overrides[get_current_user_role] = override_get_current_user_role_factory(Role.STUDENT)
    
    response = client.get("/finance")
    assert response.status_code == 403
    assert "Not enough permissions" in response.json()["detail"]

def test_student_can_view_dashboard():
    from permissions.dependencies import get_current_user_role
    app.dependency_overrides[get_current_user_role] = override_get_current_user_role_factory(Role.STUDENT)
    
    response = client.get("/dashboard")
    assert response.status_code == 200

def test_manager_can_view_finance():
    from permissions.dependencies import get_current_user_role
    app.dependency_overrides[get_current_user_role] = override_get_current_user_role_factory(Role.MANAGER)
    
    response = client.get("/finance")
    assert response.status_code == 200

def test_admin_can_access_anything():
    from permissions.dependencies import get_current_user_role
    app.dependency_overrides[get_current_user_role] = override_get_current_user_role_factory(Role.ADMIN)
    
    response = client.get("/admin-only")
    assert response.status_code == 200
    
    response = client.get("/finance")
    assert response.status_code == 200
