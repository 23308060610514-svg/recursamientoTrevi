from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UsuarioSchema(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=50)
    apellido: Optional[str] = None
    telefono: Optional[str] = None
    email: EmailStr
    password: str = Field(..., min_length=4)