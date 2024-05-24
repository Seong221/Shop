from fastapi import FastAPI

test_runner = FastAPI()


@test_runner.get("/")
def test():
    return{"message" : "hello"}