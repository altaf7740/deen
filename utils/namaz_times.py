import ephem # get the sun calculations
from datetime import datetime, timedelta

def calculate_prayer_times_hanafi(latitude, longitude, date):
    observer = ephem.Observer()
    observer.lat, observer.lon = str(latitude), str(longitude)
    observer.date = date

    # Sun calculations
    sun = ephem.Sun()

    # Calculate prayer times
    fajr = observer.previous_rising(sun, use_center=True) - (18.0 / 360.0)  # Fajr (Sun 18° below)
    dhuhr = observer.next_transit(sun)  # Dhuhr (Solar Noon)
    asr = observer.next_setting(sun, use_center=True) - (120.0 / 360.0)  # Hanafi Asr (Shadow = 2x Object)
    maghrib = observer.next_setting(sun)  # Maghrib (Sunset)
    isha = observer.next_setting(sun, use_center=True) + (18.0 / 360.0)  # Isha (Sun 18° below)

    # Convert to readable format
    return {
        "Fajr": ephem.localtime(fajr).strftime("%H:%M"),
        "Dhuhr": ephem.localtime(dhuhr).strftime("%H:%M"),
        "Asr": ephem.localtime(asr).strftime("%H:%M"),
        "Maghrib": ephem.localtime(maghrib).strftime("%H:%M"),
        "Isha": ephem.localtime(isha).strftime("%H:%M"),
    }

if __name__ == "__main__":    
    import geocoder # get the latitude and longitude, but require internet
    date = datetime.now().strftime("%Y-%d-%m")
    latitude, longitude = geocoder.ip('me').latlng    # this does not work in offline mode. if required pass latitude and longitude manually
    azan_timing = calculate_prayer_times_hanafi(latitude, longitude, date)

    print(azan_timing)
