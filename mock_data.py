"""Mock products and users for the recommendation engine."""

PRODUCTS = [
    {
        "id": "prod-1",
        "name": "Wireless Headphones",
        "price": 89.99,
        "rating": 4.5,
        "created_at": "2025-01-15T10:00:00Z",
    },
    {
        "id": "prod-2",
        "name": "Desk Lamp",
        "price": 34.99,
        "rating": 4.2,
        "created_at": "2025-02-20T14:30:00Z",
    },
    {
        "id": "prod-3",
        "name": "Bluetooth Speaker",
        "price": 59.99,
        "rating": 4.8,
        "created_at": "2025-01-10T09:00:00Z",
    },
    {
        "id": "prod-4",
        "name": "Keyboard",
        "price": 79.99,
        "rating": 4.0,
        "created_at": "2025-03-01T11:00:00Z",
    },
    {
        "id": "prod-5",
        "name": "Monitor Stand",
        "price": 49.99,
        "rating": 4.6,
        "created_at": "2025-02-05T16:00:00Z",
    },
]

USERS = [
    {"id": "alice", "name": "Alice", "tier": "free"},
    {"id": "bob", "name": "Bob", "tier": "premium"},
    {"id": "carol", "name": "Carol", "tier": "premium"},
    {"id": "dave", "name": "Dave", "tier": "free"},
    {"id": "eve", "name": "Eve", "tier": "premium"},
    {"id": "frank", "name": "Frank", "tier": "premium"},
    {"id": "grace", "name": "Grace", "tier": "premium"},
    {"id": "henry", "name": "Henry", "tier": "free"},
]


def get_user(user_id: str) -> dict | None:
    """Return user by id or None if not found."""
    for u in USERS:
        if u["id"] == user_id:
            return u
    return None


def get_product(product_id: str) -> dict | None:
    """Return product by id or None if not found."""
    for p in PRODUCTS:
        if p["id"] == product_id:
            return p
    return None
