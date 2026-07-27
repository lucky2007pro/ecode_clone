from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import List
from jose import jwt, JWTError
from users.auth import SECRET_KEY, ALGORITHM
from .enums import Permission, ROLE_PERMISSIONS, Role

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user_role(token: str = Depends(oauth2_scheme)) -> Role:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        role_str = payload.get("role")
        if role_str is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
        return Role(role_str)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

class RequirePermissions:
    def __init__(self, required_permissions: List[Permission]):
        self.required_permissions = required_permissions

    async def __call__(self, role: Role = Depends(get_current_user_role)):
        # Admin has all permissions
        if role == Role.ADMIN:
            return True
            
        user_permissions = ROLE_PERMISSIONS.get(role, [])
        
        for perm in self.required_permissions:
            if perm not in user_permissions:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, 
                    detail=f"Not enough permissions. Required: {perm.value}"
                )
        return True
