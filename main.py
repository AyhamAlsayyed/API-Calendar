from datetime import datetime, timedelta

from GoogleCalendar import GoogleCalendar

gc = GoogleCalendar()

# --- Add a new test event ---
start_time = datetime.utcnow() + timedelta(hours=0)
end_time = start_time + timedelta(hours=24)

new_event = gc.add_event(
    summary="Test",
    start_time=start_time,
    end_time=end_time,
)
print("\nNew Event Created:")
print(f"Event ID: {new_event['id']}")
print(f"Summary: {new_event['summary']}")
print(f"Start: {new_event['start']['dateTime']}")
print(f"End: {new_event['end']['dateTime']}")
