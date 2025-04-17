"""
JSON-based model implementation.
"""
from dataclasses import dataclass
import json
from uuid import uuid4


@dataclass
class Store:
    """
    name: Store name.

    address: Store address.

    city: Store city.

    phone: Store phone.

    mail: Store e-mail.
    """
    name: str
    address: str
    city: str
    phone: str
    mail: str


@dataclass
class Worker:
    """
    name: Worker's name.

    last_name: Worker's last name.

    phone: Worker's phone.

    mail: Worker's e-mail.
    """
    name: str
    last_name: str
    phone: str
    mail: str


@dataclass
class Product:
    """
    brand: Product brand.

    model: Product model.

    category: Product category.

    description: Product description.

    price: Product price.
    """
    brand: str
    model: str
    category: str
    description: str
    price: int


class NoSuchKeyError(ValueError):
    """
    Subclass of ValueError. Implemented for flexibility.
    """


class NoSuchUUIDError(ValueError):
    """
    Subclass of ValueError. Implemented for flexibility.
    """


class ValueMismatchError(ValueError):
    """
    Subclass of ValueError. Implemented for flexibility.
    """


class Model:
    """
    JSON-based model class.
    """
    def __init__(self):
        try:
            with open("data.json", encoding="utf-8") as file:
                self._data: dict = json.load(file)
        except FileNotFoundError:
            self._data = json.loads('{"stores": [], "workers": [], "products": []}')
            self._save()

    def add_store(self, store: Store):
        """
        Adds a store to the deserialized JSON file.
        :param store: Store dataclass.
        """
        self._data["stores"].append({
            "uuid": str(uuid4()),
            "name": store.name,
            "address": store.address,
            "city": store.city,
            "phone": store.phone,
            "mail": store.mail,
            "workers": [],
            "products": []
        })
        self._save()

    def add_worker(self, worker: Worker):
        """
        Adds a worker to the deserialized JSON file.
        :param worker: Worker dataclass.
        """
        self._data["workers"].append({
            "uuid": str(uuid4()),
            "name": worker.name,
            "lastName": worker.last_name,
            "phone": worker.phone,
            "mail": worker.mail
        })
        self._save()

    def add_product(self, product: Product):
        """
        Adds a product to the deserialized JSON file.
        :param product: Product dataclass.
        """
        self._data["products"].append({
            "uuid": str(uuid4()),
            "brand": product.brand,
            "model": product.model,
            "category": product.category,
            "description": product.description,
            "price": product.price
        })
        self._save()

    def get_stores(self) -> list:
        """
        Returns all stores contained in the deserialized JSON file.
        :return: List of dicts or empty list
        """
        return self._data["stores"]

    def get_workers(self) -> list:
        """
        Returns a list of all workers contained in the deserialized JSON file.
        :return: List of dicts or empty list
        """
        return self._data["workers"]

    def get_products(self) -> list:
        """
        Returns a list of all products contained in the deserialized JSON file.
        :return: List of dicts or empty list
        """
        return self._data["products"]

    def edit_store(self, index: int, uuid: str, store: Store):
        """
        Edits a store contained in the deserialized JSON file.

        If the provided index is invalid IndexError is raised.

        If a mismatch between the index and UUID is present ValueMismatchError is raised.
        :param index: Index to edit.
        :param uuid: UUID to edit.
        :param store: Instance of Store dataclass.
        """
        self._edit_value("stores", index, uuid, {
            "name": store.name,
            "address": store.address,
            "city": store.city,
            "phone": store.phone,
            "mail": store.mail,
        })

    def edit_worker(self, index: int, uuid: str, worker: Worker):
        """
        Edits a worker contained in the deserialized JSON file.

        If the provided index is invalid IndexError is raised.

        If a mismatch between the index and UUID is present ValueMismatchError is raised.
        :param index: Index to edit.
        :param uuid: UUID to edit.
        :param worker: Instance of Worker dataclass.
        """
        self._edit_value("workers", index, uuid, {
            "name": worker.name,
            "lastName": worker.last_name,
            "phone": worker.phone,
            "mail": worker.mail
        })

    def edit_product(self, index: int, uuid: str, product: Product):
        """
        Edits a product contained in the deserialized JSON file.

        If the provided index is invalid IndexError is raised.

        If a mismatch between the index and UUID is present ValueMismatchError is raised.
        :param index: Index to edit.
        :param uuid: UUID to edit.
        :param product: Instance of Product dataclass.
        """
        self._edit_value("products", index, uuid, {
            "brand": product.brand,
            "model": product.model,
            "category": product.category,
            "description": product.description,
            "price": product.price
        })

    def delete_store(self, index: int, uuid: str):
        """
        Deletes a store from the deserialized JSON file.

        If the provided index is invalid IndexError is raised.

        If nothing matches the provided UUID NoSuchUUIDError is raised.
        :param index: Index to delete.
        :param uuid: UUID to delete.
        """
        self._delete_value("stores", index, uuid)

    def delete_worker(self, index: int, uuid: str):
        """
        Deletes a worker from the deserialized JSON file.

        If the provided index is invalid IndexError is raised.

        If nothing matches the provided UUID NoSuchUUIDError is raised.
        :param index: Index to delete.
        :param uuid: UUID to delete.
        """
        self._delete_value("workers", index, uuid)

    def delete_product(self, index: int, uuid: str):
        """
        Deletes a product from the deserialized JSON file.

        If the provided index is invalid IndexError is raised.

        If nothing matches the provided UUID NoSuchUUIDError is raised.
        :param index: Index to delete.
        :param uuid: UUID to delete.
        """
        self._delete_value("products", index, uuid)

    def _edit_value(self, key: str, index: int, uuid: str, payload: dict[str, int | str]):
        if self._data[key][index]["uuid"] != uuid:
            raise ValueMismatchError("Mismatch between index and UUID")
        self._data[key][index].update(payload)
        self._save()

    def _delete_value(self, key: str, index: int, uuid: str):
        if key not in ["stores", "workers", "products"]:
            raise NoSuchKeyError("No key with such name")
        if self._data[key][index]["uuid"] != uuid:
            raise ValueMismatchError("Mismatch between index and UUID")
        del self._data[key][index]

    def _save(self):
        with open("data.json", "w", encoding="utf-8") as file:
            # for now let's leave the save indentation at 4 for easier reading
            json.dump(self._data, file, indent=4)
