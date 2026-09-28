import matplotlib.pyplot as plt

employees = {}

DEPARTMENTS = ["Sales", "HR", "IT", "Finance", "Admin"]
FULL_MONTH_DAYS = 30
PF_RATE = 0.12
TAX_RATE = 0.10
OVERTIME_RATE = 150
TASK_BONUS = 1000
SALES_INCENTIVE = 8000

def _record(name, dept, basic, hra, days, x1, x2, x3):
    record = {"name": name, "department": dept, "basic": basic,
              "hra": hra, "days_present": days}
    if dept == "Sales":
        record["sales_target"] = x1
        record["sales_achieved"] = x2
    else:
        record["overtime_hours"] = x1
        record["tasks_assigned"] = x2
        record["tasks_completed"] = x3
    return record

def get_nonEmpty(prompt):
    while True:
        value = input(prompt)
        if value:
            return value
        print("This field cannot be empty.")

def get_float(prompt):
    while True:
        raw = input(prompt)
        try:
            value = float(raw)
        except ValueError:
            print("Please enter a valid number.")
            continue
        if value < 0:
            print("Value cannot be negative.")
            continue
        return value

def get_int(prompt, minimum=0, maximum=None):
    while True:
        raw = input(prompt)
        try:
            value = int(raw)
        except ValueError:
            print("Please enter a whole number.")
            continue
        if value < minimum or (maximum is not None and value > maximum):
            top = maximum if maximum is not None else "any"
            print("Enter a number between", minimum, "and", top)
            continue
        return value

def get_existing_employeeid(prompt):
    while True:
        emp_id = input(prompt).upper()
        if emp_id in employees:
            return emp_id
        print("No employee found with that ID. Try again")

#to add new employee
def addEmployee():
    print("Add New Employee")
    emp_id = get_nonEmpty("  Enter Employee ID: ").upper()
    if emp_id in employees:
        print("  An employee with that ID already exists.")
        return

    name = get_nonEmpty("  Enter Name: ")

    print("  Departments:", ", ".join(DEPARTMENTS))
    while True:
        raw_dept = get_nonEmpty("  Enter Department: ").strip()
        dept_lookup = {d.lower(): d for d in DEPARTMENTS}

        if raw_dept.lower() in dept_lookup:
            dept = dept_lookup[raw_dept.lower()]
            break
        print("  Invalid department. Please choose from the list above.")

    basic = get_float("Enter Basic Salary: ")
    hra = get_float("Enter HRA: ")
    days_present = get_int("Enter Days Present: ", 0, 31)

    if dept == "Sales":
        sales_target = get_float("Enter Sales Target: ")
        sales_achieved = get_float("Enter Sales Achieved: ")
        record = _record(name, dept, basic, hra, days_present,
                         sales_target, sales_achieved, 0)
    else:
        overtime_hours = get_float("Enter Overtime Hours: ")
        tasks_assigned = get_int("Enter Tasks Assigned: ")
        tasks_completed = get_int("Enter Tasks Completed: ")
        record = _record(name, dept, basic, hra, days_present,
                         overtime_hours, tasks_assigned, tasks_completed)

    employees[emp_id] = record
    print("  > Employee added successfully.")

def viewEmployees():
    print("All Employees")
    if not employees:
        print("No employee records found")
        return

    print(f"{'ID':<8}{'Name':<18}{'Department':<12}{'Basic':<10}{'HRA':<10}{'Days Present':<14}")
    print("-" * 74)
    for emp_id, data in employees.items():
        print(f"{emp_id:<8}{data['name']:<18}{data['department']:<12}"
              f"{data['basic']:<10.0f}{data['hra']:<10.0f}{data['days_present']:<14}")

def printEmployee(emp_id, data):
    print(f"\n  ID: {emp_id}")
    for key, value in data.items():
        print(f"  {key.replace('_', ' ').title()}: {value}")

#to search employees by their ID's
def search_employeeId():
    print("Search Employee by ID")
    if not employees:
        print("No employee records found")
        return
    emp_id = get_existing_employeeid("Enter Employee ID to search: ")
    printEmployee(emp_id, employees[emp_id])

#to search employees by their names
def search_employeeName():
    print("Search Employee by Name")
    if not employees:
        print("No employee records found")
        return
    query = get_nonEmpty("  Enter name (or part of it) to search: ").lower()
    matches = [(eid, d) for eid, d in employees.items() if query in d["name"].lower()]
    if not matches:
        print("No matching employee found")
        return
    for emp_id, data in matches:
        print(f"  > Found: {emp_id} - {data['name']} ({data['department']})")
    if len(matches) == 1:
        printEmployee(*matches[0])

