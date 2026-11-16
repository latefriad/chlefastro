#!/usr/bin/env python3
"""
AstroDistances - Calculate exact distances between Earth, the Moon, and all Planets
+ Lunar Month Calculator (Calcul du mois de la Lune : 29 ou 30 jours, phases, âge, illumination)
Supports:
  - Exact calculations for any date/time (second-level precision) from 2000 to now and beyond.
  - Live real-time dashboard updating every second.
  - Lunar month calculation (durée de 29 ou 30 jours, âge de la lune, calendrier des phases).
  - Daily or second-by-second batch generation between 2000 and now with CSV export.
  - Built-in web dashboard launcher.
"""

import sys
import os
import time
import argparse
import csv
from datetime import datetime, timezone, timedelta

try:
    import astronomy
except ImportError:
    print("Error: 'astronomy-engine' library is required.")
    print("Install it with: pip install astronomy-engine")
    sys.exit(1)

SPEED_OF_LIGHT_KM_S = 299792.458
KM_PER_MILE = 1.609344

BODIES = [
    {"id": "Moon", "name_en": "Moon", "name_fr": "Lune", "body": astronomy.Body.Moon, "symbol": "🌕"},
    {"id": "Sun", "name_en": "Sun", "name_fr": "Soleil", "body": astronomy.Body.Sun, "symbol": "☀️"},
    {"id": "Mercury", "name_en": "Mercury", "name_fr": "Mercure", "body": astronomy.Body.Mercury, "symbol": "☿"},
    {"id": "Venus", "name_en": "Venus", "name_fr": "Vénus", "body": astronomy.Body.Venus, "symbol": "♀"},
    {"id": "Mars", "name_en": "Mars", "name_fr": "Mars", "body": astronomy.Body.Mars, "symbol": "♂"},
    {"id": "Jupiter", "name_en": "Jupiter", "name_fr": "Jupiter", "body": astronomy.Body.Jupiter, "symbol": "♃"},
    {"id": "Saturn", "name_en": "Saturn", "name_fr": "Saturne", "body": astronomy.Body.Saturn, "symbol": "♄"},
    {"id": "Uranus", "name_en": "Uranus", "name_fr": "Uranus", "body": astronomy.Body.Uranus, "symbol": "♅"},
    {"id": "Neptune", "name_en": "Neptune", "name_fr": "Neptune", "body": astronomy.Body.Neptune, "symbol": "♆"},
    {"id": "Pluto", "name_en": "Pluto", "name_fr": "Pluton", "body": astronomy.Body.Pluto, "symbol": "♇"},
]

