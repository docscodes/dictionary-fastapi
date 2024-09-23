from typing import List, Optional
from fastapi import FastAPI, Query
from fastapi.encoders import jsonable_encoder
from model.dbHandler import match_exact, match_like

app = FastAPI()


@app.get("/")
def index():
  response = {"usage": "/dict?=<word>"}
  return jsonable_encoder(response)


@app.get("/dict")
def dictionary(word: str):
  if not word:
    response = {"status": "error", "word": word, "data": "word not found"}
    return jsonable_encoder(response)

  definitions = match_exact(word)
  if definitions:
    response = {"status": "success", "word": word, "data": definitions}
    return jsonable_encoder(response)

  definitions = match_like(word)
  if definitions:
    response = {"status": "partial", "word": word, "data": definitions}
    return jsonable_encoder(response)
  else:
    response = {"status": "error", "word": word, "data": "word not found"}
    return jsonable_encoder(response)


@app.get("/dict_list")
def dictionary_list(words: List[str] = Query(None)):
  if not words:
    response = {"status": "error", "word": words, "data": "word not found"}
    return jsonable_encoder(response)

  response = {"words": []}

  for word in words:
    definitions = match_exact(word)
    if definitions:
      response["words"].append(
          {"status": "success", "word": word, "data": definitions})
    else:
      definitions = match_like(word)
      if definitions:
        response["words"].append(
            {"status": "partial", "word": word, "data": definitions})
      else:
        response[words].append(
            {"status": "error", "word": word, "data": "word not found"})

  return jsonable_encoder(response)
