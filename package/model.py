"""
JSON-based model.
"""
import dataclasses
import json
import uuid


@dataclasses.dataclass
class Store:
    """
    name: Store name. String.

    address: Store address. String.

    city: Store city. String.

    phone: Store phone. String.

    mail: Store e-mail. String.
    """
    name: str
    address: str
    city: str
    phone: str
    mail: str


@dataclasses.dataclass
class Worker:
    """
    name: Worker's name. String.

    last_name: Worker's last name. String.

    phone: Worker's phone. String.

    mail: Worker's e-mail. String.
    """
    name: str
    last_name: str
    phone: str
    mail: str


@dataclasses.dataclass
class Product:
    """
    brand: Product brand. String.

    model: Product model. String.

    category: Product category. String.

    description: Product description. String.

    price: Product price. Integer.
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


class Model:
    """
    Class of JSON-based model.
    """
    def __init__(self):
        try:
            with open("data.json", encoding="utf-8") as file:
                self._data: dict = json.load(file)
        except FileNotFoundError:
            with open("data.json", "w", encoding="utf-8") as file:
                json.dump({"stores": [], "workers": [], "products": []}, file)
            with open("data.json", encoding="utf-8") as file:
                self._data = json.load(file)

    def add_store(self, store: Store):
        """
        Adds a store to the deserialized JSON file.
        :param store: Store dataclass.
        """
        self._data["stores"].append({
            "uuid": str(uuid.uuid4()),
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
            "uuid": str(uuid.uuid4()),
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
            "uuid": str(uuid.uuid4()),
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
        :return: List of dicts
        """
        return self._data["stores"]

    def get_workers(self) -> list:
        """
        Returns a list of all workers contained in the deserialized JSON file.
        :return: List of dicts
        """
        return self._data["workers"]

    def get_products(self) -> list:
        """
        Returns a list of all products contained in the deserialized JSON file.
        :return: List of dicts
        """
        return self._data["products"]

    def edit_store(self, store_uuid: str, store: Store):
        """
        Edits a store contained in the deserialized JSON file.

        If no store matches the provided UUID ValueError is raised.
        :param store_uuid: UUID of store to edit. String.
        :param store: Instance of Store dataclass.
        """
        try:
            index = self._locate_something(store_uuid, "stores")
        except ValueError as e:
            raise e
        self._data["stores"][index].update({
            "name": store.name,
            "address": store.address,
            "city": store.city,
            "phone": store.phone,
            "mail": store.mail,
        })
        self._save()

    def edit_worker(self, worker_uuid: str, worker: Worker):
        """
        Edits a worker contained in the deserialized JSON file.

        If no worker matches the provided UUID ValueError is raised.
        :param worker_uuid: UUID of worker to edit. String.
        :param worker: Instance of Worker dataclass.
        """
        try:
            index = self._locate_something(worker_uuid, "workers")
        except ValueError as e:
            raise e
        self._data["workers"][index].update({
            "name": worker.name,
            "lastName": worker.last_name,
            "phone": worker.phone,
            "mail": worker.mail
        })
        self._save()

    def edit_product(self, product_uuid: str, product: Product):
        """
        Edits a product contained in the deserialized JSON file.

        If no product matches the provided UUID ValueError is raised.
        :param product_uuid: UUID of product to edit. String.
        :param product: Instance of Product dataclass.
        """
        try:
            index = self._locate_something(product_uuid, "products")
        except ValueError as e:
            raise e
        self._data["products"][index].update({
            "brand": product.brand,
            "model": product.model,
            "category": product.category,
            "description": product.description,
            "price": product.price
        })
        self._save()

    def delete_store(self, store_uuid: str):
        """
        Deletes a store from the deserialized JSON file.

        If no store matches the provided UUID ValueError is raised.
        :param store_uuid: UUID of store to delete. String.
        """
        try:
            self._delete_something(store_uuid, "stores")
        except ValueError as e:
            raise e

    def delete_worker(self, worker_uuid: str):
        """
        Deletes a worker from the deserialized JSON file.

        If no worker matches the provided UUID ValueError is raised.
        :param worker_uuid: UUID of worker to remove. String.
        """
        try:
            self._delete_something(worker_uuid, "workers")
        except ValueError as e:
            raise e

    def delete_product(self, product_uuid: str):
        """
        Deletes a product from the deserialized JSON file.

        If no product matches the provided UUID ValueError is raised.
        :param product_uuid: UUID of product to remove. String.
        """
        try:
            self._delete_something(product_uuid, "products")
        except ValueError as e:
            raise e

    def _delete_something(self, value_uuid: str, key: str):
        try:
            index = self._locate_something(value_uuid, key)
        except ValueError as e:
            raise e
        del self._data[key][index]
        self._save()

    def _locate_something(self, value_uuid: str, key: str):
        if key not in ["stores", "workers", "products"]:
            raise NoSuchKeyError("No key with such name")
        for index, value in enumerate(self._data[key]):  # type: int, dict
            if value["uuid"] == value_uuid:
                return index
        raise ValueError("No value with such UUID")

    def _save(self):
        with open("data.json", "w", encoding="utf-8") as file:
            # for now let's leave the save indentation at 4 for easier reading
            json.dump(self._data, file, indent=4)
