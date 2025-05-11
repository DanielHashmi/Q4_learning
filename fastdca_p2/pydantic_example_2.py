from pydantic import BaseModel, EmailStr

class Address(BaseModel):
    street: str
    city: str
    zip_code: str


class UserWithAddress(BaseModel):
    id: int
    name: str
    email: EmailStr
    addresses: list[Address]

user_data = {
    "id": 122,
    "name": "Daniel",
    "email": "daniel@gmail.com",
    "addresses": [
        {"street": "Naval Colony st 4", "city": "Karachi", "zip_code": "33332"},
        {"street": "Gulshan-e-Meymar st 6", "city": "Lahore", "zip_code": "23423"},
    ],
}
user = UserWithAddress.model_validate(user_data)
print(user.model_dump())