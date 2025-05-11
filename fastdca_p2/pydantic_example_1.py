from pydantic import BaseModel, ValidationError

class User(BaseModel):
    id: int
    name: str
    email: str
    age: int | None = None

user_data = {"id": 112, "name": "Daniel", "email": "daniel@gmail.com", "age": 18}
user = User(**user_data)
print(user)
print(user.model_dump())

try:
    invalid_user = User(id="iam_a_sneaky_number", name="Hashmi", email="hashmi@gmail.com")
except ValidationError as e:
    print(e)