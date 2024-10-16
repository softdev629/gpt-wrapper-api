from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
import os
from prompts import SOURCE_VERIFY_PROMPT, DETAIL_VERIFY_PROMPT, FACTUAL_VERIFY_PROMPT

load_dotenv()

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://165.227.93.171:3000",
    "https://verifycontent.cc/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def main():
    return {"message": "Hello World"}


class ISigninRequest(BaseModel):
    email: str
    password: str


@app.post("/api/signin")
async def signin_handler(req: ISigninRequest):
    if req.password == "thriveteam2025":
        return {"logged_in": True}
    return {"logged_in": False}


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@app.post("/api/verify/source")
async def verify_source_handler(text: str = Body(embed=True)):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": SOURCE_VERIFY_PROMPT,
            },
            {
                "role": "user",
                "content": f"Review the following content as specified in the system.\n\n<content>{text}</content>",
            },
        ],
    )
    return {"result": completion.choices[0].message.content}


@app.post("/api/verify/detail")
async def verify_detail_handler(text: str = Body(embed=True)):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": DETAIL_VERIFY_PROMPT,
            },
            {
                "role": "user",
                "content": f"Review the following content as specified in the system.\n\n<content>{text}</content>",
            },
        ],
    )
    return {"result": completion.choices[0].message.content}


@app.post("/api/verify/factual")
async def verify_factual_handler(text: str = Body(embed=True)):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": FACTUAL_VERIFY_PROMPT,
            },
            {
                "role": "user",
                "content": f"Review the following content as specified in the system.\n\n<content>{text}</content>",
            },
        ],
    )
    return {"result": completion.choices[0].message.content}
