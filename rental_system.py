"""
Vehicle Rental Management System - Group 3 (single file version)

This file is heavily commented to point out exactly WHERE and HOW each
Object-Oriented Programming (OOP) concept required by the assignment has
been used:
    - Abstraction
    - Inheritance
    - Polymorphism
    - Encapsulation
    - Object collaboration (classes working together)
    - Validation / error handling

Look for comment blocks starting with [CONCEPT] throughout the file.
"""
from abc import ABC, abstractmethod
from datetime import datetime


# =============================================================================
# VEHICLE CLASSES
# =============================================================================
# [CONCEPT: ABSTRACTION]
# Vehicle inherits from ABC (Abstract Base Class). This means:
#   1. Vehicle itself can NEVER be created directly (Vehicle(...) would fail).
#   2. Vehicle exists only to be a common "template" that Car, Motorcycle and
#      Van are built from.
# This models the real world correctly: a rental company never rents out a
# generic, unspecified "vehicle" - every real vehicle is a specific type
# (a car, a motorcycle, or a van).
class Vehicle(ABC):
    """Abstract parent class. It cannot be created directly."""

    def __init__(self, reg_no, make, model):
        # [CONCEPT: VALIDATION]
        # Reject empty text BEFORE any attribute is stored, so the object is
        # never left in a half-valid state.
        if reg_no.strip() == "" or make.strip() == "" or model.strip() == "":
            raise ValueError("Registration, make and model cannot be empty.")

        # [CONCEPT: ENCAPSULATION - private attribute]
        # The double-underscore prefix (__reg_no) makes this attribute
        # "private" through Python's name mangling. It is private because
        # the registration number is the vehicle's identity - if outside
        # code could reassign it after creation, two vehicles could end up
        # sharing the same registration number and break every lookup in
        # RentalSystem. There is deliberately NO setter for it: once set in
        # the constructor, it can only be read (see the reg_no property
        # below), never changed.
        self.__reg_no = reg_no.strip().upper()

        # These two are left as ordinary PUBLIC attributes on purpose.
        # Nothing bad happens if someone changes a vehicle's make or model
        # after creation (it doesn't break any rule elsewhere in the
        # system), so adding private variables + getters/setters here would
        # be encapsulation "for decoration" only, which the assignment
        # explicitly warns against.
        self.make = make.strip()
        self.model = model.strip()

        # [CONCEPT: ENCAPSULATION - private attribute]
        # __available is private for the same reason as __reg_no: it must
        # only ever change through the controlled methods mark_rented() and
        # mark_available() below, because those methods contain the
        # business rule ("you cannot rent an already-rented vehicle").
        # If this were a public attribute, any code could set
        # vehicle.available = True/False directly and silently break that
        # rule.
        self.__available = True

    # [CONCEPT: ENCAPSULATION - read-only property]
    # @property turns reg_no() into something that can be READ like a plain
    # attribute (vehicle.reg_no) but cannot be WRITTEN to from outside the
    # class, because no matching @reg_no.setter is defined. This gives
    # controlled, read-only access to the private __reg_no attribute.
    @property
    def reg_no(self):
        return self.__reg_no

    # Same idea: is_available is a read-only "window" onto the private
    # __available flag. Outside code can check it, but can only change it by
    # calling mark_rented()/mark_available(), never directly.
    @property
    def is_available(self):
        return self.__available

    def mark_rented(self):
        # [CONCEPT: VALIDATION]
        # This is the single rule that prevents the same vehicle from being
        # rented to two customers at once. Because __available is private,
        # this method is the ONLY legal way to flip it to False.
        if not self.__available:
            raise ValueError("Vehicle is already rented.")
        self.__available = False

    def mark_available(self):
        # [CONCEPT: VALIDATION]
        # Mirror rule: you cannot "return" a vehicle that was never rented.
        if self.__available:
            raise ValueError("Vehicle is not rented, so it cannot be returned.")
        self.__available = True

    def type_name(self):
        # Returns the actual subclass name ("Car", "Motorcycle" or "Van") of
        # whatever object this method is called on. Used by the menu to
        # display what kind of vehicle each row is, without the Vehicle
        # class needing to know its own subclasses.
        return self.__class__.__name__

    # [CONCEPT: ABSTRACTION + the contract for POLYMORPHISM]
    # @abstractmethod means:
    #   - Vehicle does NOT provide an implementation of this method.
    #   - Every subclass of Vehicle (Car, Motorcycle, Van) is FORCED by
    #     Python to provide its own calculate_rental_cost(). If a subclass
    #     forgot to, Python would refuse to let you create an object of
    #     that subclass at all.
    # This single method name is what makes polymorphism possible later:
    # every vehicle type answers to the same method call, but each
    # implementation is different (see the three classes below).
    @abstractmethod
    def calculate_rental_cost(self, days):
        """Every subclass must calculate its own cost."""


