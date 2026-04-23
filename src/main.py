import json
from datetime import datetime
from pathlib import Path

# Build file path to /data/salon_schedule.json
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "salon_schedule.json"


def load_schedule():
    """Load existing appointments from the JSON file."""
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


def save_schedule(schedule):
    """Save appointments to the JSON file."""
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(schedule, file, indent=4)


def is_available(schedule, date, time, exclude_index=None):
    """
    Check whether a date/time slot is available.
    exclude_index is used when updating an appointment so the current
    appointment does not conflict with itself.
    """
    for index, appt in enumerate(schedule):
        if index == exclude_index:
            continue
        if appt["date"] == date and appt["time"] == time:
            return False
    return True


def view_schedule(show_numbers=False):
    """Display the schedule in sorted order."""
    schedule = load_schedule()

    if not schedule:
        print("No appointments yet.")
        return []

    schedule_sorted = sorted(
        enumerate(schedule),
        key=lambda item: (item[1]["date"], item[1]["time"])
    )

    print("\nSalon Schedule:")
    for display_num, (original_index, appt) in enumerate(schedule_sorted, start=1):
        if show_numbers:
            print(
                f"{display_num}. {appt['date']} {appt['time']} - "
                f"{appt['client']} ({appt['service']})"
            )
        else:
            print(
                f"{appt['date']} {appt['time']} - "
                f"{appt['client']} ({appt['service']})"
            )

    return schedule_sorted


def book_appointment():
    """Book a new appointment if the time slot is available."""
    schedule = load_schedule()

    name = input("Client Name: ").strip()
    service = input("Service (Blowout, Color, Silk Press): ").strip()
    date = input("Date (YYYY-MM-DD): ").strip()
    time = input("Time (HH:MM): ").strip()

    if is_available(schedule, date, time):
        appointment = {
            "client": name,
            "service": service,
            "date": date,
            "time": time,
            "created": datetime.now().isoformat(timespec="seconds")
        }
        schedule.append(appointment)
        save_schedule(schedule)
        print("Appointment booked successfully!")
    else:
        print("Time slot already taken.")


def update_appointment():
    """Update an existing appointment."""
    schedule = load_schedule()

    if not schedule:
        print("No appointments available to update.")
        return

    schedule_sorted = view_schedule(show_numbers=True)

    try:
        choice = int(input("\nEnter the appointment number to update: ").strip())
        if choice < 1 or choice > len(schedule_sorted):
            print("Invalid appointment number.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return

    original_index, current_appt = schedule_sorted[choice - 1]

    print("\nPress Enter to keep the current value.")

    new_name = input(f"Client Name [{current_appt['client']}]: ").strip()
    new_service = input(f"Service [{current_appt['service']}]: ").strip()
    new_date = input(f"Date [{current_appt['date']}]: ").strip()
    new_time = input(f"Time [{current_appt['time']}]: ").strip()

    updated_name = new_name if new_name else current_appt["client"]
    updated_service = new_service if new_service else current_appt["service"]
    updated_date = new_date if new_date else current_appt["date"]
    updated_time = new_time if new_time else current_appt["time"]

    if not is_available(schedule, updated_date, updated_time, exclude_index=original_index):
        print("Time slot already taken. Update canceled.")
        return

    schedule[original_index]["client"] = updated_name
    schedule[original_index]["service"] = updated_service
    schedule[original_index]["date"] = updated_date
    schedule[original_index]["time"] = updated_time
    schedule[original_index]["updated"] = datetime.now().isoformat(timespec="seconds")

    save_schedule(schedule)
    print("Appointment updated successfully!")


def cancel_appointment():
    """Cancel an existing appointment."""
    schedule = load_schedule()

    if not schedule:
        print("No appointments available to cancel.")
        return

    schedule_sorted = view_schedule(show_numbers=True)

    try:
        choice = int(input("\nEnter the appointment number to cancel: ").strip())
        if choice < 1 or choice > len(schedule_sorted):
            print("Invalid appointment number.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return

    original_index, selected_appt = schedule_sorted[choice - 1]

    confirm = input(
        f"Are you sure you want to cancel the appointment for "
        f"{selected_appt['client']} on {selected_appt['date']} at {selected_appt['time']}? (y/n): "
    ).strip().lower()

    if confirm == "y":
        removed = schedule.pop(original_index)
        save_schedule(schedule)
        print(
            f"Appointment for {removed['client']} on "
            f"{removed['date']} at {removed['time']} canceled successfully!"
        )
    else:
        print("Cancellation aborted.")


def main():
    """Main menu system."""
    while True:
        print("\nThe EGO Lounge Scheduling System")
        print("1. Book Appointment")
        print("2. View Schedule")
        print("3. Update Appointment")
        print("4. Cancel Appointment")
        print("5. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            book_appointment()
        elif choice == "2":
            view_schedule()
        elif choice == "3":
            update_appointment()
        elif choice == "4":
            cancel_appointment()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1, 2, 3, 4, or 5.")


if __name__ == "__main__":
    main()