# LaunchDarkly E-Commerce Recommendation Engine

A mock e-commerce recommendation engine that demonstrates feature flagging and A/B experimentation using the [LaunchDarkly](https://launchdarkly.com) Python SDK.

---

## What It Does

Users browse a product catalog and receive a ranked list of recommendations. The ranking strategy they see depends on who they are and which experiment variant they're assigned to — all controlled in real time via LaunchDarkly, with no code changes required.

---

## LaunchDarkly Integration

This project uses two flags:

### 1. `premium-recommendations` (Feature Flag)
Controls **who gets access** to intelligent ranking.

| User tier | Result |
|-----------|--------|
| `free` | Alphabetical list (no intelligence applied) |
| `premium` | Algorithm-based ranking |

This flag uses a targeting rule: `if user.tier is one of "premium" → serve true`. Free users never reach the experiment — they're gated out first.

### 2. `recommendation-ranking-experiment` (Experiment Flag)
Controls **which ranking algorithm** premium users see, as a 50/50 random split.

| Variant | Behavior |
|---------|----------|
| `control` | Sort by rating (highest rated first) |
| `treatment` | Sort by recency (newest first) |

LD hashes each user's key to assign them consistently — the same user always sees the same variant, every request.

### Why Two Flags?

The feature flag and the experiment solve different problems:

- The **flag** is about operational control — gate expensive logic to premium users, with an instant kill switch if something breaks.
- The **experiment** is about learning — which ranking strategy actually drives more engagement?

Separating them means you can roll back the experiment without touching the premium gate, and vice versa.

---

## The Experiment

**Hypothesis:** Sorting recommendations by recency drives more clicks than sorting by rating.

**Metric:** `recommendation_clicked` — whether a user clicked at least once after seeing their recommendation list (binary occurrence metric, higher is better).

**Statistical approach:** Frequentist, fixed horizon, two-sided test at α = 0.05.

The two-sided test is intentional — while the hypothesis is directional (we believe recency wins), a two-sided test is more statistically rigorous. It detects a significant difference in either direction, so if rating actually outperforms recency, we catch that too.

**Interpreting results:**
1. If p < 0.05 → the observed difference is statistically significant (unlikely due to chance)
2. Look at the click rates per variant → whichever is higher drives more engagement
3. That result directly informs the flag rollout — no code deploy needed

> In this mock project, statistical significance isn't reachable with 4 users. The instrumentation pattern — flag evaluation, event tracking, experiment configuration — is production-ready. Significance is a function of user volume and time, not code.

---

## Project Structure
```
ld-recommendation-engine/
├── main.py          # FastAPI app and endpoints
├── recommender.py   # Sorting algorithms (alphabetical, rating, recency)
├── ld_client.py     # LaunchDarkly SDK initialization and helpers
├── mock_data.py     # Mock products and users
├── static/
│   └── index.html   # Single-page UI (vanilla JS)
├── requirements.txt
└── .env             # SDK key (not committed)
```

---

## Setup

### Prerequisites
- Python 3.11+
- A [LaunchDarkly](https://launchdarkly.com/pricing) account (free developer tier)

### 1. Clone the repo
```bash
git clone https://github.com/AChoy7/ld-recommendation-engine
cd ld-recommendation-engine
```

### 2. Create a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your LaunchDarkly SDK key
Create a `.env` file in the project root:
```
LAUNCHDARKLY_SDK_KEY=sdk-your-test-environment-key-here
```
Use your **Test** environment SDK key from the LaunchDarkly dashboard.

### 5. Configure LaunchDarkly flags
Create two flags in your Test environment:

**Flag 1: `premium-recommendations`** (Boolean)
- Targeting rule: `if user tier is one of "premium"` → serve `true`
- Default rule: serve `false`

**Flag 2: `recommendation-ranking-experiment`** (String)
- Variations: `recency` (treatment), `rating` (control)
- Default rule: 50% / 50% percentage rollout, randomized by user key

### 6. Run the app
```bash
uvicorn main:app --reload
```

Open [http://localhost:8000](http://localhost:8000)

---

## Demo Walkthrough

1. Select **Alice (free)** → alphabetical list, badge shows `alphabetical`
2. Select **Bob (premium)** → rating-sorted list, badge shows `rating`
3. Select **Carol (premium)** → recency-sorted list, badge shows `recency`
4. Click a product → fires `recommendation_clicked` event to LaunchDarkly
5. Open LD dashboard → Iterate → Experiments → see live exposures and click attributions per variant

Bob and Carol are in different experiment variants because LD hashes their user keys to opposite sides of the 50/50 split.

---

## Mock Users

| User | Tier | Experiment Variant |
|------|------|-------------------|
| Alice | free | N/A (gated out) |
| Bob | premium | control (rating) |
| Carol | premium | treatment (recency) |
| Dave | free | N/A (gated out) |

---

## Key Design Decisions

**In-memory data only** — no database, no auth. Keeps the focus on the LaunchDarkly integration rather than infrastructure.

**Algorithm badge in API response** — the backend computes which algorithm was used and returns it in the response. The frontend doesn't need to know anything about flags or variants — it just renders what the API tells it.

**Fallback values** — both flag evaluations specify safe defaults. If LaunchDarkly is unreachable, free users get alphabetical and premium users get rating. The app degrades gracefully rather than erroring.

**ISO 8601 timestamps** — `created_at` values use ISO format so they sort correctly as plain strings without parsing. `"2025-03-01"` > `"2025-01-10"` lexicographically, which matches chronological order.