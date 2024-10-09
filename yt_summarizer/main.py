import json
import logging

from fastapi import FastAPI, Request, Response

from yt_summarizer.service.yt_helper import YTHelper

app = FastAPI()
logger = logging.getLogger("uvicorn")


@app.post("/smr")
async def smr(request: Request):
    body = await request.body()
    body_str = body.decode("utf-8")

    try:
        body_dict = json.loads(body_str)
        logger.info(f"Converted body to dict: {body_dict}, type: {type(body_dict)}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return {"error": "An error occurred"}

    obj = YTHelper.extract_info(body_dict.get("url"))
    test = (
        {"message": f"{obj.title}"} if obj is not None else {"message": "Invalid URL"}
    )

    return Response(content=json.dumps(test), media_type="application/json")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
