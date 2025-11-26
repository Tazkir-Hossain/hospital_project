import requests

BASE_URL = "http://127.0.0.1:8000"

# -------------------------------
# Helper Functions
# -------------------------------

def show_all():
    r = requests.get(f"{BASE_URL}/doctors")
    print("\nAll Doctors:")
    for d in r.json():
        print(d)


def show_one():
    doctor_id = int(input("Enter doctor ID: "))
    r = requests.get(f"{BASE_URL}/doctors/{doctor_id}")
    print(r.json())


def add_doctor():
    print("\nEnter new doctor details:")
    doc = {
        "id": int(input("ID: ")),
        "name": input("Name: "),
        "specialty": input("Specialty: "),
        "email": input("Email: "),
        "visiting_time": input("Visiting Time: "),
        "fee": int(input("Fee: "))
    }

    headers = {"X-ROLE": "authority"}
    r = requests.post(f"{BASE_URL}/doctors", json=doc, headers=headers)
    print(r.json())


def update_doctor(role, my_id=None):
    doctor_id = int(input("Enter doctor ID to update: "))

    if role == "doctor" and doctor_id != my_id:
        print("\n❌ You can only update your own profile!")
        return

    print("\nEnter updated details:")
    doc = {
        "id": doctor_id,
        "name": input("Name: "),
        "specialty": input("Specialty: "),
        "email": input("Email: "),
        "visiting_time": input("Visiting Time: "),
        "fee": int(input("Fee: "))
    }

    headers = {"X-ROLE": role}
    if role == "doctor":
        headers["X-DOCTOR-ID"] = str(my_id)

    r = requests.put(f"{BASE_URL}/doctors/{doctor_id}", json=doc, headers=headers)
    print(r.json())


def delete_doctor():
    doctor_id = int(input("Enter doctor ID to delete: "))
    headers = {"X-ROLE": "authority"}
    r = requests.delete(f"{BASE_URL}/doctors/{doctor_id}", headers=headers)
    print(r.json())


# -------------------------------
# Mode Systems
# -------------------------------

def authority_mode():
    while True:
        print("\n--- AUTHORITY MODE ---")
        print("1. View All Doctors")
        print("2. View Doctor by ID")
        print("3. Add Doctor")
        print("4. Update Doctor")
        print("5. Delete Doctor")
        print("6. Exit")

        c = input("Choose: ")

        if c == "1":
            show_all()
        elif c == "2":
            show_one()
        elif c == "3":
            add_doctor()
        elif c == "4":
            update_doctor(role="authority")
        elif c == "5":
            delete_doctor()
        elif c == "6":
            break
        else:
            print("Invalid choice!")


def doctor_mode():
    my_id = int(input("\nEnter YOUR doctor ID: "))

    while True:
        print("\n--- DOCTOR MODE ---")
        print("1. View All Doctors")
        print("2. View Doctor by ID")
        print("3. Update Your Information")
        print("4. Exit")

        c = input("Choose: ")

        if c == "1":
            show_all()
        elif c == "2":
            show_one()
        elif c == "3":
            update_doctor(role="doctor", my_id=my_id)
        elif c == "4":
            break
        else:
            print("Invalid choice!")


def patient_mode():
    while True:
        print("\n--- PATIENT MODE ---")
        print("1. View All Doctors")
        print("2. View Doctor by ID")
        print("3. Exit")

        c = input("Choose: ")

        if c == "1":
            show_all()
        elif c == "2":
            show_one()
        elif c == "3":
            break
        else:
            print("Invalid choice!")


# -------------------------------
# Entry Point
# -------------------------------

if __name__ == "__main__":
    while True:
        print("\n======= MAIN MENU =======")
        print("1. Authority")
        print("2. Doctor")
        print("3. Patient")
        print("4. Exit")

        choice = input("Choose mode: ")

        if choice == "1":
            authority_mode()
        elif choice == "2":
            doctor_mode()
        elif choice == "3":
            patient_mode()
        elif choice == "4":
            break
        else:
            print("Invalid option!")
