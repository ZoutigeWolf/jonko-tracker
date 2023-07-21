from typing import TypeVar, Type, Union, Any

from database import database

T = TypeVar("T", bound="Model")


class Model:
    table = "none"

    def __init__(self, id: int) -> None:
        self.id = id

    def as_dict(self) -> dict:
        d = self.__dict__

        for k, v in d.items():
            if isinstance(v, bytes):
                d[k] = str(v)

        return d

    def update(self, **kwargs) -> None:
        for k, v in kwargs.items():
            if not hasattr(self, k) or not isinstance(v, type(getattr(self, k))):
                continue

            setattr(self, k, v)

        data = self.__dict__

        database.execute(
            f"""
            UPDATE {self.table}
            SET {(', '.join([f'{k} = %s' for k in data.keys() if k != 'id']))}
            WHERE id = %s
            """,
            tuple(v for k, v in data.items() if k != "id") + (self.id,)
        )

    def delete(self) -> None:
        database.execute(
            f"DELETE FROM {self.table} WHERE id = %s",
            (self.id,)
        )

    @classmethod
    def create(cls: Type[T], *args) -> T:
        id = cls.get_next_id()

        t = cls(id, *args)

        database.execute(
            f"""
            INSERT INTO {cls.table}
            VALUES({(', '.join(['%s' for _ in range(len(args) + 1)]))})
            """,
            (id,) + args
        )

        return t

    @classmethod
    def get_all(cls: Type[T]) -> list[T]:
        return [cls(*r) for r in database.execute(f"SELECT * FROM {cls.table}")]

    @classmethod
    def get_by(cls: Type[T], name: str, value: Any) -> Union[T, None]:
        res = [x for x in cls.get_all() if getattr(x, name) == value]

        return res[0] if len(res) != 0 else None

    @classmethod
    def get_next_id(cls: Type[T]) -> int:
        return max([x.id for x in cls.get_all()], default=0) + 1

    def __repr__(self) -> str:
        return str(self.__dict__)
