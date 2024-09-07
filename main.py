import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates

from utils import (generate_image_from_rgba, generate_random_hex, generate_rgba_from_hex, generate_rgba_from_rgb,
                   generate_rgba_from_rgba, generate_rgba_from_hsl, rgba_to_hex)

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/favicon.ico", response_class=StreamingResponse)
async def get_favicon():
    hex_color = generate_random_hex()
    try:
        rgba = generate_rgba_from_hex(hex_color)
    except ValueError as e:
        return HTMLResponse(content=f"Invalid hex value: {str(e)}", status_code=400)
    image_io = generate_image_from_rgba(rgba, 1, True)
    return StreamingResponse(image_io, media_type="image/png")


@app.get("/favicon/{hex}", response_class=StreamingResponse)
async def get_favicon(hex: str):
    rgba = generate_rgba_from_hex(hex)
    image_io = generate_image_from_rgba(rgba, 1, True)
    return StreamingResponse(image_io, media_type="image/png")


@app.get("/hex/{hex_code}", response_class=HTMLResponse)
async def get_hex(request: Request, hex_code: str):
    try:
        rgba = generate_rgba_from_hex(hex_code)
    except ValueError as e:
        return HTMLResponse(content=f"Invalid hex value: {str(e)}", status_code=400)
    image_base64 = generate_image_from_rgba(rgba, 1, False)
    return templates.TemplateResponse("urls_template.html",
                                      {"request": request, "image_data": image_base64,
                                       "code": rgba_to_hex(rgba)})


@app.get("/rgb/{rgb_code}", response_class=HTMLResponse)
async def get_rgb_color(request: Request, rgb_code: str):
    try:
        rgba = generate_rgba_from_rgb(rgb_code)
    except ValueError as e:
        return HTMLResponse(f"Invalid RGB color code: {str(e)}", status_code=400)

    image_base64 = generate_image_from_rgba(rgba, 1, False)
    return templates.TemplateResponse("urls_template.html",
                                      {"request": request, "image_data": image_base64,
                                       "code": rgba_to_hex(rgba)})


@app.get("/rgba/{rgba_code}", response_class=HTMLResponse)
async def get_rgba_color(request: Request, rgba_code: str):
    try:
        rgba = generate_rgba_from_rgba(rgba_code)
    except ValueError as e:
        return HTMLResponse(f"Invalid RGBA color code: {str(e)}", status_code=400)

    image_base64 = generate_image_from_rgba(rgba, 1, False)
    return templates.TemplateResponse("urls_template.html",
                                      {"request": request, "image_data": image_base64,
                                       "code": rgba_to_hex(rgba)})


@app.get("/hsl/{hsl_code}", response_class=HTMLResponse)
async def get_hsl_color(request: Request, hsl_code: str):
    try:
        rgba = generate_rgba_from_hsl(hsl_code)
    except ValueError as e:
        return HTMLResponse(f"Invalid HSL color code: {str(e)}", status_code=400)

    image_base64 = generate_image_from_rgba(rgba, 1, False)
    return templates.TemplateResponse("urls_template.html",
                                      {"request": request, "image_data": image_base64,
                                       "code": rgba_to_hex(rgba)})


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8383, log_level="info", reload=True
                )  # uvicorn.run("main:app", host="0.0.0.0", port=8383, log_level="info", workers=4)
