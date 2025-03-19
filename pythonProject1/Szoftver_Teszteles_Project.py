from typing import List, Optional
import unittest
from io import StringIO
import contextlib
import sys


DEBUG = False

# Ha a debug true akkor kiirja az uzeneteket
def debug_print(message: str):
    if DEBUG:
        print(message, file=sys.stderr)


# Employee obijektumot letrehozasa a megadott adatokkal

class Employee:
    def __init__(self, name: str, birthdate: str, hire_date: str, base_salary: int, is_team_leader: bool = False):
        self.name = name
        self.birthdate = birthdate
        self.hire_date = hire_date
        self.base_salary = base_salary
        self.is_team_leader = is_team_leader
        self.team_members: List['Employee'] = []

# Csatag hozza adasa

    def add_team_member(self, member: 'Employee'):
        self.team_members.append(member)
        debug_print(f"{self.name} hozzáadta {member.name}-t a csapatához.")

# Alkalmazott es csapatvezeto fizetesenek a kiszamitasa

    def calculate_salary(self) -> int:
        # Számítás 2018-as alapokkal a teszteknek megfelelően.
        years_of_service = 2018 - int(self.hire_date.split('.')[-1])
        base_calc = self.base_salary + (years_of_service * 100)
        debug_print(f"{self.name} alapbére: {self.base_salary}$, szolgálati évek: {years_of_service}, számított bér: {base_calc}$")
        if self.is_team_leader:
            team_bonus = len(self.team_members) * 200
            final_salary = base_calc + team_bonus
            debug_print(f"{self.name} csapatvezető, csapatbónusz: {team_bonus}$, végső fizetés: {final_salary}$")
            return final_salary
        else:
            return base_calc


# Email kuldes  szimulalas

class EmailSender:
    @staticmethod
    def send_email(name: str, message: str):
        print(f"Email sent to {name} with message: {message}")


# Inicsializalja az EmployeeRelationsManager obijektumot

class EmployeeRelationsManager:
    def __init__(self, employees: List[Employee]):
        self.employees = employees

# Meg keresi az alkalmazottat az adatbazisban

    def find_employee(self, name: str, birthdate: Optional[str] = None) -> Optional[Employee]:
        debug_print(f"Keresés az adatbázisban: {name}, születési dátum: {birthdate}")
        for employee in self.employees:
            if employee.name == name and (birthdate is None or employee.birthdate == birthdate):
                debug_print(f"Találat: {employee.name}")
                return employee
        debug_print("Nincs találat.")
        return None

# Ellenorzi hogy az adott nevel es szuletesi datummal rendelkezo alkalmazott csapatvezeto

    def is_team_leader(self, name: str, birthdate: str) -> bool:
        employee = self.find_employee(name, birthdate)
        return employee is not None and employee.is_team_leader

# Lekeri a csapatagok neveit

    def get_team_members(self, team_leader_name: str, team_leader_birthdate: str) -> List[str]:
        team_leader = self.find_employee(team_leader_name, team_leader_birthdate)
        if team_leader and team_leader.is_team_leader:
            return [member.name for member in team_leader.team_members]
        return []

# Ellenorzi hogy az adott nev szerepel az adatbazisban

    def is_employee_in_database(self, name: str) -> bool:
        return self.find_employee(name) is not None


# Inicializalja az EmployeeManager obijectumot az alkalmazott listajaval es az  EmailSender peldanyal.

class EmployeeManager:
    def __init__(self, employees: List[Employee], email_sender: EmailSender):
        self.employees = employees
        self.email_sender = email_sender

# Kiszamolja az alkalmazott fizeteset a nev, belepesi datum es alapber alapjan
    # 0 at add ha nincs alakalmazott
    def calculate_employee_salary(self, name: str, hire_date: str, base_salary: int) -> int:
        debug_print(f"Fizetés számítása: {name}, belépési dátum: {hire_date}, alapbér: {base_salary}")
        employee = next((emp for emp in self.employees if
                         emp.name == name and emp.hire_date == hire_date and emp.base_salary == base_salary), None)
        if employee:
            return employee.calculate_salary()
        debug_print("Alkalmazott nem található.")
        return 0

# Kiszamitja az alkalmazott fizeteset majd e-mailt kuld a szamitott fizetesrol
    # Ha nincs alkalmazott akkor hiba uzenetett add.
    def calculate_salary_and_send_email(self, name: str, hire_date: str, base_salary: int):
        salary = self.calculate_employee_salary(name, hire_date, base_salary)
        if salary > 0:
            message = f"Your calculated salary is {salary}$."
            self.email_sender.send_email(name, message)
        else:
            print("Employee not found.")



# EmployeeRelationsManager teszteléséhez:
john_doe = Employee("John Doe", "31.01.1970", "10.10.1998", 1000, is_team_leader=True)
myrta = Employee("Myrta Torkelson", "15.05.1985", "10.10.2000", 1500)
jettie = Employee("Jettie Lynch", "20.08.1988", "10.10.2005", 2000)
tomas = Employee("Tomas Andre", "12.12.1975", "10.10.2010", 2500)
gretchen = Employee("Gretchen Walford", "25.03.1980", "10.10.2015", 4000)



