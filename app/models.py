import sqlalchemy as sa
import sqlalchemy.orm as so
from typing import Optional
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_admin.contrib.sqla import ModelView
from app import db, login, admin


class Users(db.Model, UserMixin):
    __tablename__ = "users"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(140), index=True,
                                             unique=True)

    rank: so.Mapped[str] = so.mapped_column(sa.String(20), index=True,
                                            default='Player', nullable=True)

    password_hash: so.Mapped[Optional[str]] = so.mapped_column(
        sa.String(256))

    posts: so.WriteOnlyMapped['Post'] = so.relationship(
        back_populates='author'
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @login.user_loader
    def load_user(id):
        return db.session.get(Users, int(id))

    def __repr__(self):
        return f"<User {self.email}>"


class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(140))
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc)
    )
    user_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey('users.id'), index=True
    )

    author: so.Mapped[Users] = so.relationship(
        back_populates='posts'
    )

    def __repr__(self):
        return f"<Post {self.body}>"


admin.add_view(ModelView(Users, db.session))
admin.add_view(ModelView(Post, db.session))
