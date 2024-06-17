from fastapi import FastAPI

app = FastAPI(__name__)


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
