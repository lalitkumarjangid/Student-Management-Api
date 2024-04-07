from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel, Field
from pymongo import MongoClient
from bson import ObjectId
import os
import uvicorn

app = FastAPI()

# Connect to MongoDB
def get_db():
    client = MongoClient(os.getenv("MONGODB_URI"))
    return client["library_management"]["students"]

class Address(BaseModel):
    city: str
    country: str

class Student(BaseModel):
    id: str = Field(default=None, alias="id")
    name: str
    age: int
    address: Address

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "name": "John Doe",
                "age": 20,
                "address": {
                    "city": "New York",
                    "country": "USA"
                }
            }
        }

@app.post("/api/students", status_code=201, response_model=Student)
async def create_student(student: Student = Body(...)):
    collection = get_db()
    student = student.dict(by_alias=True)  # Use by_alias=True to include aliases
    result = collection.insert_one(student)
    student["_id"] = str(result.inserted_id)
    return student

@app.patch("/api/students/{id}", response_model=Student)
async def update_student(id: str, student: Student = Body(...)):
    collection = get_db()
    student = student.dict(by_alias=True, exclude_unset=True)  # Use by_alias=True to include aliases
    result = collection.update_one({"_id": ObjectId(id)}, {"$set": student})
    if result.modified_count == 1:
        return collection.find_one({"_id": ObjectId(id)})
    else:
        raise HTTPException(status_code=404, detail="Student not found")

@app.get("/api/students", response_model=list[Student])
async def list_students(country: str = None, age: int = None):
    collection = get_db()
    query = {}
    if country:
        query["address.country"] = country
    if age:
        query["age"] = {"$gte": age}
    students = list(collection.find(query))
    for student in students:
        student["_id"] = str(student["_id"])
    return students

@app.get("/api/students/{id}", response_model=Student)
async def get_student(id: str):
    collection = get_db()
    student = collection.find_one({"_id": ObjectId(id)})
    if student:
        student["_id"] = str(student["_id"])
        return student
    else:
        raise HTTPException(status_code=404, detail="Student not found")



@app.delete("/api/students/{id}", status_code=204)
async def delete_student(id: str):
    collection = get_db()
    result = collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count != 1:
        raise HTTPException(status_code=404, detail="Student not found")

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000)