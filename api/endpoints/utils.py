from fastapi import HTTPException


def raise_exception(code: int, msg: str):
    raise HTTPException(status_code=code, detail=msg)