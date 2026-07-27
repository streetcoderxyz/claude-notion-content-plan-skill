#!/usr/bin/env python3
"""Resolve Vietnamese lunar-calendar holidays falling inside a solar month.

Fixed-date observances live in references/vn-holidays.md. Lunar ones (Tet, Vu Lan,
Trung Thu, ...) drift year to year and MUST NOT be guessed -- run this instead.

    python3 scripts/lunar_holidays.py 08 2026
    08/2026 lunar holidays:
      27/08/2026  Vu Lan (Ram thang 7)          [AL 15/7]

    python3 scripts/lunar_holidays.py 08 2026 --all
    # every day of the month with its lunar date, for spot checks

Algorithm: Ho Ngoc Duc's Vietnamese lunar calendar conversion (timezone UTC+7).
"""

import argparse
import math

TIMEZONE = 7

# (lunar_day, lunar_month) -> (Vietnamese name, suggested content angle)
LUNAR_HOLIDAYS = {
    (1, 1): ("Tet Nguyen Dan", "Platform: lich nghi + du tru thuoc Tet; Care: an uong ngay Tet"),
    (15, 1): ("Ram thang Gieng", "Care: an chay, tieu hoa"),
    (10, 3): ("Gio to Hung Vuong", "B: nghi le thong bao"),
    (5, 5): ("Tet Doan Ngo", "Care: diet sau bo, suc khoe duong ruot"),
    (15, 7): ("Vu Lan (Ram thang 7)", "Care: tri an cha me, suc khoe ong ba"),
    (15, 8): ("Trung Thu", "Care: an toan banh trung thu cho tre, den long"),
    (23, 12): ("Ong Cong Ong Tao", "Platform: don dep, kiem ke cuoi nam"),
}


def jd_from_date(dd, mm, yy):
    a = int((14 - mm) / 12)
    y = yy + 4800 - a
    m = mm + 12 * a - 3
    jd = dd + int((153 * m + 2) / 5) + 365 * y + int(y / 4) - int(y / 100) + int(y / 400) - 32045
    if jd < 2299161:
        jd = dd + int((153 * m + 2) / 5) + 365 * y + int(y / 4) - 32083
    return jd


def new_moon(k):
    T = k / 1236.85
    T2 = T * T
    T3 = T2 * T
    dr = math.pi / 180
    jd1 = 2415020.75933 + 29.53058868 * k + 0.0001178 * T2 - 0.000000155 * T3
    jd1 += 0.00033 * math.sin((166.56 + 132.87 * T - 0.009173 * T2) * dr)
    M = 359.2242 + 29.10535608 * k - 0.0000333 * T2 - 0.00000347 * T3
    Mpr = 306.0253 + 385.81691806 * k + 0.0107306 * T2 + 0.00001236 * T3
    F = 21.2964 + 390.67050646 * k - 0.0016528 * T2 - 0.00000239 * T3
    c1 = (0.1734 - 0.000393 * T) * math.sin(M * dr) + 0.0021 * math.sin(2 * dr * M)
    c1 -= 0.4068 * math.sin(Mpr * dr) - 0.0161 * math.sin(dr * 2 * Mpr)
    c1 -= 0.0004 * math.sin(dr * 3 * Mpr)
    c1 += 0.0104 * math.sin(dr * 2 * F) - 0.0051 * math.sin(dr * (M + Mpr))
    c1 -= 0.0074 * math.sin(dr * (M - Mpr)) - 0.0004 * math.sin(dr * (2 * F + M))
    c1 -= 0.0004 * math.sin(dr * (2 * F - M)) + 0.0006 * math.sin(dr * (2 * F + Mpr))
    c1 += 0.0010 * math.sin(dr * (2 * F - Mpr)) + 0.0005 * math.sin(dr * (2 * Mpr + M))
    if T < -11:
        deltat = 0.001 + 0.000839 * T + 0.0002261 * T2 - 0.00000845 * T3 - 0.000000081 * T * T3
    else:
        deltat = -0.000278 + 0.000265 * T + 0.000262 * T2
    return jd1 + c1 - deltat


