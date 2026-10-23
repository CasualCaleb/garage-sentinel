from fastapi import APIRouter, Request, HTTPException, Depends
from models import UsernameUpdate, User
from services import user_services

async def require_user(request: Request) -> User:
    if "user_id" not in request.session:
        raise HTTPException(
            status_code=401,
            detail="You have not logged in"
        )

    user_id = request.session["user_id"]
    user = await user_services.get_user(user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user

router = APIRouter(
    prefix="/api/users",
    dependencies=[Depends(require_user)]
)

# Get current user info
@router.get("/me", name="me")
async def read_user_oauth_accounts(
        user: User = Depends(require_user)
):
    oauth_accounts = await user_services.get_oauth_accounts(user)
    return {
        'user': user,
        'oauth_accounts': [
            oauth_account for oauth_account in oauth_accounts
        ]
    }

# Change the current user's username
@router.patch("/me/username", name="username")
async def update_username(
        data: UsernameUpdate,
        user: User = Depends(require_user)
):
    is_updated = await user_services.change_username(
        user.id,
        data.username
    )
    return is_updated

# Delete the current user
@router.delete("/me", name="delete_me")
async def delete_me(
        request: Request,
        user: User = Depends(require_user)
):
    is_deleted = await user_services.delete_user(user.id)

    if is_deleted :
        request.session.clear()

    return is_deleted