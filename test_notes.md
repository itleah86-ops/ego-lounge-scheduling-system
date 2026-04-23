# Test Notes for The EGO Lounge Scheduling System

## Test 1: Book a valid appointment
- Input client name, service, date, and time
- Expected result: appointment is saved in salon_schedule.json
- Actual result: Passed

## Test 2: Prevent double booking
- Attempt to book the same date and time as an existing appointment
- Expected result: system displays "Time slot already taken."
- Actual result: Passed

## Test 3: View schedule
- Choose the view schedule option
- Expected result: all appointments display in date/time order
- Actual result: Passed

## Test 4: Update appointment
- Select an existing appointment and change the client name, service, date, or time
- Expected result: the appointment is updated and saved in salon_schedule.json
- Actual result: Passed

## Test 5: Prevent update to a taken time slot
- Attempt to update an appointment to the same date and time as another existing appointment
- Expected result: system displays "Time slot already taken. Update canceled."
- Actual result: Passed

## Test 6: Cancel appointment
- Select an existing appointment and confirm cancellation
- Expected result: the appointment is removed from salon_schedule.json
- Actual result: Passed

## Test 7: Abort cancellation
- Select an existing appointment and enter anything other than "y" when asked to confirm
- Expected result: system displays "Cancellation aborted." and keeps the appointment
- Actual result: Passed

## Test 8: Invalid menu option
- Enter an invalid menu choice such as 6
- Expected result: system displays invalid choice message
- Actual result: Passed

## Test 9: Empty schedule file
- Use an empty JSON list []
- Expected result: system displays "No appointments yet." or indicates there are no appointments available
- Actual result: Passed

## Known limitations
- The program does not yet validate date and time format beyond user input text.
- The program uses a command-line interface instead of a graphical interface.
- The program does not include authentication or multi-user support.
- Appointment data is stored locally in a JSON file rather than a database.
