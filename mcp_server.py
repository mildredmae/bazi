# mcp_server.py
# FastAPI BaZi REST API

from fastapi import FastAPI, Query
from bazi_tool import BaZiCalculator

app = FastAPI(title="BaZi REST API")

@app.get("/api/bazi")
def get_bazi(
    name: str = Query(..., description="Person's name"),
    gender: str = Query(..., regex="^(male|female|男|女)$", description="Gender (male/female)"),
    year: int = Query(..., description="Birth year"),
    month: int = Query(..., description="Birth month"),
    day: int = Query(..., description="Birth day"),
    hour: int = Query(..., description="Birth hour (0–23)"),
    minute: int = Query(0, description="Birth minute (0–59)"),
    birth_city: str = Query(..., description="Birth city name")
):
    """Compute BaZi chart using BaZiCalculator and return structured JSON."""
    try:
        g = "男" if gender.lower() in ["male", "男"] else "女"
        calc = BaZiCalculator(
            name=name,
            gender=g,
            calendar="公历",
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
            birth_city=birth_city,
            current_city=birth_city,
        )
        return {
            "name": name,
            "gender": gender,
            "bazi": calc.ba_zi,
            "jie_qi": calc.jie_qi_info,
            "da_yun": calc.da_yun_info,
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def root():
    return {"message": "🪶 BaZi REST API is alive — use /api/bazi"}
