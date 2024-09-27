from fastapi import APIRouter, Query, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from api.scrape import Vlr

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)
vlr = Vlr()


@router.get("/news")
@limiter.limit("250/minute")
async def VLR_news(request: Request):
    return vlr.vlr_news()


@router.get("/stats")
@limiter.limit("250/minute")
async def VLR_stats(
    request: Request,
    event_group_id: str = Query(..., description="type of event (GC 2024: 62, GC 2023: 38, GC 2022: 17, GC 2021: 8, or all)"),
    event_id: str = Query(..., description="name of the tournament"),
    series_id: str = Query(..., description="group stage, playoffs, etc"),
    region: str = Query(..., description="Region shortname"),
    min_rounds: str = Query(..., description="min_rounds"),
    min_rating: str = Query(..., description="min_rating"),
    agent: str = Query(..., description="breach, viper, or all"),
    map_id: str = Query(..., description="map_id: a number, or all"),
    timespan: str = Query(..., description="Timespan (30, 60, 90, or all)"),
):
    """
    Get VLR stats with query parameters.

    region shortnames:\n
        "na": "north-america",\n
        "eu": "europe",\n
        "ap": "asia-pacific",\n
        "sa": "latin-america",\n
        "jp": "japan",\n
        "oce": "oceania",\n
        "mn": "mena"\n
    """
    return vlr.vlr_stats(region, timespan)


@router.get("/rankings")
@limiter.limit("250/minute")
async def VLR_ranks(
    request: Request, region: str = Query(..., description="Region shortname")
):
    """
    Get VLR rankings for a specific region.

    region shortnames:\n
        "na": "north-america",\n
        "eu": "europe",\n
        "ap": "asia-pacific",\n
        "la": "latin-america",\n
        "la-s": "la-s",\n
        "la-n": "la-n",\n
        "oce": "oceania",\n
        "kr": "korea",\n
        "mn": "mena",\n
        "gc": "game-changers",\n
        "br": "Brazil",\n
        "cn": "china",\n
        "jp": "japan",\n
        "col": "collegiate",\n
    """
    return vlr.vlr_rankings(region)


@router.get("/match")
@limiter.limit("250/minute")
async def VLR_match(request: Request, q: str):
    """
    query parameters:\n
        "upcoming": upcoming matches,\n
        "live_score": live match scores,\n
        "results": match results,\n
    """
    if q == "upcoming":
        return vlr.vlr_upcoming_matches()
    elif q == "live_score":
        return vlr.vlr_live_score()
    elif q == "results":
        return vlr.vlr_match_results()
    else:
        return {"error": "Invalid query parameter"}


@router.get("/health")
def health():
    return vlr.check_health()