def sun_longitude(jdn):
    T = (jdn - 2451545.0) / 36525
    T2 = T * T
    dr = math.pi / 180
    M = 357.52910 + 35999.05030 * T - 0.0001559 * T2 - 0.00000048 * T * T2
    L0 = 280.46645 + 36000.76983 * T + 0.0003032 * T2
    dl = (1.914600 - 0.004817 * T - 0.000014 * T2) * math.sin(dr * M)
    dl += (0.019993 - 0.000101 * T) * math.sin(dr * 2 * M) + 0.000290 * math.sin(dr * 3 * M)
    L = (L0 + dl) * dr
    return L - math.pi * 2 * int(L / (math.pi * 2))


def get_sun_longitude(day_number, tz):
    return int(sun_longitude(day_number - 0.5 - tz / 24.0) / math.pi * 6)


def get_new_moon_day(k, tz):
    return int(new_moon(k) + 0.5 + tz / 24.0)


def get_lunar_month_11(yy, tz):
    off = jd_from_date(31, 12, yy) - 2415021
    k = int(off / 29.530588853)
    nm = get_new_moon_day(k, tz)
    if get_sun_longitude(nm, tz) >= 9:
        nm = get_new_moon_day(k - 1, tz)
    return nm


def get_leap_month_offset(a11, tz):
    k = int((a11 - 2415021.076998695) / 29.530588853 + 0.5)
    i = 1
    arc = get_sun_longitude(get_new_moon_day(k + i, tz), tz)
    while True:
        last = arc
        i += 1
        arc = get_sun_longitude(get_new_moon_day(k + i, tz), tz)
        if arc == last or i >= 14:
            break
    return i - 1


def solar_to_lunar(dd, mm, yy, tz=TIMEZONE):
    """Return (lunar_day, lunar_month, lunar_year, is_leap_month)."""
    day_number = jd_from_date(dd, mm, yy)
    k = int((day_number - 2415021.076998695) / 29.530588853)
    month_start = get_new_moon_day(k + 1, tz)
    if month_start > day_number:
        month_start = get_new_moon_day(k, tz)
    a11 = get_lunar_month_11(yy, tz)
    b11 = a11
    if a11 >= month_start:
        lunar_year = yy
        a11 = get_lunar_month_11(yy - 1, tz)
    else:
        lunar_year = yy + 1
        b11 = get_lunar_month_11(yy + 1, tz)
    lunar_day = day_number - month_start + 1
    diff = int((month_start - a11) / 29)
    lunar_leap = 0
    lunar_month = diff + 11
    if b11 - a11 > 365:
        leap_month_diff = get_leap_month_offset(a11, tz)
        if diff >= leap_month_diff:
            lunar_month = diff + 10
            if diff == leap_month_diff:
                lunar_leap = 1
    if lunar_month > 12:
        lunar_month -= 12
    if lunar_month >= 11 and diff < 4:
        lunar_year -= 1
    return lunar_day, lunar_month, lunar_year, lunar_leap


def days_in_month(mm, yy):
    if mm == 2:
        leap = (yy % 4 == 0 and yy % 100 != 0) or yy % 400 == 0
        return 29 if leap else 28
    return 30 if mm in (4, 6, 9, 11) else 31


def main():
    ap = argparse.ArgumentParser(description="Vietnamese lunar holidays in a solar month")
    ap.add_argument("month", type=int, help="solar month, 1-12")
    ap.add_argument("year", type=int, help="solar year, e.g. 2026")
    ap.add_argument("--all", action="store_true", help="print every day with its lunar date")
    args = ap.parse_args()

    if not 1 <= args.month <= 12:
        ap.error("month must be 1-12")

    hits = []
    for dd in range(1, days_in_month(args.month, args.year) + 1):
        ld, lm, _ly, leap = solar_to_lunar(dd, args.month, args.year)
        solar = f"{dd:02d}/{args.month:02d}/{args.year}"
        lunar = f"AL {ld}/{lm}{' nhuan' if leap else ''}"
        holiday = LUNAR_HOLIDAYS.get((ld, lm)) if not leap else None
        if args.all:
            mark = f"  <== {holiday[0]}" if holiday else ""
            print(f"  {solar}  [{lunar}]{mark}")
        if holiday:
            hits.append((solar, holiday[0], holiday[1], lunar))

    if args.all:
        return

    print(f"{args.month:02d}/{args.year} lunar holidays:")
    if not hits:
        print("  (none)")
    for solar, name, angle, lunar in hits:
        print(f"  {solar}  {name:<28} [{lunar}]")
        print(f"              angle: {angle}")


if __name__ == "__main__":
    main()
