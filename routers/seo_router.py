from fastapi import APIRouter
import requests
from urllib.parse import quote

router = APIRouter(prefix="/seo", tags=["SEO"])


@router.get("/research")
def seo_research(keyword: str):
    suggestions = []

    try:
        encoded_keyword = quote(keyword)

        url = (
            "https://suggestqueries.google.com/"
            "complete/search"
            f"?client=firefox&hl=vi&q={encoded_keyword}"
        )

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        suggestions = requests.get(
            url,
            headers=headers,
            timeout=10
        ).json()[1]

    except Exception as e:
        print("GOOGLE SUGGEST ERROR:", str(e))
        suggestions = []

    return {
        "keyword": keyword,
        "google_suggest": suggestions,
        "google_trends": []
    }