def format_light_time(seconds: float) -> str:
    if seconds < 60:
        return f"{seconds:.2f} s"
    elif seconds < 3600:
        mins = int(seconds // 60)
        secs = seconds % 60
        return f"{mins}m {secs:.1f}s"
    else:
        hours = int(seconds // 3600)
        rem = seconds % 3600
        mins = int(rem // 60)
        secs = rem % 60
        return f"{hours}h {mins}m {secs:.0f}s"

def calculate_distance(body: astronomy.Body, astro_time: astronomy.Time):
    """Calculate distance in AU, km, miles, light time, and radial velocity."""
    vec = astronomy.GeoVector(body, astro_time, True)
    dist_au = vec.Length()
    dist_km = dist_au * astronomy.KM_PER_AU
    dist_miles = dist_km / KM_PER_MILE
    light_time_s = dist_km / SPEED_OF_LIGHT_KM_S

    # Compute radial velocity using a 1-second forward finite difference
    astro_time_next = astro_time.AddDays(1.0 / 86400.0)
    vec_next = astronomy.GeoVector(body, astro_time_next, True)
    dist_km_next = vec_next.Length() * astronomy.KM_PER_AU
    velocity_km_s = dist_km_next - dist_km  # > 0 means moving away, < 0 means moving closer

    return {
        "au": dist_au,
        "km": dist_km,
        "miles": dist_miles,
        "light_seconds": light_time_s,
        "light_time_str": format_light_time(light_time_s),
        "velocity_km_s": velocity_km_s,
        "status": "Approaching (se rapproche)" if velocity_km_s < 0 else "Receding (s'éloigne)"
    }

def get_moon_phase_name(phase_deg: float, lang: str = "fr") -> str:
    """Return lunar phase name based on ecliptic longitude difference (0 to 360 deg)."""
    deg = phase_deg % 360.0
    if deg < 15.0 or deg >= 345.0:
        return "Nouvelle Lune (New Moon) 🌑" if lang == "fr" else "New Moon 🌑"
    elif deg < 75.0:
        return "Premier Croissant / Hilal (Waxing Crescent) 🌒" if lang == "fr" else "Waxing Crescent 🌒"
    elif deg < 105.0:
        return "Premier Quartier (First Quarter) 🌓" if lang == "fr" else "First Quarter 🌓"
    elif deg < 165.0:
        return "Gibbeuse Croissante (Waxing Gibbous) 🌔" if lang == "fr" else "Waxing Gibbous 🌔"
    elif deg < 195.0:
        return "Pleine Lune / Badr (Full Moon) 🌕" if lang == "fr" else "Full Moon 🌕"
    elif deg < 255.0:
        return "Gibbeuse Décroissante (Waning Gibbous) 🌖" if lang == "fr" else "Waning Gibbous 🌖"
    elif deg < 285.0:
        return "Dernier Quartier (Third Quarter) 🌗" if lang == "fr" else "Third Quarter 🌗"
    else:
        return "Dernier Croissant (Waning Crescent) 🌘" if lang == "fr" else "Waning Crescent 🌘"

def calculate_lunar_month(dt: datetime):
    """Calculate the lunar month encompassing the given datetime."""
    astro_time = astronomy.Time.Make(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second + dt.microsecond / 1e6)
    
    # Previous New Moon (Start of current lunar month)
    prev_nm = astronomy.SearchMoonPhase(0.0, astro_time, -35.0)
    # Next New Moon (End of current lunar month)
    next_nm = astronomy.SearchMoonPhase(0.0, astro_time, +35.0)
    
    # Intermediate quarters
    fq = astronomy.SearchMoonPhase(90.0, prev_nm, 35.0)
    fm = astronomy.SearchMoonPhase(180.0, prev_nm, 35.0)
    tq = astronomy.SearchMoonPhase(270.0, prev_nm, 35.0)
    
    illum = astronomy.Illumination(astronomy.Body.Moon, astro_time)
    phase_deg = astronomy.MoonPhase(astro_time)
    
    total_days = next_nm.ut - prev_nm.ut
    age_days = astro_time.ut - prev_nm.ut
    cal_days = 30 if total_days >= 29.5 else 29
    
    days_int = int(total_days)
    hours = int((total_days - days_int) * 24)
    mins = int((((total_days - days_int) * 24) - hours) * 60)
    secs = int((((((total_days - days_int) * 24) - hours) * 60) - mins) * 60)
    
    # Calculate Perigee (min distance) and Apogee (max distance) during this lunation
    curr = prev_nm
    min_km = float('inf')
    max_km = float('-inf')
    min_time = None
    max_time = None
    step_hours = 1.0 / 24.0
    while curr.ut <= next_nm.ut:
        d = astronomy.GeoVector(astronomy.Body.Moon, curr, True).Length() * astronomy.KM_PER_AU
        if d < min_km:
            min_km = d
            min_time = curr
        if d > max_km:
            max_km = d
            max_time = curr
        curr = curr.AddDays(step_hours)

    return {
        "datetime_utc": dt.strftime("%Y-%m-%d %H:%M:%S UTC"),
        "prev_new_moon": prev_nm.Utc().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "first_quarter": fq.Utc().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "full_moon": fm.Utc().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "third_quarter": tq.Utc().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "next_new_moon": next_nm.Utc().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "total_days": total_days,
        "cal_days": cal_days,
        "duration_str": f"{days_int} jours, {hours}h {mins}m {secs}s",
        "age_days": age_days,
        "age_str": f"Jour {age_days:.2f} / {total_days:.2f} jours ({ (age_days/total_days)*100:.1f}% du cycle)",
        "illumination_pct": illum.phase_fraction * 100.0,
        "phase_deg": phase_deg,
        "perigee_km": min_km,
        "perigee_date": min_time.Utc().strftime("%Y-%m-%d %H:%M UTC"),
        "apogee_km": max_km,
        "apogee_date": max_time.Utc().strftime("%Y-%m-%d %H:%M UTC")
    }

def print_lunar_month_report(dt: datetime, lang: str = "fr"):
    info = calculate_lunar_month(dt)
    phase_name = get_moon_phase_name(info["phase_deg"], lang=lang)
    
    print("\n" + "=" * 90)
    title = "🌙 CALCUL DU MOIS LUNAIRE (LUNAR MONTH : 29 / 30 JOURS) 🌙"
    print(title.center(90))
    print(f"Date d'observation : {info['datetime_utc']}".center(90))
    print("=" * 90)
    
    print(f"  • Statut du Mois Lunaire   : MOIS DE {info['cal_days']} JOURS ({info['duration_str']})")
    print(f"  • Âge de la Lune           : {info['age_str']}")
    print(f"  • Phase Actuelle           : {phase_name}")
    print(f"  • Illumination du Disque   : {info['illumination_pct']:.1f}%")
    print(f"  • Angle de Phase           : {info['phase_deg']:.1f}°")
    print("-" * 90)
    print("  🗓️ CALENDRIER DES 4 PHASES DU MOIS EN COURS :")
    print(f"    🌑 Nouvelle Lune (Début du mois) : {info['prev_new_moon']}")
    print(f"    🌓 Premier Quartier              : {info['first_quarter']}")
    print(f"    🌕 Pleine Lune (Milieu du mois)  : {info['full_moon']}")
    print(f"    🌗 Dernier Quartier              : {info['third_quarter']}")
    print(f"    🌑 Nouvelle Lune (Fin du mois)   : {info['next_new_moon']}")
    print("-" * 90)
    print("  📏 DISTANCES EXTRÊMES DE CE MOIS LUNAIRE :")
    print(f"    🟢 Périgée (Plus proche de la Terre) : {info['perigee_km']:>12,.1f} km le {info['perigee_date']}")
    print(f"    🔴 Apogée  (Plus loin de la Terre)   : {info['apogee_km']:>12,.1f} km le {info['apogee_date']}")
    print("=" * 90 + "\n")

def print_lunar_year(year: int, lang: str = "fr"):
    t_start = astronomy.Time.Make(year, 1, 1, 0, 0, 0)
    t_end = astronomy.Time.Make(year + 1, 1, 1, 0, 0, 0)
    
    print("\n" + "=" * 105)
    title = f"🗓️ TOUS LES MOIS LUNAIRES DE L'ANNÉE {year} (29 OU 30 JOURS)"
    print(title.center(105))
    print("=" * 105)
    header = f"{'N°':<4} | {'Début (Nouvelle Lune)':<22} | {'Pleine Lune (Badr)':<20} | {'Fin (Nouv. Lune)':<20} | {'Durée':<12} | {'Type':<12}"
    print(header)
    print("-" * 105)
    
    nm = astronomy.SearchMoonPhase(0.0, t_start, -35.0)
    idx = 1
    count_29 = 0
    count_30 = 0
    
    while nm.ut < t_end.ut:
        next_nm = astronomy.SearchMoonPhase(0.0, nm.AddDays(1.0), 35.0)
        fm = astronomy.SearchMoonPhase(180.0, nm, 35.0)
        dur = next_nm.ut - nm.ut
        cal_days = 30 if dur >= 29.5 else 29
        if cal_days == 29:
            count_29 += 1
        else:
            count_30 += 1
            
        days_int = int(dur)
        hours = int((dur - days_int) * 24)
        mins = int((((dur - days_int) * 24) - hours) * 60)
        dur_str = f"{days_int}j {hours:02d}h{mins:02d}"
        
        type_str = f"🟩 29 jours" if cal_days == 29 else f"🟦 30 jours"
        
        start_str = nm.Utc().strftime("%Y-%m-%d %H:%M UTC")
        full_str = fm.Utc().strftime("%Y-%m-%d %H:%M UTC")
        end_str = next_nm.Utc().strftime("%Y-%m-%d %H:%M UTC")
        
        print(f"{idx:<4} | {start_str:<22} | {full_str:<20} | {end_str:<20} | {dur_str:<12} | {type_str:<12}")
        nm = next_nm
        idx += 1
        
    print("-" * 105)
    print(f"Total année {year} : {idx-1} mois lunaires | Mois de 29 jours : {count_29} | Mois de 30 jours : {count_30}")
    print("=" * 105 + "\n")

def print_table(dt: datetime, lang: str = "en"):
    astro_time = astronomy.Time.Make(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second + dt.microsecond / 1e6)
    utc_str = dt.strftime("%Y-%m-%d %H:%M:%S UTC")
    
    title = f"🌍 EARTH DISTANCES TO CELESTIAL BODIES (DISTANCES DEPUIS LA TERRE) 🌍"
    sub = f"Date & Time: {utc_str}"
    print("\n" + "=" * 105)
    print(title.center(105))
    print(sub.center(105))
    print("=" * 105)
    
    header = f"{'Celestial Body':<20} | {'Distance (km)':<22} | {'Distance (AU)':<14} | {'Light Time':<14} | {'Radial Velocity':<20}"
    if lang == "fr":
        header = f"{'Corps Céleste':<20} | {'Distance (km)':<22} | {'Distance (UA)':<14} | {'Temps Lumière':<14} | {'Vitesse Radiale':<20}"
    print(header)
    print("-" * 105)

    for item in BODIES:
        res = calculate_distance(item["body"], astro_time)
        name = f"{item['symbol']} {item['name_' + lang] if 'name_' + lang in item else item['name_en']}"
        km_str = f"{res['km']:>18,.1f} km"
        au_str = f"{res['au']:>11.6f} AU"
        lt_str = f"{res['light_time_str']:>12}"
        
        vel = res['velocity_km_s']
        if abs(vel) < 0.001:
            vel_str = f"{vel*1000:>+8.2f} m/s (=)"
        else:
            arrow = "▼" if vel < 0 else "▲"
            vel_str = f"{arrow} {vel:>+7.3f} km/s"

        print(f"{name:<20} | {km_str} | {au_str} | {lt_str} | {vel_str:>19}")
    print("=" * 105)
    
    # Quick Lunar Month Preview
    lunar = calculate_lunar_month(dt)
    phase_name = get_moon_phase_name(lunar["phase_deg"], lang=lang)
    print(f"🌙 Mois lunaire actuel : {lunar['age_str']} | Type: Mois de {lunar['cal_days']} jours | {phase_name} ({lunar['illumination_pct']:.1f}%)")
    print("=" * 105 + "\n")

def run_live(lang: str = "en"):
    print("\033[?25l", end="")  # hide cursor
    try:
        while True:
            # Clear screen
            print("\033[H\033[J", end="")
            now = datetime.now(timezone.utc)
            print_table(now, lang=lang)
            print("  ⚡ [LIVE MODE: Refreshing every second / Actualisation chaque seconde]")
            print("  Press Ctrl+C to stop.")
            time.sleep(1.0)
    except KeyboardInterrupt:
        print("\n\nStopped.")
    finally:
        print("\033[?25h", end="")  # restore cursor

def generate_range_csv(start_dt: datetime, end_dt: datetime, step_seconds: int, output_path: str):
    print(f"Generating distances from {start_dt.isoformat()} to {end_dt.isoformat()} (step: {step_seconds}s)...")
    curr = start_dt
    rows_written = 0

    fieldnames = ["datetime_utc", "body", "distance_km", "distance_au", "distance_miles", "light_time_seconds", "velocity_km_s"]
    with open(output_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        while curr <= end_dt:
            astro_time = astronomy.Time.Make(curr.year, curr.month, curr.day, curr.hour, curr.minute, curr.second)
            dt_str = curr.strftime("%Y-%m-%d %H:%M:%S")
            for item in BODIES:
                res = calculate_distance(item["body"], astro_time)
                writer.writerow({
                    "datetime_utc": dt_str,
                    "body": item["id"],
                    "distance_km": f"{res['km']:.2f}",
                    "distance_au": f"{res['au']:.8f}",
                    "distance_miles": f"{res['miles']:.2f}",
                    "light_time_seconds": f"{res['light_seconds']:.4f}",
                    "velocity_km_s": f"{res['velocity_km_s']:.6f}"
                })
            rows_written += 1
            curr += timedelta(seconds=step_seconds)

    print(f"✅ Successfully wrote {rows_written} time steps ({rows_written * len(BODIES)} records) to: {output_path}")

def parse_date(date_str: str) -> datetime:
    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d",
        "%Y/%m/%d %H:%M:%S",
        "%Y/%m/%d %H:%M",
        "%Y/%m/%d",
        "%d/%m/%Y %H:%M:%S",
        "%d/%m/%Y",
    ]
    for fmt in formats:
        try:
            dt = datetime.strptime(date_str.strip(), fmt)
            return dt.replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    raise ValueError(f"Could not parse date string: '{date_str}'. Expected format: YYYY-MM-DD HH:MM:SS")

def start_web_server(port: int = 8080):
    import http.server
    import socketserver
    import webbrowser
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), Handler) as httpd:
        url = f"http://localhost:{port}/index.html"
        print(f"\n🚀 Web server started at {url}")
        print("Opening in your default browser...")
        try:
            webbrowser.open(url)
        except Exception:
            pass
        print("Press Ctrl+C to terminate the server.\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nWeb server stopped.")

def main():
    parser = argparse.ArgumentParser(description="Calculate exact distances between Earth and Moon, Sun, Planets + Lunar Month (29/30 days) from 2000 to now.")
    parser.add_argument("--date", "-d", help="Date & time in UTC (e.g. '2024-05-15 14:30:00' or '2000-01-01'). Defaults to now.")
    parser.add_argument("--live", "-l", action="store_true", help="Live mode updating every second in the terminal.")
    parser.add_argument("--lang", choices=["en", "fr"], default="fr", help="Language: 'fr' (Français, default) or 'en' (English).")
    parser.add_argument("--lunar", "-m", action="store_true", help="Display full Lunar Month report (durée 29 ou 30 jours, phases, âge, périgée, apogée).")
    parser.add_argument("--lunar-year", type=int, metavar="YEAR", help="List all lunar months of a year (e.g. --lunar-year 2026) indicating 29 or 30 days.")
    parser.add_argument("--range", nargs=2, metavar=("START", "END"), help="Calculate a time range, e.g. --range 2000-01-01 2026-11-16")
    parser.add_argument("--step", choices=["second", "minute", "hour", "day", "week", "month"], default="day", help="Step size for range calculation (default: day).")
    parser.add_argument("--output", "-o", default="earth_distances.csv", help="Output CSV path for range mode.")
    parser.add_argument("--web", "-w", action="store_true", help="Launch the interactive web application in browser.")
    parser.add_argument("--port", type=int, default=8080, help="Port for web server (default: 8080).")

    args = parser.parse_args()

    if args.web:
        start_web_server(args.port)
        return

    if args.lunar_year:
        print_lunar_year(args.lunar_year, lang=args.lang)
        return

    # Single date
    if args.date:
        dt = parse_date(args.date)
    else:
        dt = datetime.now(timezone.utc)

    if args.lunar:
        print_lunar_month_report(dt, lang=args.lang)
        return

    if args.live:
        run_live(args.lang)
        return

    if args.range:
        start_dt = parse_date(args.range[0])
        end_dt = parse_date(args.range[1])
        step_map = {
            "second": 1,
            "minute": 60,
            "hour": 3600,
            "day": 86400,
            "week": 7 * 86400,
            "month": 30 * 86400,
        }
        step_sec = step_map[args.step]
        generate_range_csv(start_dt, end_dt, step_sec, args.output)
        return

    print_table(dt, lang=args.lang)

if __name__ == "__main__":
    main()
