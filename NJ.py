
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

  