from datetime import datetime, timedelta
import re
import locale

def parse_time(time_str):
    """
    Konversi format waktu yang berbeda ke format datetime.
    """
    if "|" in time_str:
        time_str = time_str.split("|")[1].strip()
        
    if "yang lalu" in time_str:
        return parse_relative_time(time_str)
    else:
        return parse_absolute_time(time_str)

def parse_relative_time(relative_str):
    """
    Konversi waktu relatif (misal: '9 jam yang lalu') ke datetime.
    """
    now = datetime.now()
    match = re.match(r"(\d+)\s+(detik|menit|jam|hari)\s+yang lalu", relative_str)

    if match:
        value = int(match[1])
        unit = match[2]

        if unit == "detik":
            return now - timedelta(seconds=value)
        elif unit == "menit":
            return now - timedelta(minutes=value)
        elif unit == "jam":
            return now - timedelta(hours=value)
        elif unit == "hari":
            return now - timedelta(days=value)

    return now

def parse_absolute_time(absolute_str):
    """
    Konversi waktu absolut (misal: 'Senin, 17 Maret 2025 / 14:02 WIB') ke datetime.
    """
    try:
        parts = absolute_str.split("/")
        if len(parts) == 2:
            date_part = parts[0].split(", ")[1].strip() 
            time_part = parts[1].split(" WIB")[0].strip() 

            formatted_date = datetime.strptime(f"{date_part} {time_part}", "%d %B %Y %H:%M")

            return formatted_date
    except Exception as e:
        print(f"Error parsing absolute time: {e}")

    return datetime.now() 


locale.setlocale(locale.LC_TIME, "id_ID.utf8")

def parse_kontan_time(kontan_time_str):
    """
    Konversi format Kontan: "| Senin, 17 Maret 2025 / 14:21 WIB" → datetime
    """
    try:
        if "|" in kontan_time_str:
            kontan_time_str = kontan_time_str.split("|")[1].strip()
        
        date_part, time_part = kontan_time_str.split(" / ")
        
        date_part = date_part.split(", ")[1]

        formatted_datetime_str = f"{date_part} {time_part}".replace(" WIB", "")

        return datetime.strptime(formatted_datetime_str, "%d %B %Y %H:%M")
    except Exception as e:
        print(f"Error parsing Kontan time: {e}")
        return datetime.now()
