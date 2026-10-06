from fastapi import APIRouter, HTTPException
from pathlib import Path

# CPU Paths
cpu_info_path = Path("/proc/cpuinfo")
cpu_temp_path = Path("/sys/class/thermal/thermal_zone0/temp")
# Memory Paths
memory_usage_path = Path("/proc/meminfo")
# System Paths
system_uptime_path = Path("/proc/uptime")
load_average_path = Path("/proc/loadavg")

router = APIRouter()

def get_cpu_info():
    raw_info = cpu_info_path.read_text().strip()

    cpu_data = {}

    for line in raw_info.splitlines():
        if ":" not in line:
            continue

        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()

        if key == "vendor_id":
            cpu_data["vendor_id"] = value

        elif key == "model name":
            cpu_data["model_name"] = value

        elif key == "cpu MHz":
            cpu_data["cpu_mhz"] = float(value)

        if len(cpu_data) == 3:
            break

    raw_temp = cpu_temp_path.read_text().strip()
    temp_c = round(int(raw_temp) / 1000, 1)

    cpu_data["cpu_temp_c"] = temp_c

    return cpu_data

def get_mem_info():
    raw_memory = memory_usage_path.read_text().strip()

    mem_data = {}

    for line in raw_memory.splitlines():
        if ":" not in line:
            continue

        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()

        value_kb = int(value.split()[0])

        if key == "MemTotal":
            mem_data["mem_total"] = value_kb

        elif key == "MemFree":
            mem_data["mem_free"] = value_kb

        elif key == "MemAvailable":
            mem_data["mem_available"] = value_kb

        if len(mem_data) == 3:
            break

    mem_data["mem_used"] = (
        mem_data["mem_total"] - mem_data["mem_available"]
    )
    mem_data["mem_usage_percent"] = round(
        mem_data["mem_used"] / mem_data["mem_total"] * 100,
        2
    )

    return mem_data

def get_system_info():
    system_data = {}

    raw_uptime = system_uptime_path.read_text().strip()
    uptime_seconds = float(raw_uptime.split()[0])

    raw_load = load_average_path.read_text().strip()
    load_values = raw_load.split()

    system_data["uptime_seconds"] = round(uptime_seconds, 2)
    system_data["load_15_min"] = float(load_values[2])

    return system_data

@router.get("/api/telemetry")
async def get_telemetry():
    try:
        cpu_data = get_cpu_info()
        mem_data = get_mem_info()
        system_data = get_system_info()

        return {
            "CPU": {
                "vendor_id": cpu_data["vendor_id"],
                "model_name": cpu_data["model_name"],
                "cpu_frequency_mhz": cpu_data["cpu_mhz"],
                "cpu_temp_c": cpu_data["cpu_temp_c"],
            },
            "MEMORY": {
                "mem_total_kb": mem_data["mem_total"],
                "mem_free_kb": mem_data["mem_free"],
                "mem_available_kb": mem_data["mem_available"],
                "mem_used_kb": mem_data["mem_used"],
                "mem_usage_percent": mem_data["mem_usage_percent"],
            },
            "SYSTEM": {
                "uptime_seconds": system_data["uptime_seconds"],
                "load_15_min": system_data["load_15_min"],
            }
        }

    except (FileNotFoundError, ValueError, PermissionError, KeyError):
        raise HTTPException(
            status_code=500,
            detail="Unable to read system telemetry"
        )