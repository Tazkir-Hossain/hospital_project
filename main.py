from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
import os

FILE_PATH = "doctors.txt"

app = FastAPI()


class Doctor(BaseModel):
    id: int
    name: str
    specialty: str
    email: str
    visiting_time: str
    fee: int


def read_doctors():
    if not os.path.exists(FILE_PATH):
        return []
    doctors = []
    with open(FILE_PATH, "r") as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) == 6:
                doc = Doctor(
                    id=int(parts[0]),
                    name=parts[1],
                    specialty=parts[2],
                    email=parts[3],
                    visiting_time=parts[4],
                    fee=int(parts[5])
                )
                doctors.append(doc)
    return doctors


def write_doctors(doctors):
    with open(FILE_PATH, "w") as f:
        for d in doctors:
            f.write(f"{d.id}|{d.name}|{d.specialty}|{d.email}|{d.visiting_time}|{d.fee}\n")


# ------------------------------
#           GET
# ------------------------------

@app.get("/doctors")
def get_all_doctors():
    return read_doctors()


@app.get("/doctors/{doctor_id}")
def get_doctor(doctor_id: int):
    for doc in read_doctors():
        if doc.id == doctor_id:
            return doc
    raise HTTPException(status_code=404, detail="Doctor not found")


# ------------------------------
#           POST  (Authority Only)
# ------------------------------

@app.post("/doctors")
def add_doctor(
    doctor: Doctor,
    x_role: str = Header(default="patient")
):
    if x_role != "authority":
        raise HTTPException(status_code=403, detail="Only authority can add doctors")

    doctors = read_doctors()
    for d in doctors:
        if d.id == doctor.id:
            raise HTTPException(status_code=400, detail="ID already exists")

    doctors.append(doctor)
    write_doctors(doctors)

    return {"message": "Doctor added successfully"}


# ------------------------------
#           PUT  (Authority or Doctor updating self)
# ------------------------------

@app.put("/doctors/{doctor_id}")
def update_doctor(
    doctor_id: int,
    updated: Doctor,
    x_role: str = Header(default="patient"),
    x_doctor_id: int = Header(default=None)
):
    # Patient cannot update
    if x_role == "patient":
        raise HTTPException(status_code=403, detail="Patients cannot update")

    # Doctor can only update their own info
    if x_role == "doctor" and x_doctor_id != doctor_id:
        raise HTTPException(status_code=403, detail="Doctor can only update their own information")

    doctors = read_doctors()
    for i, d in enumerate(doctors):
        if d.id == doctor_id:
            doctors[i] = updated
            write_doctors(doctors)
            return {"message": "Doctor updated"}

    raise HTTPException(status_code=404, detail="Doctor not found")


# ------------------------------
#           DELETE (Authority Only)
# ------------------------------

@app.delete("/doctors/{doctor_id}")
def delete_doctor(
    doctor_id: int,
    x_role: str = Header(default="patient")
):
    if x_role != "authority":
        raise HTTPException(status_code=403, detail="Only authority can delete doctors")

    doctors = read_doctors()
    new_docs = [d for d in doctors if d.id != doctor_id]

    if len(new_docs) == len(doctors):
        raise HTTPException(status_code=404, detail="Doctor not found")

    write_doctors(new_docs)
    return {"message": "Doctor deleted"}
