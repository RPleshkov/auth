from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.database import db_connector
from sqlalchemy.ext.asyncio import AsyncSession


SessionDep = Annotated[AsyncSession, Depends(db_connector.get_session)]
RequestForm = Annotated[OAuth2PasswordRequestForm, Depends()]