# [CONCEPT: INHERITANCE]
# Car(Vehicle) means Car automatically gets everything Vehicle already
# built: __init__, reg_no, is_available, mark_rented(), mark_available(),
# type_name(). Car does not need to rewrite any of that code - it only adds
# what makes a Car different from any other vehicle: its own pricing rule.
class Car(Vehicle):
    # [CONCEPT: POLYMORPHISM / METHOD OVERRIDING]
    # This method has the EXACT same name and signature as the abstract
    # method in Vehicle, but a completely different implementation. This is
    # "overriding": Car is replacing Vehicle's placeholder with real
    # behaviour specific to cars.
    def calculate_rental_cost(self, days):
        return 50 * days                 # 50 per day


class Motorcycle(Vehicle):
    # [CONCEPT: POLYMORPHISM / METHOD OVERRIDING]
    # Same method name as Car's version above, but a different rate. When
    # code elsewhere calls vehicle.calculate_rental_cost(days), Python
    # automatically picks THIS version if `vehicle` happens to be a
    # Motorcycle object - no if/elif type-checking needed anywhere.
    def calculate_rental_cost(self, days):
        return 25 * days                 # 25 per day


class Van(Vehicle):
    # [CONCEPT: POLYMORPHISM / METHOD OVERRIDING]
    # A third, again different, implementation of the same method name.
    # Car, Motorcycle and Van now form one inheritance family that all
    # "speak the same language" (calculate_rental_cost) but each answers
    # in its own way - this is polymorphism ("many forms").
    def calculate_rental_cost(self, days):
        return 80 * days + 30            # 80 per day + 30 fixed insurance fee


# =============================================================================
# CUSTOMER CLASS
# =============================================================================
class Customer:
    def __init__(self, customer_id, name, phone):
        # [CONCEPT: ENCAPSULATION - private attribute]
        # __customer_id is private because RentalSystem looks customers up
        # by this value (see RentalSystem.find_customer below). If it could
        # be changed after registration, existing rentals would point to a
        # customer ID that no longer matches anything, silently breaking
        # lookups and rental history.
        self.__customer_id = customer_id.strip().upper()

        # [CONCEPT: ENCAPSULATION - private attribute + property/setter]
        # __name is private and is only ever changed through the name
        # property's setter below, which enforces a validation rule (must
        # be at least 2 characters). Setting self.name = name here calls
        # that setter immediately, so the rule applies even in the
        # constructor, not just on later changes.
        self.__name = ""
        self.name = name                                   # uses the setter

        # phone and rentals are left as ordinary PUBLIC attributes. There is
        # no rule elsewhere in the system that depends on phone being
        # unchangeable, and rentals is a plain list that Rental objects are
        # appended to - making it private would add complexity without
        # protecting anything meaningful for a project this size.
        self.phone = phone
        self.rentals = []

        if self.__customer_id == "":
            raise ValueError("Customer ID cannot be empty.")

    # [CONCEPT: ENCAPSULATION - read-only property]
    # Like Vehicle.reg_no, this exposes __customer_id for reading only.
    @property
    def customer_id(self):
        return self.__customer_id

    # [CONCEPT: ENCAPSULATION - property with validation in the setter]
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        # [CONCEPT: VALIDATION]
        # Runs automatically every time someone does customer.name = "...",
        # including inside __init__. Rejects anything under 2 characters.
        if len(value.strip()) < 2:
            raise ValueError("Name must have at least 2 characters.")
        self.__name = value.strip()

    def total_spent(self):
        # [CONCEPT: OBJECT COLLABORATION]
        # Customer does not store a running total itself - it asks each of
        # its own Rental objects for their .cost, and only counts rentals
        # that have actually been completed (return_date is not None).
        # This keeps the "how much has this customer paid" logic in one
        # place instead of duplicating it around the program.
        return sum(r.cost for r in self.rentals if r.return_date is not None)


