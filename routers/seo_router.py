from fastapi import APIRouter
from pytrends.request import TrendReq
import requests
from urllib.parse import quote

router = APIRouter(prefix="/seo", tags=["SEO"])


@router.get("/research")
def seo_research(keyword: str):
    trend_keywords = []
    suggestions = []

    # GOOGLE SUGGEST
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

    # GOOGLE TRENDS
    try:
        pytrend = TrendReq(
            hl="vi-VN",
            tz=420
        )

        pytrend.build_payload(
            [keyword],
            cat=0,
            timeframe="today 12-m",
            geo="VN"
        )

        related = pytrend.related_queries()

        if (
            related.get(keyword)
            and related[keyword].get("top") is not None
        ):
            trend_keywords = (
                related[keyword]["top"]["query"]
                .head(10)
                .tolist()
            )

    except Exception as e:
        print("GOOGLE TRENDS ERROR:", str(e))
        trend_keywords = []

    return {
        "keyword": keyword,
        "google_suggest": suggestions,
        "google_trends": trend_keywords
    }