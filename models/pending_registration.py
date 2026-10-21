from pydantic import BaseModel

class CreatePendingRegistration(BaseModel):
    username: str
    provider: str
    provider_id: str
    provider_email: str

class PendingRegistration(CreatePendingRegistration):
    token_hash: str