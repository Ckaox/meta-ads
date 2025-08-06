from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from playwright.async_api import async_playwright
import uvicorn

app = FastAPI()

@app.get("/get_page_id")
async def get_page_id(fb_url: str = Query(..., description="Facebook page URL")):
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            await page.goto(fb_url, timeout=30000)
            await page.wait_for_timeout(3000)

            html = await page.content()

            # Buscar el "pageID" en el HTML
            import re
            match = re.search(r'"pageID":"(\d+)"', html)
            if match:
                page_id = match.group(1)
                return {"success": True, "page_id": page_id}
            else:
                return JSONResponse(status_code=404, content={"success": False, "error": "Page ID not found"})

    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
