"""Recommendation ranking algorithms."""

from typing import TypedDict


class Product(TypedDict):
    id: str
    name: str
    price: float
    rating: float
    created_at: str


def alphabetical(products: list[Product]) -> list[Product]:
    """Sort products by name A–Z."""
    return sorted(products, key=lambda p: p["name"].lower())


def by_rating(products: list[Product]) -> list[Product]:
    """Sort products by rating descending."""
    return sorted(products, key=lambda p: p["rating"], reverse=True)


def by_recency(products: list[Product]) -> list[Product]:
    """Sort products by created_at descending (newest first)."""
    return sorted(products, key=lambda p: p["created_at"], reverse=True)
