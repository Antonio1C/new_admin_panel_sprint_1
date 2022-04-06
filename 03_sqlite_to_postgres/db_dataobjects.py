import uuid
from dataclasses import dataclass, field, fields
from datetime import datetime


def get_fields(data_type: type):
    return [fld.name for fld in fields(data_type)]


@dataclass
class Filmwork():
    title: str
    description: str
    creation_date: datetime
    type: str
    created_at: datetime
    updated_at: datetime
    rating: float = field(default=0.0)
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class Person:
    full_name: str
    created_at: datetime
    updated_at: datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class Genre:
    name: str
    description: str
    created_at: datetime
    updated_at: datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class GenreFilmwork:
    genre_id: uuid.UUID
    film_work_id: uuid.UUID
    created_at: datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class PersonFilmwork:
    person_id: uuid.UUID
    film_work_id: uuid.UUID
    role: str
    created_at: datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)


TABLE_TYPES = {
    'film_work': Filmwork,
    'person': Person,
    'genre': Genre,
    'genre_film_work': GenreFilmwork,
    'person_film_work': PersonFilmwork,
}


FIELD_MATCHING = {
    'created_at': 'created',
    'updated_at': 'modified',
}