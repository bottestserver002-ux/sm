from fastapi import APIRouter
from pytrends.request import TrendReq
import requests

router = APIRouter(prefix="/seo", tags=["SEO"])


@router.get("/research")
def seo_research(keyword: str):

    # ====================
    # GOOGLE TRENDS
    # ====================
    pytrend = TrendReq(
        hl="vi-VN",
        tz=420
    )

    try:
        pytrend.build_payload([keyword])

        related = pytrend.related_queries()

        trend_keywords = []

        if (
            related.get(keyword)
            and related[keyword]["top"] is not None
        ):
            trend_keywords = (
                related[keyword]["top"]["query"]
                .head(10)
                .tolist()
            )

    except:
        trend_keywords = []

    # ====================
    # GOOGLE SUGGEST
    # ====================

    try:
        url = (
            "https://suggestqueries.google.com/"
            "complete/search"
            f"?client=firefox&hl=vi&q={keyword}"
        )

        suggestions = requests.get(
            url,
            timeout=10
        ).json()[1]

    except:
        suggestions = []

    return {
        "keyword": keyword,
        "google_suggest": suggestions,
        "google_trends": trend_keywords
    }