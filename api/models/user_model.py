from api.models import BaseModel, Field, Optional

class UserModel(BaseModel):
    id: str = Field(..., description="Unique identifier for the user provided by auth system")
    email: str = Field(..., description="User's email address")
    first_name: str = Field(None, description="User's first name")
    last_name: str = Field(None, description="User's last name")


class UserModelOutput(UserModel):
    id: str

    class Config:
        from_attributes = True


class UserEditModel(BaseModel):
    first_name: Optional[str] = Field(None, description="User's first name")
    last_name: Optional[str] = Field(None, description="User's last name")
    email: Optional[str] = Field(None, description="User's email address")