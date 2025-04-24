from typing import Annotated
from fastapi import Depends
from app.database import db_connector
from sqlalchemy.ext.asyncio import AsyncSession


SessionDep = Annotated[AsyncSession, Depends(db_connector.get_session)]
