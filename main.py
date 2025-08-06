from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from playwright.async_api import async_playwright
import uvicorn
import re

app = FastAPI()

@app.get("/check_page_ads")
async def check_page_ads(fb_url: str = Query(..., description="Facebook page URL")):
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            # Entrar a Facebook y extraer el pageID
            await page.goto(fb_url, timeout=30000)
            await page.wait_for_timeout(3000)
            html = await page.content()
            match = re.search(r'"pageID":"(\d+)"', html)

            if not match:
                return JSONResponse(status_code=404, content={"success": False, "error": "Page ID not found"})

            page_id = match.group(1)

            # Buscar en la AdLibrary con el ID extraido
            ad_library_url = f"https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=ES&view_all_page_id={page_id}"
            await page.goto(ad_library_url, timeout=30000)
            await page.wait_for_timeout(4000)
            ad_html = await page.content()

            # Verificar si tiene anuncios activos
            ads_active = "Ad started" in ad_html
            ads_count = len(re.findall(r"Ad started", ad_html))

            await browser.close()

            return {
                "success": True,
                "page_id": page_id,
                "ads_active": ads_active,
                "ads_count": ads_count
            }

    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
