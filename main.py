"""FastAPI recommendation engine with LaunchDarkly integration."""

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from ld_client import get_client, get_context, track
from mock_data import PRODUCTS, USERS, get_product, get_user
from recommender import alphabetical, by_rating, by_recency

app = FastAPI(title="Recommendation Engine")


class ClickBody(BaseModel):
    user_id: str
    product_id: str


@app.get("/recommendations")
def get_recommendations(user_id: str = Query(..., alias="user_id")):
    """Return ranked products based on LD flags. 404 if user not found."""
    user = get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    context = get_context(user_id, user["tier"], user["name"])
    client = get_client()

    premium = client.variation("premium-recommendations", context, False)

    if not premium:
        products = alphabetical(PRODUCTS)
        algorithm = "alphabetical"
    else:
        ranking = client.variation("recommendation-ranking-experiment", context, "rating")
        print(f"User {user_id} got ranking: {ranking}")
        print(f"User {user_id} got ranking: '{ranking}' == 'recency': {ranking == 'recency'}")
        if ranking == "recency":
            products = by_recency(PRODUCTS)
            algorithm = "recency"
        else:
            products = by_rating(PRODUCTS)
            algorithm = "rating"

    return {"products": products, "algorithm": algorithm}


@app.post("/click")
def post_click(body: ClickBody):
    """Track recommendation click event."""
    user = get_user(body.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not get_product(body.product_id):
        raise HTTPException(status_code=404, detail="Product not found")

    context = get_context(body.user_id, user["tier"], user["name"])
    track("recommendation_clicked", context, {"product_id": body.product_id})
    return {"ok": True}


@app.get("/users")
def get_users():
    """Return list of mock users."""
    return USERS


@app.get("/")
def root():
    """Serve the static app."""
    return FileResponse("static/index.html")


app.mount("/static", StaticFiles(directory="static"), name="static")