def updateEmployee():
    print("Update Employee")
    if not employees:
        print("No employee records found")
        return
    emp_id = get_existing_employeeid("Enter Employee ID to update: ")
    data = employees[emp_id]
    print(f"Updating record for", {data['name']}, ({data['department']}))
    print("Leave a field blank to keep its current value.")

    new_basic = input(f"  Basic Salary (current: {data['basic']}): ")
    if new_basic:
        data["basic"] = float(new_basic)

    new_hra = input(f"  HRA (current: {data['hra']}): ")
    if new_hra:
        data["hra"] = float(new_hra)

    new_days = input(f"  Days Present (current: {data['days_present']}): ")
    if new_days:
        data["days_present"] = int(new_days)

    if data["department"] == "Sales":
        new_achieved = input(f"  Sales Achieved (current: {data['sales_achieved']}): ")
        if new_achieved:
            data["sales_achieved"] = float(new_achieved)
    else:
        new_completed = input(f"  Tasks Completed (current: {data['tasks_completed']}): ")
        if new_completed:
            data["tasks_completed"] = int(new_completed)

    print("  > Employee record updated.")

#to delete employee
def delEmployee():
    print("Delete Employee")
    if not employees:
        print("No employee records found")
        return
    emp_id = get_existing_employeeid("Enter Employee ID to delete: ")
    name = employees[emp_id]["name"]
    confirm = input(f"  Are you sure you want to delete {name}? (y/n): ").lower()
    if confirm == "y":
        del employees[emp_id]
        print("  > Employee record deleted.")
    else:
        print("  Deletion cancelled.")

#to record the employees data
def rec_attendance():
    print(" Record Attendance")
    if not employees:
        print("  No employee records found.")
        return
    emp_id = get_existing_employeeid("  Enter Employee ID: ")
    data = employees[emp_id]
    status = input(f"  Mark {data['name']} present today? (y/n): ").lower()
    if status == "y":
        if data["days_present"] >= 31:
            print("  Days present is already at the monthly maximum.")
        else:
            data["days_present"] += 1
            print(f"  > Marked present. Total days present: {data['days_present']}.")
    else:
        print("  > Marked absent. No change to days present.")

#to view the attendance report of the employees
def view_attendancerep():
    print("Attendance Report")
    if not employees:
        print("No employee records found")
        return
    print(f"{'ID':<8}{'Name':<18}{'Days Present':<14}{'Attendance %':<12}")
    print("-" * 52)
    for emp_id, data in employees.items():
        pct = min(data["days_present"] / FULL_MONTH_DAYS, 1.0) * 100
        print(f"{emp_id:<8}{data['name']:<18}{data['days_present']:<14}{pct:<12.1f}")

#to calculate gross net
def calculate_grossnet(data):
    attendance_ratio = min(data["days_present"] / FULL_MONTH_DAYS, 1.0)
    prorated_base = (data["basic"] + data["hra"]) * attendance_ratio

    if data["department"] == "Sales":
        target = data["sales_target"]
        achieved_ratio = (data["sales_achieved"] / target) if target > 0 else 0
        bonus = achieved_ratio * SALES_INCENTIVE
    else:
        overtime_pay = data["overtime_hours"] * OVERTIME_RATE
        task_bonus = TASK_BONUS if (data["tasks_assigned"] > 0 and
                                    data["tasks_completed"] >= data["tasks_assigned"]) else 0
        bonus = overtime_pay + task_bonus

    gross = prorated_base + bonus
    deductions = gross * (PF_RATE + TAX_RATE)
    net = gross - deductions
    return gross, deductions, net

def cal_sal():
    print("Calculate Salary ")
    if not employees:
        print(" No employee records found")
        return
    emp_id = get_existing_employeeid("  Enter Employee ID: ")
    data = employees[emp_id]
    gross, deductions, net = calculate_grossnet(data)
    print(f"\n  Employee      : {data['name']} ({emp_id})")
    print(f"  Gross Earnings: Rs. {gross:.2f}")
    print(f"  Deductions    : Rs. {deductions:.2f}")
    print(f"  Net Pay       : Rs. {net:.2f}")

def payroll_stats():
    print("Payroll Statistics & Analysis ")
    if not employees:
        print("No employee records found")
        return

    nets = {}
    dept_totals = {}
    for emp_id, data in employees.items():
        _, _, net = calculate_grossnet(data)
        nets[emp_id] = net
        dept_totals[data["department"]] = dept_totals.get(data["department"], 0) + net

    total = sum(nets.values())
    average = total / len(nets)
    highest_id = max(nets, key=nets.get)
    lowest_id = min(nets, key=nets.get)

    print(f"Total Payroll Expense : Rs. {total:.2f}")
    print(f"Average Net Pay       : Rs. {average:.2f}")
    print(f"Highest Paid Employee : {employees[highest_id]['name']} ({highest_id}) - Rs. {nets[highest_id]:.2f}")
    print(f"Lowest Paid Employee  : {employees[lowest_id]['name']} ({lowest_id}) - Rs. {nets[lowest_id]:.2f}")

    print("\n  Department-wise Expense:")
    for dept, amount in dept_totals.items():
        print(f"    {dept:<10}: Rs. {amount:.2f}")

