import ephem
from datetime import datetime
import math

def calculate_prayer_times_hanafi(latitude, longitude, date_str):
    observer = ephem.Observer()
    observer.lat, observer.lon = str(latitude), str(longitude)
    observer.date = date_str  # Ensure date_str is "YYYY/MM/DD"
    original_date = observer.date

    sun = ephem.Sun()

    # Fajr: Sun 18° below horizon at dawn
    observer.horizon = '-18'
    observer.date = original_date
    fajr = observer.previous_rising(sun, use_center=True)

    # Dhuhr: Solar noon
    observer.date = original_date
    dhuhr = observer.next_transit(sun)

    # Maghrib: Sunset
    observer.horizon = '0'
    observer.date = original_date
    maghrib = observer.next_setting(sun)

    # Isha: Sun 18° below horizon after sunset
    observer.horizon = '-18'
    observer.date = original_date
    isha = observer.next_setting(sun, use_center=True)

    # Asr: Hanafi (shadow = 2x object)
    def compute_hanafi_asr(obs, sun_obj, dhuhr_time):
        obs.date = dhuhr_time
        sun.compute(obs)
        decl = sun.dec
        lat = obs.lat
        phi = ephem.degrees(lat)
        delta = decl
        angle = math.atan(1.0 / (2 + math.tan(abs(phi - delta))))
        asr_alt = ephem.degrees(angle)

        # Find when sun's altitude equals asr_alt after Dhuhr
        def find_asr_time(start, end):
            tolerance = ephem.second * 30
            while end - start > tolerance:
                mid = start + (end - start)/2
                obs.date = mid
                sun.compute(obs)
                if sun.alt > asr_alt:
                    start = mid
                else:
                    end = mid
            return start

        try:
            asr_start = dhuhr_time
            asr_end = maghrib
            asr_time = find_asr_time(asr_start, asr_end)
            return asr_time
        except:
            return dhuhr_time + (maghrib - dhuhr_time) * 0.5  # Fallback

    asr = compute_hanafi_asr(observer, sun, dhuhr)

    return {
        "Fajr": ephem.localtime(fajr).strftime("%H:%M"),
        "Dhuhr": ephem.localtime(dhuhr).strftime("%H:%M"),
        "Asr": ephem.localtime(asr).strftime("%H:%M"),
        "Maghrib": ephem.localtime(maghrib).strftime("%H:%M"),
        "Isha": ephem.localtime(isha).strftime("%H:%M"),
    }

if __name__ == "__main__":    
    import geocoder
    date = datetime.now().strftime("%Y/%m/%d")  # Corrected date format
    g = geocoder.ip('me')
    if g.latlng:
        latitude, longitude = g.latlng
        times = calculate_prayer_times_hanafi(latitude, longitude, date)
        print(times)
    else:
        print("Location not found. Using default coordinates.")
        # Example: Default to Mecca's coordinates
        times = calculate_prayer_times_hanafi(21.4225, 39.8262, date)
        print(times)