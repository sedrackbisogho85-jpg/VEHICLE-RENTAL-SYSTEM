# Vehicle Rental Management System

A menu-driven, command-line program written in **Python** that manages a small vehicle rental business. It lets you register customers, add vehicles, rent and return them, search records, view rental history and compare prices.

The project was built by **Group 3** as an **Object-Oriented Programming (OOP)** assignment. Its main goal is to show clearly where and how the core OOP concepts are used:

- Abstraction
- Inheritance
- Polymorphism
- Encapsulation
- Object collaboration (classes working together)
- Validation and error handling

All code is in a single file: `vehiche.py`.

---

## Table of Contents

1. [Features](#features)
2. [Requirements](#requirements)
3. [How to Run](#how-to-run)
4. [The Menu](#the-menu)
5. [Pricing Rules](#pricing-rules)
6. [Project Structure](#project-structure)
7. [Class Guide](#class-guide)
8. [OOP Concepts Explained](#oop-concepts-explained)
9. [Validation and Error Handling](#validation-and-error-handling)
10. [How a Rental Works (Step by Step)](#how-a-rental-works-step-by-step)
11. [Example Session](#example-session)
12. [Sample Data](#sample-data)
13. [Limitations](#limitations)
14. [Possible Improvements](#possible-improvements)
15. [Team](#team)

---

## Features

- Register customers with a unique ID, name and phone number
- Add three types of vehicles: **Car**, **Motorcycle** and **Van**
- Prevent duplicate customer IDs and duplicate registration numbers
- Rent a vehicle to a customer for a number of days
- Prevent a vehicle from being rented twice at the same time
- Return a vehicle and automatically calculate the final cost
- Display all available vehicles
- Display all currently rented vehicles
- Search for a customer or a vehicle
- View a customer's full rental history and total amount spent
- View a summary of the whole business (customers, vehicles, rentals, revenue)
- Compare the price of every vehicle for the same number of days
- Load sample data for quick testing
- Friendly error messages instead of program crashes

---

## Requirements

- **Python 3.6 or newer** (the program uses f-strings)
- No external libraries. It only uses Python's built-in modules:
  - `abc` for abstract classes
  - `datetime` for reading and comparing dates

---

## How to Run

1. Save the file as `vehiche.py`.
2. Open a terminal or command prompt in the folder that contains the file.
3. Run:

```bash
python vehiche.py
```

On some systems you may need to use `python3` instead:

```bash
python3 vehiche.py
```

The menu will appear and wait for your choice. Type a number from 1 to 13 and press **Enter**.

---

## The Menu

| No. | Option | What it does |
|----|--------|--------------|
| 1 | Register Customer | Asks for ID, name and phone, then saves the customer |
| 2 | Add Vehicle | Choose the type (Car, Motorcycle or Van), then enter registration number, make and model |
| 3 | Display Available Vehicles | Lists all vehicles that are free to rent |
| 4 | Display Rented Vehicles | Lists vehicles currently rented out, with the customer and rental date |
| 5 | Rent Vehicle | Rents a vehicle to a customer and shows an estimated cost |
| 6 | Return Vehicle | Returns a vehicle and shows the days charged and the final cost |
| 7 | Search Customer | Finds a customer by ID |
| 8 | Search Vehicle | Finds a vehicle by registration number |
| 9 | View Customer Rental History | Shows all of a customer's rentals and the total spent |
| 10 | View Rental Summary | Shows totals for customers, vehicles, rentals and revenue |
| 11 | Compare Prices (Polymorphism) | Shows the cost of every vehicle for a number of days |
| 12 | Load Sample Data | Adds 2 customers and 3 vehicles for testing |
| 13 | Exit | Closes the program |

---

## Pricing Rules

Each vehicle type has its own way of calculating the rental cost.

| Vehicle | Formula | Example (3 days) |
|---------|---------|------------------|
| Car | 50 x days | 150 |
| Motorcycle | 25 x days | 75 |
| Van | 80 x days + 30 (fixed insurance fee) | 270 |

Two costs are calculated:

- **Estimated cost:** worked out when the rental is created, using the number of days the customer asked for.
- **Final cost:** worked out when the vehicle is returned, using the **real** number of days between the rental date and the return date.

**Important billing rule:** a rental is always charged for **at least 1 day**, even if the vehicle is returned on the same date it was rented.

---

## Project Structure

The file is organised into clear sections:

```
vehiche.py
|
|-- Imports (abc, datetime)
|
|-- VEHICLE CLASSES
|     |-- Vehicle        (abstract parent class)
|     |-- Car            (child of Vehicle)
|     |-- Motorcycle     (child of Vehicle)
|     |-- Van            (child of Vehicle)
|
|-- CUSTOMER CLASS
|     |-- Customer
|
|-- RENTAL CLASS
|     |-- Rental
|
|-- RENTAL SYSTEM (the manager class)
|     |-- RentalSystem
|
|-- MENU / USER INTERFACE FUNCTIONS
|     |-- read_text, read_number, read_date   (input helpers)
|     |-- show_menu and one function per menu option
|
|-- MAIN PROGRAM LOOP
      |-- main()
```

### Class relationships

```
              Vehicle (abstract)
             /      |        \
          Car  Motorcycle    Van          <- inheritance

  Customer  <----  Rental  ---->  Vehicle   <- a Rental links one customer to one vehicle

  RentalSystem holds:  list of Customers
                       list of Vehicles
                       list of Rentals
```

A key design choice is that the **menu functions are thin**. They only read input, call a method and print the result. The real rules live inside the classes.

---

## Class Guide

### `Vehicle` (abstract parent class)

The template for every vehicle. It cannot be created directly.

| Member | Type | Description |
|--------|------|-------------|
| `reg_no` | read-only property | Registration number. Stored in capitals. It is private and cannot be changed after creation |
| `make` | public attribute | Manufacturer, for example "Toyota" |
| `model` | public attribute | Model, for example "Corolla" |
| `is_available` | read-only property | `True` if the vehicle can be rented |
| `mark_rented()` | method | Sets the vehicle to rented. Fails if it is already rented |
| `mark_available()` | method | Sets the vehicle back to available. Fails if it was not rented |
| `type_name()` | method | Returns the real class name: "Car", "Motorcycle" or "Van" |
| `calculate_rental_cost(days)` | abstract method | Has no code here. Every child class must write its own |

### `Car`, `Motorcycle`, `Van` (child classes)

Each one inherits everything from `Vehicle` and only adds its own `calculate_rental_cost(days)`.

### `Customer`

| Member | Type | Description |
|--------|------|-------------|
| `customer_id` | read-only property | Unique ID, stored in capitals. Private, cannot be changed |
| `name` | property with setter | Must have at least 2 characters. Checked every time it is set |
| `phone` | public attribute | Phone number |
| `rentals` | public list | All rentals made by this customer |
| `total_spent()` | method | Adds up the cost of this customer's **completed** rentals |

### `Rental`

A record of one rental. It links a customer to a vehicle.

| Member | Description |
|--------|-------------|
| `rental_id` | Number of the rental (1, 2, 3, ...) |
| `customer` | The actual `Customer` object |
| `vehicle` | The actual `Vehicle` object |
| `rental_date` | The date the vehicle was taken |
| `days` | Number of days (estimated first, then the real number after return) |
| `return_date` | `None` until the vehicle is returned |
| `cost` | Estimated at first, then final after return |
| `finish(return_date)` | Closes the rental, checks the date, recalculates days and cost |
| `status()` | Returns "Active" or "Completed" |

### `RentalSystem` (the manager)

Holds the three main lists and coordinates the other classes.

| Method | Description |
|--------|-------------|
| `find_customer(customer_id)` | Returns the matching customer or raises "Customer not found." |
| `find_vehicle(reg_no)` | Returns the matching vehicle or raises "Vehicle not found." |
| `register_customer(customer)` | Adds a customer. Rejects duplicate IDs |
| `add_vehicle(vehicle)` | Adds a vehicle. Rejects duplicate registration numbers |
| `rent_vehicle(customer_id, reg_no, rental_date, days)` | Creates a rental and returns it |
| `return_vehicle(reg_no, return_date)` | Finishes the active rental and frees the vehicle |

---

## OOP Concepts Explained

The code contains comment blocks starting with `[CONCEPT: ...]` to point out each concept. Here is where each one is used.

### 1. Abstraction

`Vehicle` inherits from `ABC` and has an `@abstractmethod`. This means:

- You can **never** create a plain `Vehicle(...)`.
- It exists only as a template for `Car`, `Motorcycle` and `Van`.
- Every child class is **forced** to write its own `calculate_rental_cost()`.

This matches the real world: a rental company never rents a "generic vehicle". It rents a car, a motorcycle or a van.

### 2. Inheritance

`Car(Vehicle)`, `Motorcycle(Vehicle)` and `Van(Vehicle)` automatically receive everything `Vehicle` already has: the constructor, `reg_no`, `is_available`, `mark_rented()`, `mark_available()` and `type_name()`. They only add what makes them different, which is their price.

### 3. Polymorphism

All three vehicle classes have a method with the **same name**, `calculate_rental_cost(days)`, but each one gives a **different result**.

The clearest example is the **Compare Prices** option. It loops through every vehicle and calls the same method:

```python
for vehicle in system.vehicles:
    print(vehicle.calculate_rental_cost(days))
```

There is no `if vehicle is a Car ... elif vehicle is a Van ...`. Python automatically runs the correct version for each object. The `Rental` class uses the same idea: it never needs to know the vehicle type to work out the cost.

### 4. Encapsulation

Important data is hidden using a double underscore (`__`), which makes an attribute **private**:

| Private attribute | Why it is private |
|-------------------|-------------------|
| `Vehicle.__reg_no` | It identifies the vehicle. If changed, two vehicles could share one registration number and break every search |
| `Vehicle.__available` | It must only change through `mark_rented()` and `mark_available()`, which enforce the "no double renting" rule |
| `Customer.__customer_id` | The system finds customers by this ID, so changing it would break the lookup and the rental history |
| `Customer.__name` | It may change, but only through the `name` setter, which checks the length |

Access is given through:

- **Read-only properties** (`@property` with no setter): `reg_no`, `is_available`, `customer_id`
- **A property with a setter that validates**: `Customer.name`

Some attributes are **deliberately public** (`make`, `model`, `phone`, `rentals`, and the fields of `Rental`) because nothing breaks if they change. Hiding them would be encapsulation just for decoration.

### 5. Object Collaboration

Classes work together instead of one class doing everything.

- A `Rental` holds **references** to the real `Customer` and `Vehicle` objects. It does not copy their data.
- `Customer.total_spent()` asks each `Rental` for its cost.
- `RentalSystem.rent_vehicle()` brings several objects together: it finds the customer and vehicle, asks the vehicle to mark itself rented, creates a `Rental`, and tells the customer to remember it.
- Each class enforces its **own** rules. For example, `RentalSystem` does not check whether a vehicle is already rented. It simply asks the `Vehicle`, which knows its own state.

### 6. Validation and Error Handling

See the next section.

---

## Validation and Error Handling

The program checks input and breaks no rules. When something is wrong, the code raises a `ValueError` with a clear message. The `main()` loop catches it, prints it, and shows the menu again, so the program never crashes.

| Check | Where | Error message |
|-------|-------|---------------|
| Empty registration, make or model | `Vehicle.__init__` | Registration, make and model cannot be empty. |
| Empty customer ID | `Customer.__init__` | Customer ID cannot be empty. |
| Name shorter than 2 characters | `Customer.name` setter | Name must have at least 2 characters. |
| Duplicate customer ID | `RentalSystem.register_customer` | Customer ID already exists. |
| Duplicate registration number | `RentalSystem.add_vehicle` | Registration number already exists. |
| Customer not found | `RentalSystem.find_customer` | Customer not found. |
| Vehicle not found | `RentalSystem.find_vehicle` | Vehicle not found. |
| Days is zero or negative | `RentalSystem.rent_vehicle`, `compare_prices` | Rental days must be more than 0. |
| Renting an already rented vehicle | `Vehicle.mark_rented` | Vehicle is already rented. |
| Returning a vehicle that is not rented | `Vehicle.mark_available`, `RentalSystem.return_vehicle` | Vehicle is not rented, so it cannot be returned. |
| Return date before rental date | `Rental.finish` | Return date cannot be before the rental date. |
| Empty input | `read_text` | Input cannot be empty. |
| Not a whole number | `read_number` | Please enter a valid whole number. |
| Wrong date format | `read_date` | Invalid date. Use YYYY-MM-DD, e.g. 2026-09-28. |
| Invalid vehicle type choice | `add_vehicle` | Invalid vehicle type. |
| Invalid menu choice | `main` | Error: invalid choice, enter a number from 1 to 13. |

**Note:** IDs and registration numbers are not case sensitive. Spaces at the start and end are removed, and the value is converted to capital letters, so `c001` and `C001` are treated as the same ID.

---

## How a Rental Works (Step by Step)

### Renting a vehicle (menu option 5)

1. The user enters the customer ID, vehicle registration, rental date and number of days.
2. `RentalSystem` finds the `Customer` object.
3. `RentalSystem` finds the `Vehicle` object.
4. The number of days is checked (it must be more than 0).
5. The vehicle is asked to mark itself as rented. This fails if it is already rented.
6. A new `Rental` is created. It calls `calculate_rental_cost()` on the vehicle to get the **estimated cost**.
7. The rental is added to the customer's list and to the system's master list.
8. The rental ID and estimated cost are shown.

### Returning a vehicle (menu option 6)

1. The user enters the vehicle registration and the return date.
2. `RentalSystem` finds the vehicle and checks that it is currently rented.
3. It finds the **active** rental for that vehicle (the one with no return date).
4. The `Rental` finishes itself. It checks the return date, works out the real days (minimum 1) and recalculates the **final cost**.
5. The vehicle is marked as available again.
6. The days charged and the final cost are shown.

---

## Example Session

```
========================================
     VEHICLE RENTAL MANAGEMENT SYSTEM
========================================
1. Register Customer
2. Add Vehicle
...
13. Exit
Enter choice: 12
Sample data loaded.

Enter choice: 5
Customer ID: C001
Vehicle registration: UAB123C
Rental date (YYYY-MM-DD): 2026-09-28
Number of days: 3
Rental confirmed. ID: 1, estimated cost: 150

Enter choice: 6
Vehicle registration: UAB123C
Return date (YYYY-MM-DD): 2026-09-30
Vehicle returned. Days charged: 2, final cost: 100

Enter choice: 5
Customer ID: C001
Vehicle registration: UAB123C
Rental date (YYYY-MM-DD): 2026-10-01
Number of days: 0
Error: Rental days must be more than 0.
```

In this example the customer expected 3 days (estimate 150), but returned the car after 2 days, so the final cost is 100. The last step shows how an error is handled without crashing.

---

## Sample Data

Menu option 12 loads the following records so you can test quickly.

**Customers**

| ID | Name | Phone |
|----|------|-------|
| C001 | Alice Mukasa | 0700111222 |
| C002 | Brian Okello | 0755333444 |

**Vehicles**

| Registration | Type | Make | Model |
|--------------|------|------|-------|
| UAB123C | Car | Toyota | Corolla |
| UBB456M | Motorcycle | Honda | CB500 |
| UCC789V | Van | Toyota | HiAce |

If you select option 12 a second time, the program catches the duplicate error and shows "Sample data was already loaded." instead of crashing.

---

## Limitations

- **No permanent storage.** All data is kept in memory. When the program closes, everything is lost.
- **No editing or deleting.** Customers and vehicles can be added but not edited or removed from the menu.
- **Simple pricing.** Rates are fixed in the code and cannot be changed while the program runs.
- **No payment, deposit or late-fee handling.**
- **Text interface only.** There is no graphical interface.
- **Revenue only counts completed rentals.** Active rentals show an estimated cost but do not count toward total spent or total revenue.

---

## Possible Improvements

- Save and load data using a file (JSON or CSV) or a database such as SQLite
- Add options to edit and delete customers and vehicles
- Add more vehicle types (for example Truck or Bus) by creating one new child class with its own pricing. The rest of the program would not need to change
- Add late-return fees and discounts for long rentals
- Add a graphical or web interface
- Add automated tests for the classes
- Add user login for staff

---

## Team

**Group 3**

| Name | Role |
|------|------|
| _Add member name_ | _Add role_ |
| _Add member name_ | _Add role_ |
| _Add member name_ | _Add role_ |

**Course:** Object-Oriented Programming (Python)
**Institution:** Uganda Christian University (UCU)
