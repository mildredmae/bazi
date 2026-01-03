# mcp_server.py
import os
from mcp.server.fastmcp import FastMCP
from bazi_tool import BaZiCalculator

# --- MCP SERVER (for internal AI connections) ---
mcp = FastMCP(name="BaZi Tool")
mcp.settings.port = int(os.environ.get("PORT", "8001"))
mcp.settings.host = "0.0.0.0"

@mcp.tool()
def bazi(
    name: str,
    gender: str,
    calendar: str,
    year: int,
    month: int,
    day: int,
    hour: int,
    minute: int,
    birth_city: str,
    current_city: str | None = None,
) -> dict:
    """
    Calculate BaZi (八字) information.
    """
    calculator = BaZiCalculator(
        name=name,
        gender=gender,
        calendar=calendar,
        year=year,
        month=month,
        day=day,
        hour=hour,
        minute=minute,
        birth_city=birth_city,
        current_city=current_city,
    )

    gender_text = "男 (乾造)" if calculator.gender == "男" else "女 (坤造)"

    if calculator.calendar == "公历":
        solar_date_str = f"{calculator.solar_time.year}年{calculator.solar_time.month}月{calculator.solar_time.day}日{calculator.solar_time.hour:02d}:{calculator.solar_time.minute:02d}"
        lunar_year = calculator.lunar_date.getLunarYear()
        lunar_month = calculator.lunar_date.getLunarMonth()
        lunar_day = calculator.lunar_date.getLunarDay()
        is_leap = "(闰月)" if calculator.lunar_date.isLunarLeap() else ""
        lunar_date_str = f"{lunar_year}年{lunar_month}月{lunar_day}日{calculator.solar_time.hour:02d}:{calculator.solar_time.minute:02d} {is_leap}"
        birth_time_info = {"公历": solar_date_str, "农历": lunar_date_str}
    else:
        lunar_year = calculator.lunar_date.getLunarYear()
        lunar_month = calculator.lunar_date.getLunarMonth()
        lunar_day = calculator.lunar_date.getLunarDay()
        is_leap = "(闰月)" if calculator.lunar_date.isLunarLeap() else ""
        lunar_date_str = f"{lunar_year}年{lunar_month}月{lunar_day}日{calculator.solar_time.hour:02d}:{calculator.solar_time.minute:02d} {is_leap}"
        solar_date_str = f"{calculator.solar_time.year}年{calculator.solar_time.month}月{calculator.solar_time.day}日{calculator.solar_time.hour:02d}:{calculator.solar_time.minute:02d}"
        birth_time_info = {"农历": lunar_date_str, "公历": solar_date_str}

    result = {
        "姓名": calculator.name,
        "性别": gender_text,
        "出生时间": birth_time_info,
        "出生城市": f"{calculator.birth_city} (经度: {calculator.birth_longitude}°E)",
        "现居城市": calculator.current_city,
        "八字": calculator.ba_zi,
        "节气": calculator.jie_qi_info,
        "大运": calculator.da_yun_info,
    }
    return result


# --- FASTAPI REST ENDPOINT (for HTTP clients & GPT Actions) ---
from fastapi import FastAPI, Query
import uvicorn

app = FastAPI(title="BaZi REST API")

@app.get("/api/bazi")
def get_bazi(
    name: str = Query(...),
    gender: str = Query(..., regex="^(male|female|男|女)$"),
    year: int = Query(...),
    month: int = Query(...),
    day: int = Query(...),
    hour: int = Query(...),
    minute: int = Query(0),
    birth_city: str = Query(...),
):
    # Convert English gender to Chinese
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


if __name__ == "__main__":
    # Run both MCP and FastAPI servers
    import threading

    # Start MCP server in a background thread (for internal AI tools)
    def run_mcp():
        mcp.run(transport="streamable-http")

    threading.Thread(target=run_mcp, daemon=True).start()

    # Start REST API (for HTTP clients)
    port = int(os.environ.get("PORT", "10000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