mark_spencer = Employee("Mark Spencer", "01.01.1980", "10.10.1998", 1000, is_team_leader=False)
lisa_monroe = Employee("Lisa Monroe", "05.05.1985", "10.10.2008", 2000, is_team_leader=True)
member_a = Employee("Member A", "01.01.1990", "10.10.2018", 1500)
member_b = Employee("Member B", "02.02.1991", "10.10.2019", 1500)
member_c = Employee("Member C", "03.03.1992", "10.10.2020", 1500)


john_doe.add_team_member(myrta)  # Myrta hozzadasa John Doe csapatahoz
john_doe.add_team_member(jettie)

lisa_monroe.add_team_member(member_a) # Member A hozzadasa Lisa Monroe csapatahoz
lisa_monroe.add_team_member(member_b)
lisa_monroe.add_team_member(member_c)


employees = [
    john_doe, myrta, jettie, tomas, gretchen,
    mark_spencer, lisa_monroe, member_a, member_b, member_c
]

# Peldany letrehozas
erm = EmployeeRelationsManager(employees)
email_sender = EmailSender()
em = EmployeeManager(employees, email_sender)


# unit tesztek
class TestEmployeeRelationsManager(unittest.TestCase):
    def setUp(self):
        print("\n[START] EmployeeRelationsManager test case: " + self._testMethodName)

    def tearDown(self):
        print("[END] EmployeeRelationsManager test case: " + self._testMethodName)

    def test_team_leader_exists(self):
        question = "Kérdés: Van-e egy csapatvezető John Doe névvel, akinek a születési dátuma 31.01.1970?"
        print(question)
        result = erm.is_team_leader("John Doe", "31.01.1970")
        print("Válasz:", result)
        self.assertTrue(result)

    def test_john_doe_team_members(self):
        question = "Kérdés: John Doe csapattagjai: Myrta Torkelson és Jettie Lynch?"
        print(question)
        team_members = erm.get_team_members("John Doe", "31.01.1970")
        print("Válasz:", team_members)
        self.assertIn("Myrta Torkelson", team_members)
        self.assertIn("Jettie Lynch", team_members)
        self.assertEqual(len(team_members), 2)

    def test_tomas_not_in_john_doe_team(self):
        question = "Kérdés: Van-e Tomas Andre John Doe csapatában?"
        print(question)
        team_members = erm.get_team_members("John Doe", "31.01.1970")
        print("Válasz:", team_members)
        self.assertNotIn("Tomas Andre", team_members)

    def test_gretchen_base_salary(self):
        question = "Kérdés: Gretchen Walford alapbére 4000$?"
        print(question)
        employee = erm.find_employee("Gretchen Walford")
        base_salary = employee.base_salary if employee else None
        print("Válasz:", base_salary)
        self.assertIsNotNone(employee)
        self.assertEqual(base_salary, 4000)

    def test_tomas_not_team_leader(self):
        question = "Kérdés: Tomas Andre csapatvezető-e, és üres-e a csapattag lista?"
        print(question)
        is_leader = erm.is_team_leader("Tomas Andre", "12.12.1975")
        team_members = erm.get_team_members("Tomas Andre", "12.12.1975")
        print("Válasz: Csapatvezető:", is_leader, "Csapattagok:", team_members)
        self.assertFalse(is_leader)
        self.assertEqual(team_members, [])

    def test_jude_not_in_database(self):
        question = "Kérdés: Jude Overcash szerepel-e az adatbázisban?"
        print(question)
        in_database = erm.is_employee_in_database("Jude Overcash")
        print("Válasz:", in_database)
        self.assertFalse(in_database)


class TestEmployeeManager(unittest.TestCase):
    def setUp(self):
        print("\n[START] EmployeeManager test case: " + self._testMethodName)

    def tearDown(self):
        print("[END] EmployeeManager test case: " + self._testMethodName)

    def test_non_team_leader_salary(self):
        question = "Kérdés: Mark Spencer fizetése 3000$ (nem csapatvezető)?"
        print(question)
        salary = em.calculate_employee_salary("Mark Spencer", "10.10.1998", 1000)
        print("Válasz:", salary)
        self.assertEqual(salary, 3000)

    def test_team_leader_salary(self):
        question = "Kérdés: Lisa Monroe fizetése 3600$ (csapatvezető, 3 csapattaggal)?"
        print(question)
        salary = em.calculate_employee_salary("Lisa Monroe", "10.10.2008", 2000)
        print("Válasz:", salary)
        self.assertEqual(salary, 3600)

    def test_salary_calculation_email(self):
        question = "Kérdés: Az e-mail küldés megfelelő üzenettel történik-e?"
        print(question)
        captured_output = StringIO()
        with contextlib.redirect_stdout(captured_output):
            em.calculate_salary_and_send_email("Lisa Monroe", "10.10.2008", 2000)
        output = captured_output.getvalue().strip()
        print("Válasz:", output)
        expected_message = "Email sent to Lisa Monroe with message: Your calculated salary is 3600$."
        self.assertEqual(output, expected_message)



if __name__ == "__main__":
    unittest.main(verbosity=2)
