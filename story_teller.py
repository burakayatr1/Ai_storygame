from openai import OpenAI
from fastapi import FastAPI
from fastapi.responses import FileResponse
from dotenv import load_dotenv
import os

load_dotenv()

AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
API_KEY = os.getenv("AZURE_API_KEY")
DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME")

client = OpenAI(
    api_key=API_KEY,
    base_url=f"{AZURE_ENDPOINT}",
)

hafiza = [
    {
        "role": "system", 
        "content": """Sen yaratıcı bir macera oyun yöneticisisin. 
        - OYUNUN EN BAŞINDA sadece bir kere 'Grok Macera Dünyasına Hoş Geldin! Sabah uyandın ve dışarı çıktın... Sola git(0)/Sağa git (1) ' cümlesi ile başla.
        - Kullanıcıya her seferinde (1) ve (0) şeklinde iki seçenek sun.
        - Kullanıcı toplamda 3 seçim yapacak. 2. seçimden sonra hikayeyi epik bir finalle bitir ve oyun bitti yaz."""
    }
]
hafiza.append({"role": "assistant", "content": "Grok Macera Dünyasına Hoş Geldin! Sabah uyandın ve dışarı çıktın... Sola git(0)/Sağa git (1) "})

app = FastAPI()
tur_sayaci = 0
@app.post("/story")
def story(input: str):
    global tur_sayaci
    hafiza.append({"role": "user", "content": f"Seçeneğim: {input}"})
    tur_sayaci += 1
    
    response = client.chat.completions.create(
        model=DEPLOYMENT_NAME,
        messages=hafiza,
        temperature=1.0
    )
    grok_yazisi = response.choices[0].message.content
    hafiza.append({"role": "assistant", "content": grok_yazisi})

    return grok_yazisi

@app.get("/")
def main():
    return FileResponse("index.html")

#uvicorn story_teller:app --reload