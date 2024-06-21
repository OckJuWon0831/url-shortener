from fastapi import HTTPException


def raise_bad_request(message):
    raise HTTPException(status_code=400, detail=message)


# 키가 존재하지 않는 경우
def raise_not_found(request, message=None):
    message = message or f"URL '{request.url}' doesn't exist"
    raise HTTPException(status_code=404, detail=message)