# =============================================================================
# RENTAL CLASS
# =============================================================================
class Rental:
    """One rental. It links a Customer to a Vehicle."""

    def __init__(self, rental_id, customer, vehicle, rental_date, days):
        # rental_id, customer, vehicle, rental_date and days are public here.
        # A Rental is a simple record of a transaction; nothing in the
        # system relies on these being unchangeable, so plain attributes
        # keep the class easy to read.
        self.rental_id = rental_id

        # [CONCEPT: OBJECT COLLABORATION / ASSOCIATION]
        # A Rental object does not copy the customer's or vehicle's data -
        # it holds a direct reference to the actual Customer object and the
        # actual Vehicle object. This means if that customer's name were
        # updated, every Rental referencing them would automatically see
        # the new name, because they all point to the SAME object in
        # memory.
        self.customer = customer
        self.vehicle = vehicle

        self.rental_date = rental_date
        self.days = days
        self.return_date = None

        # [CONCEPT: POLYMORPHISM IN ACTION]
        # Rental does NOT know or care whether `vehicle` is a Car,
        # Motorcycle or Van. It just calls calculate_rental_cost(days) on
        # whatever object was passed in, and Python automatically runs the
        # correct subclass's version. This is exactly why the abstract
        # method was declared on Vehicle: Rental can treat every vehicle
        # type identically through that one shared method name.
        self.cost = vehicle.calculate_rental_cost(days)    # estimate (polymorphism)

    def finish(self, return_date):
        # [CONCEPT: VALIDATION]
        # A return date earlier than the rental date makes no logical
        # sense (you cannot return a car before you rented it), so it is
        # rejected here before anything else changes.
        if return_date < self.rental_date:
            raise ValueError("Return date cannot be before the rental date.")

        # Bill for at least 1 day even if rented and returned on the same
        # date (a same-day rental still counts as a full day's use).
        self.days = max(1, (return_date - self.rental_date).days)
        self.return_date = return_date

        # [CONCEPT: POLYMORPHISM IN ACTION - again]
        # The final cost is recalculated the same polymorphic way as the
        # estimate was: by calling calculate_rental_cost() on whichever
        # vehicle subclass this rental happens to hold.
        self.cost = self.vehicle.calculate_rental_cost(self.days)  # final cost

    def status(self):
        return "Completed" if self.return_date else "Active"


