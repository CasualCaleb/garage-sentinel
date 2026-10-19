from pydantic import BaseModel

class File(BaseModel):
    id: int
    user_id: int
    filename: str
    filetype: str
    storage_name: str
    created_at: str