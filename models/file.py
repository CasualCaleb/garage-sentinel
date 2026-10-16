from pydantic import BaseModel

class File(BaseModel):
    id: int
    filename: str
    filetype: str
    storage_name: str
    created_at: str