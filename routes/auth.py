from fastapi import APIRouter, HTTPException, Request

router = APIRouter(prefix="/api/auth", tags=["auth"])

async def validate_current_user(request: Request) -> int:
    user_id = request.session.get("user_id")

    if not isinstance(user_id, int):
        raise HTTPException(
            status_code=401,
            detail="User not logged in",
        )

    return user_id

@router.get("/dev/get_user/{user_id}")
async def get_user(request: Request, user_id: int):
    request.session["user_id"] = user_id
    return {"user_id": user_id}

@router.get("/logout")
async def logout(request: Request) -> bool:
    user_id = await validate_current_user(request)

    if user_id:
        request.session.pop("user_id")

    return not isinstance(await validate_current_user(request), int)