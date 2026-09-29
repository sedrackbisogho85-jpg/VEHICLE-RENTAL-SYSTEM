

def register_customer(system):
    # This constructor call can itself raise a ValueError (empty ID, or a
    # name under 2 characters via the name setter) - main() catches it.
    customer = Customer(read_text("Customer ID: "), read_text("Name: "),
                        read_text("Phone: "))
    system.register_customer(customer)
    print("Customer registered. - vehicle.py:9")


def add_vehicle(system):
    # [CONCEPT: OBJECT COLLABORATION]
    # This dictionary maps a menu digit straight to the matching CLASS
    # (not an instance). Car, Motorcycle and Van are all interchangeable
    # here because they all take the same constructor arguments - a small,
    # practical demonstration of how the inheritance family makes this
    # kind of generic code possible.
    kinds = {"1": Car, "2": Motorcycle, "3": Van}
    choice = input("Type (1=Car, 2=Motorcycle, 3=Van): ").strip()
    if choice not in kinds:
        raise ValueError("Invalid vehicle type.")
    vehicle = kinds[choice](read_text("Registration number: "),
                            read_text("Make: "), read_text("Model: "))
    system.add_vehicle(vehicle)
    print("Vehicle added. - vehicle.py:26")


def show_available(system):
    print(f"{'Registration':<14}{'Type':<12}{'Model':<20}Status - vehicle.py:30")
    found = False
    for v in system.vehicles:
        # v.is_available reads the PRIVATE __available flag through its
        # read-only property - the menu can check it but never set it.
        if v.is_available:
            # v.type_name() works the same for every vehicle type without
            # the menu needing to know if v is a Car, Motorcycle or Van.
            print(f"{v.reg_no:<14}{v.type_name():<12} - vehicle.py:38"
                  f"{v.make + ' ' + v.model:<20}Available")
            found = True
    if not found:
        print("No available vehicles. - vehicle.py:42")


def show_rented(system):
    print(f"{'Registration':<14}{'Type':<12}{'Customer':<18}{'Rental Date':<13}Status - vehicle.py:46")
    found = False
    for r in system.rentals:
        if r.return_date is None:
            print(f"{r.vehicle.reg_no:<14}{r.vehicle.type_name():<12} - vehicle.py:50"
                  f"{r.customer.name:<18}{str(r.rental_date):<13}Rented")
            found = True
    if not found:
        print("No rented vehicles. - vehicle.py:54")


def rent_vehicle(system):
    customer_id = read_text("Customer ID: ")
    reg_no = read_text("Vehicle registration: ")
    rental_date = read_date("Rental date (YYYY-MM-DD): ")
    days = read_number("Number of days: ")
    # All the real work (and all the validation) happens inside
    # system.rent_vehicle(); this function just displays the result.
    rental = system.rent_vehicle(customer_id, reg_no, rental_date, days)
    print(f"Rental confirmed. ID: {rental.rental_id}, - vehicle.py:65"
          f"estimated cost: {rental.cost}")


def return_vehicle(system):
    reg_no = read_text("Vehicle registration: ")
    return_date = read_date("Return date (YYYY-MM-DD): ")
    r = system.return_vehicle(reg_no, return_date)
    print(f"Vehicle returned. Days charged: {r.days}, final cost: {r.cost} - vehicle.py:73")


def search_customer(system):
    customer = system.find_customer(read_text("Customer ID: "))
    print(f"{customer.customer_id} | {customer.name} | {customer.phone} - vehicle.py:78")


def search_vehicle(system):
    vehicle = system.find_vehicle(read_text("Registration number: "))
    state = "Available" if vehicle.is_available else "Rented"
    print(f"{vehicle.reg_no} | {vehicle.type_name()} | - vehicle.py:84"
          f"{vehicle.make} {vehicle.model} | {state}")


def customer_history(system):
    customer = system.find_customer(read_text("Customer ID: "))
    print(f"Customer: {customer.name} | Rentals: {len(customer.rentals)} - vehicle.py:90")
    for r in customer.rentals:
        print(f"{r.rental_id} | {r.vehicle.reg_no} | {r.rental_date} | - vehicle.py:92"
              f"{r.return_date or '-'} | {r.cost} | {r.status()}")
    # [CONCEPT: OBJECT COLLABORATION]
    # customer.total_spent() itself collaborates with each Rental in
    # customer.rentals to work out the figure - the menu just prints it.
    print(f"Total spent: {customer.total_spent()} - vehicle.py:97")


def show_summary(system):
    completed = [r for r in system.rentals if r.return_date is not None]
    available = len([v for v in system.vehicles if v.is_available])
    print("RENTAL SUMMARY - vehicle.py:103")
    print("Total customers  : - vehicle.py:104", len(system.customers))
    print("Total vehicles   : - vehicle.py:105", len(system.vehicles))
    print("Available        : - vehicle.py:106", available)
    print("Rented           : - vehicle.py:107", len(system.vehicles) - available)
    print("Total rentals    : - vehicle.py:108", len(system.rentals))
    print("Completed rentals: - vehicle.py:109", len(completed))
    print("Total revenue    : - vehicle.py:110", sum(r.cost for r in completed))


def compare_prices(system):
    days = read_number("Number of days: ")
    if days <= 0:
        raise ValueError("Rental days must be more than 0.")

    # [CONCEPT: POLYMORPHISM - the clearest demonstration in the program]
    # This loop treats every object in system.vehicles identically: it
    # just calls vehicle.calculate_rental_cost(days) on each one. There is
    # NO "if vehicle is a Car... elif vehicle is a Motorcycle..." anywhere.
    # Yet the printed results differ per vehicle, because Python looks up
    # calculate_rental_cost on each object's ACTUAL class (Car, Motorcycle
    # or Van) at the moment the loop runs. This is runtime polymorphism.
    for vehicle in system.vehicles:      # same call, different result per class
        print(f"{vehicle.reg_no} ({vehicle.type_name()}): - vehicle.py:126"
              f"{vehicle.calculate_rental_cost(days)}")


def load_sample_data(system):
    try:
        system.register_customer(Customer("C001", "Alice Mukasa", "0700111222"))
        system.register_customer(Customer("C002", "Brian Okello", "0755333444"))
        # [CONCEPT: INHERITANCE + POLYMORPHISM at object-creation time]
        # Car, Motorcycle and Van objects are created here and immediately
        # afterwards stored in the SAME list (system.vehicles) alongside
        # each other, even though they are different classes. This only
        # works because they all inherit from Vehicle and share its
        # interface - the rest of the program can treat them uniformly.
        system.add_vehicle(Car("UAB123C", "Toyota", "Corolla"))
        system.add_vehicle(Motorcycle("UBB456M", "Honda", "CB500"))
        system.add_vehicle(Van("UCC789V", "Toyota", "HiAce"))
        print("Sample data loaded. - vehicle.py:143")
    except ValueError:
        # [CONCEPT: VALIDATION]
        # If sample data was already loaded in this run, register_customer/
        # add_vehicle would raise a duplicate error - caught here so
        # re-selecting this option does not crash the program.
        print("Sample data was already loaded. - vehicle.py:149")


