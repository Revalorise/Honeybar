import sqlalchemy as sa
import sqlalchemy.orm as so
from mojang import API
from typing import Optional
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login
from app.utils.load_minecraft_details import get_minecraft_avatar

api = API()


class User(db.Model, UserMixin):
    __tablename__ = "hb_user"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)

    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)

    minecraft_username: so.Mapped[str] = so.mapped_column(sa.String(30), index=True,
                                                          unique=True)

    minecraft_uuid: so.Mapped[str] = so.mapped_column(sa.String(36), index=True,
                                                      unique=True)

    minecraft_avatar: so.Mapped[str] = so.mapped_column(sa.String(100), unique=True)

    rank: so.Mapped[Optional[str]] = so.mapped_column(sa.String(20), default='Player', nullable=True)

    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    created_at: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime, default=datetime.utcnow
    )

    posts: so.WriteOnlyMapped['Post'] = so.relationship(
        back_populates='author'
    )

    def set_password(self, password: str) -> None:
        """Set registered password into hash."""
        self.password_hash = generate_password_hash(password)

    def set_uuid(self, minecraft_username: str) -> None:
        """Set Minecraft uuid based on Minecraft username."""
        self.minecraft_uuid = api.get_uuid(minecraft_username)

    def get_uuid(self) -> str:
        """Get and return Minecraft uuid."""
        return self.minecraft_uuid

    def set_avatar(self, uuid: str) -> None:
        """Set Minecraft avatar based on Minecraft uuid."""
        self.minecraft_avatar = get_minecraft_avatar(uuid)

    def check_password(self, password: str):
        return check_password_hash(self.password_hash, password)

    @login.user_loader
    def load_user(id):
        return db.session.get(User, int(id))

    def __repr__(self):
        return f"<User {self.email}>"


class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)

    title: so.Mapped[str] = so.mapped_column(sa.String(100))
    body: so.Mapped[str] = so.mapped_column(sa.String(500))

    created_at: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.utcnow
    )
    updated_at: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.utcnow, onupdate=datetime.utcnow
    )

    author: so.Mapped[User] = so.relationship(
        back_populates='posts'
    )

    def __repr__(self):
        return f"<Post {self.body}>"
