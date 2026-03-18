from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.analysis import verse_analysis, letter_analysis, word_search
from app.analysis import muqattaat_analysis

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/verse", response_class=HTMLResponse)
def verse_page(request: Request):
    return templates.TemplateResponse("verse.html", {"request": request})


@app.post("/verse", response_class=HTMLResponse)
def verse_analyze(request: Request, surah: int = Form(...), ayah: int = Form(...)):

    result = verse_analysis(surah, ayah)

    return templates.TemplateResponse(
        "verse.html",
        {"request": request, "result": result}
    )


@app.get("/letter", response_class=HTMLResponse)
def letter_page(request: Request):
    return templates.TemplateResponse("letter.html", {"request": request})


@app.post("/letter", response_class=HTMLResponse)
def letter_analyze(request: Request, letter: str = Form(...), surah: int = Form(...)):

    result = letter_analysis(letter, surah)

    return templates.TemplateResponse(
        "letter.html",
        {"request": request, "result": result}
    )


@app.get("/word", response_class=HTMLResponse)
def word_page(request: Request):
    return templates.TemplateResponse("word.html", {"request": request})


@app.post("/word", response_class=HTMLResponse)
def word_analyze(request: Request, word: str = Form(...)):

    results, total = word_search(word)

    return templates.TemplateResponse(
        "word.html",
        {"request": request, "results": results, "total": total}
    )


@app.get("/muqattaat", response_class=HTMLResponse)
def muqattaat_page(request: Request):

    results = muqattaat_analysis()

    return templates.TemplateResponse(
        "muqattaat.html",
        {
            "request": request,
            "results": results
        }
    )