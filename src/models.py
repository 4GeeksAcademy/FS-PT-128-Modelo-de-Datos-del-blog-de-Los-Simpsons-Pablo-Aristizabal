from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Table, Column, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

favorite_characters = Table(
    "favorite_characters",
    db.Model.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("character_id", Integer, ForeignKey("character.id"), primary_key=True),
)

favorite_locations = Table(
    "favorite_locations",
    db.Model.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("location_id", Integer, ForeignKey("location.id"), primary_key=True),
)

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    favorite_characters: Mapped[list["Character"]] = relationship(
        "Character",
        secondary = favorite_characters,
        back_populates = "favorited_by"
    )
    favorite_locations: Mapped[list["Location"]] = relationship(
        "Location",
        secondary = favorite_locations,
        back_populates = "favorited_by"
    )

  
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "favorite_characters": [character.serialize() for character in self.favorite_characters],
            "favorite_locations": [location.serialize() for location in self.favorite_locations],
            # do not serialize the password, its a security breach
        }


class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    age: Mapped[str] = mapped_column(Integer)
    occupation: Mapped[str] = mapped_column(String(120), nullable=False)
    image: Mapped[str] = mapped_column(String(120), nullable=True)
    favorited_by: Mapped[list["User"]] = relationship(
        "User",
        secondary=favorite_characters,
        back_populates="favorite_characters"
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "occupation": self.occupation,
            "image": self.image
        }
    
class Location(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    town: Mapped[str] = mapped_column(String(50))
    use: Mapped[str] = mapped_column(String(50))

    favorited_by: Mapped[list["User"]] = relationship(
        "User",
        secondary = favorite_locations,
        back_populates = "favorite_locations"
    )

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'town': self.town,
            'use': self.use
        }