#to display the bar chart
def bar_chart():
    print("Salary Bar Chart (Net Pay)")
    if not employees:
        print("No employee records found")
        return

    nets = {eid: calculate_grossnet(d)[2] for eid, d in employees.items()}

    names = [employees[eid]["name"] for eid in nets]
    values = list(nets.values())

    plt.figure(figsize=(10, 5))
    plt.bar(names, values, color="skyblue")
    plt.xlabel("Employee")
    plt.ylabel("Net Pay (Rs.)")
    plt.title("Salary Bar Chart (Net Pay)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig("salary_bar_chart.jpeg")
    plt.show()

    max_net = max(values) or 1
    for emp_id, net in nets.items():
        bar_len = int((net / max_net) * 40)
        print(f"  {employees[emp_id]['name']:<18}| {'#' * bar_len} Rs.{net:.0f}")

#to show the employee of the month
def employee_of_the_month():
    print(" Employee of the Month ")
    if not employees:
        print("No employee records found")
        return

    best_id, best_score = None, -1
    for emp_id, data in employees.items():
        if data["department"] == "Sales":
            score = (data["sales_achieved"] / data["sales_target"]) if data["sales_target"] > 0 else 0
        else:
            score = (data["tasks_completed"] / data["tasks_assigned"]) if data["tasks_assigned"] > 0 else 0
        if score > best_score:
            best_id, best_score = emp_id, score

    data = employees[best_id]
    print(f"  {data['name']} ({best_id}) - {data['department']} - Performance: {best_score * 100:.1f}%")

def sort_employees_sal():
    print(" Sort Employees by Net Salary")
    if not employees:
        print("No employee records found")
        return
    order = input("  Sort (a)scending or (d)escending? ").lower()
    ranked = sorted(employees.items(), key=lambda item: calculate_grossnet(item[1])[2],
                    reverse=(order == "d"))
    for emp_id, data in ranked:
        net = calculate_grossnet(data)[2]
        print(f"  {emp_id:<8}{data['name']:<18}Rs. {net:.2f}")

def payroll_rep():
    print(" Full Payroll Report ")
    if not employees:
        print("  No employee records found.")
        return
    print(f"{'ID':<8}{'Name':<18}{'Dept':<10}{'Gross':<12}{'Deductions':<12}{'Net Pay':<12}")
    print("-" * 72)
    for emp_id, data in employees.items():
        gross, deductions, net = calculate_grossnet(data)
        print(f"{emp_id:<8}{data['name']:<18}{data['department']:<10}"
              f"{gross:<12.2f}{deductions:<12.2f}{net:<12.2f}")

def gen_payslip():
    print("Generate Payslip")
    if not employees:
        print("No employee records found")
        return
    emp_id = get_existing_employeeid("  Enter Employee ID: ")
    data = employees[emp_id]
    gross, deductions, net = calculate_grossnet(data)

    print("=" * 40)
    print("PAYSLIP".center(40))
    print("=" * 40)
    print(f"Employee ID   : {emp_id}")
    print(f"Name          : {data['name']}")
    print(f"Department    : {data['department']}")
    print(f"Days Present  : {data['days_present']}")
    print("-" * 40)
    print(f"Gross Earnings: Rs. {gross:>12.2f}")
    print(f"Deductions    : Rs. {deductions:>12.2f}")
    print("-" * 40)
    print(f"NET PAY       : Rs. {net:>12.2f}")
    print("=" * 40)

MENU_ACTIONS = {
    "1": viewEmployees,
    "2": search_employeeId,
    "3": updateEmployee,
    "4": delEmployee,
    "5": rec_attendance,
    "6": view_attendancerep,
    "7": cal_sal,
    "8": payroll_stats,
    "9": bar_chart,
    "10": employee_of_the_month,
    "11": sort_employees_sal,
    "12": search_employeeName,
    "13": payroll_rep,
    "14": gen_payslip,
    "15": addEmployee,
}

def print_menu():
    print("\n" + "=" * 50)
    print("EMPLOYEE PAYROLL MANAGEMENT SYSTEM".center(50))
    print("=" * 50)
    labels = [
        "View All Employees", "Search Employee by ID",
        "Update Employee", "Delete Employee", "Record Attendance",
        "View Attendance Report", "Calculate Salary (Individual)",
        "Payroll Statistics & Analysis", "Salary Bar Chart",
        "Employee of the Month", "Sort Employees by Salary",
         "Search Employee by Name","Full Payroll Report", "Generate Payslip", "Add New Employee",
    ]
    for i, label in enumerate(labels, start=1):
        print(f"{i:>2}.  {label}")
    print(" 0.  Exit")
    print("=" * 50)

def main():
    while True:
        print_menu()
        choice = input("Enter your choice: ")
        if choice == "0":
            print("Thank you for using the Payroll Management System. Goodbye!")
            break
        action = MENU_ACTIONS.get(choice)
        if action:
            action()
        else:
            print("  Invalid choice. Please select a valid menu option.")

if __name__ == "__main__":
    main()