# =============================================================================
# RENTAL SYSTEM (the "manager" class)
# =============================================================================
# [CONCEPT: OBJECT COLLABORATION]
# RentalSystem does not do the actual rental-cost math, customer-name
# validation, or availability checking itself - it collaborates with
# Customer, Vehicle and Rental objects and lets each of them enforce their
# own rules. RentalSystem's job is only to hold the three collections
# (customers, vehicles, rentals) and coordinate the lookups between them.
# This keeps business logic spread across the classes that own it, instead
# of piling everything into one giant class.
class RentalSystem:
    def __init__(self):
        # Public lists: RentalSystem's whole purpose is to hold and expose
        # these collections, so there is no need to hide them behind
        # getters - the menu functions below read them directly (e.g. to
        # loop over system.vehicles).
        self.customers = []
        self.vehicles = []
        self.rentals = []

    def find_customer(self, customer_id):
        # [CONCEPT: VALIDATION]
        # A plain linear search. If nothing matches, a clear ValueError is
        # raised instead of returning None and letting the program crash
        # later with a confusing AttributeError.
        for c in self.customers:
            if c.customer_id == customer_id.strip().upper():
                return c
        raise ValueError("Customer not found.")

    def find_vehicle(self, reg_no):
        for v in self.vehicles:
            if v.reg_no == reg_no.strip().upper():
                return v
        raise ValueError("Vehicle not found.")

    def register_customer(self, customer):
        # [CONCEPT: VALIDATION]
        # Enforces uniqueness of customer_id, which Customer itself cannot
        # enforce alone (a single Customer object cannot know about every
        # other Customer object - only the collection they all live in can
        # check that).
        for c in self.customers:
            if c.customer_id == customer.customer_id:
                raise ValueError("Customer ID already exists.")
        self.customers.append(customer)

    def add_vehicle(self, vehicle):
        # [CONCEPT: VALIDATION]
        # Same idea as above, but for vehicle registration numbers.
        for v in self.vehicles:
            if v.reg_no == vehicle.reg_no:
                raise ValueError("Registration number already exists.")
        self.vehicles.append(vehicle)

    def rent_vehicle(self, customer_id, reg_no, rental_date, days):
        # [CONCEPT: OBJECT COLLABORATION]
        # This one method shows several objects working together to
        # complete a single transaction:
        #   1. Ask itself to find the Customer object.
        #   2. Ask itself to find the Vehicle object.
        #   3. Validate the number of days.
        #   4. Ask the Vehicle to mark itself as rented (Vehicle enforces
        #      its own "already rented" rule - RentalSystem does not
        #      duplicate that check).
        #   5. Create a Rental object, which itself calls the vehicle's
        #      polymorphic calculate_rental_cost() to work out the price.
        #   6. Tell the Customer object to remember this rental.
        #   7. Keep the Rental in the system's own master list too.
        customer = self.find_customer(customer_id)
        vehicle = self.find_vehicle(reg_no)

        # [CONCEPT: VALIDATION]
        if days <= 0:
            raise ValueError("Rental days must be more than 0.")

        vehicle.mark_rented()             # raises an error if already rented
        rental = Rental(len(self.rentals) + 1, customer, vehicle, rental_date, days)
        customer.rentals.append(rental)
        self.rentals.append(rental)
        return rental

    def return_vehicle(self, reg_no, return_date):
        # [CONCEPT: VALIDATION]
        # Reject the return immediately if the vehicle was never marked as
        # rented in the first place.
        vehicle = self.find_vehicle(reg_no)
        if vehicle.is_available:
            raise ValueError("Vehicle is not rented, so it cannot be returned.")

        # [CONCEPT: OBJECT COLLABORATION]
        # Find the matching ACTIVE rental for this vehicle, let the Rental
        # object finish itself (it validates the return date and
        # recalculates its own cost polymorphically), then tell the
        # Vehicle it is available again.
        for r in self.rentals:
            if r.vehicle is vehicle and r.return_date is None:
                r.finish(return_date)
                vehicle.mark_available()
                return r


# =============================================================================
# MENU / USER INTERFACE FUNCTIONS
# =============================================================================
# Everything below this line is deliberately "thin": it only reads input,
# calls a RentalSystem method, and prints a result. None of the business
# rules (uniqueness checks, availability checks, date validation beyond
# basic format) live here - they live inside the classes above. This is
# what the assignment calls avoiding "putting all logic inside the menu".

def read_text(prompt):
    value = input(prompt).strip()
    # [CONCEPT: VALIDATION]
    if value == "":
        raise ValueError("Input cannot be empty.")
    return value


def read_number(prompt):
    try:
        return int(read_text(prompt))
    except ValueError:
        # [CONCEPT: VALIDATION]
        # Catches Python's own ValueError from int("abc") and turns it into
        # a message a non-programmer user can understand.
        raise ValueError("Please enter a valid whole number.")


def read_date(prompt):
    text = read_text(prompt)
    try:
        return datetime.strptime(text, "%Y-%m-%d").date()
    except ValueError:
        # [CONCEPT: VALIDATION]
        raise ValueError("Invalid date. Use YYYY-MM-DD, e.g. 2026-09-28.")


def show_menu():
    print("\n========================================")
    print("     VEHICLE RENTAL MANAGEMENT SYSTEM")
    print("========================================")
    print("1. Register Customer")
    print("2. Add Vehicle")
    print("3. Display Available Vehicles")
    print("4. Display Rented Vehicles")
    print("5. Rent Vehicle")
    print("6. Return Vehicle")
    print("7. Search Customer")
    print("8. Search Vehicle")
    print("9. View Customer Rental History")
    print("10. View Rental Summary")
    print("11. Compare Prices (Polymorphism)")
    print("12. Load Sample Data")
    print("13. Exit")



