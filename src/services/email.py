import jwt
from jwt.exceptions import PyJWTError
from pathlib import Path
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi_mail.errors import ConnectionErrors
from pydantic import EmailStr

from src.conf.config import settings


conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME="Web_assistant System",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent / 'templates',
)

SECRET_KEY = settings.SECRET_KEY_JWT
ALGORITHM = settings.ALGORITHM


class EmailTokenHandler:
    SECRET_KEY = SECRET_KEY
    ALGORITHM = ALGORITHM

    def create_email_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=1)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire})
        token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return token

    async def get_email_from_token(self, token: str):
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            email = payload["sub"]
            return email
        except PyJWTError as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail="Invalid token for email verification")


token_handler = EmailTokenHandler()


async def send_email(email: EmailStr, username: str, host: str):

    try:
        token_verification = token_handler.create_email_token({"sub": email})
        message = MessageSchema(
            subject="Confirm your email ",
            recipients=[email],
            template_body={"host": host, "username": username, "token": token_verification},
            subtype=MessageType.html
        )

        fm = FastMail(conf)
        await fm.send_message(message, template_name="verify_email.html")
        # Логирование успешной отправки
        print(f"Email sent successfully to {email}")
        return {"message": f"Email sent successfully to {email}"}

    except ConnectionErrors as err:
        # Логирование ошибок
        print(f"Failed to send email to {email}: {err}")
        return {"message": f"Failed to send email to {email}", "error": str(err)}
