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


