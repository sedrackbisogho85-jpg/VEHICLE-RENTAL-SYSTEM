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
