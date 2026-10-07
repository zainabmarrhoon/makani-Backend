from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from models.user import UserModel
from database import get_db
import jwt
from jwt import DecodeError, ExpiredSignatureError
from jwt.exceptions import InvalidSubjectError
from config.environment import JWT_SECRET


http_bearer = HTTPBearer()


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(http_bearer)
):
    try:
        payload = jwt.decode(
            token.credentials,
            JWT_SECRET,
            algorithms=["HS256"]
        )

        current_user_id = payload.get("sub")

        if current_user_id is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token invalid"
            )

        current_user_id = int(current_user_id)

        user = (
            db.query(UserModel)
            .filter(UserModel.id == current_user_id)
            .first()
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )

        return user

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token invalid"
        )

    except DecodeError as err:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Could not decode token: {str(err)}"
        )

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token has expired"
        )

    except InvalidSubjectError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token invalid"
        )