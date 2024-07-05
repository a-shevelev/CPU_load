import asyncio
from collections import defaultdict
from datetime import datetime, timedelta
import psutil
from app.cpu.models import CPULoad, ServerStatus
from app.database.models import postgres_accessor

async def save_cpu_load():
    while True:
        cpu_load_value = psutil.cpu_percent(interval=0)
        async with postgres_accessor.db.transaction():
            await CPULoad.create(load=cpu_load_value, timestamp=datetime.now())
        print(f"Saved CPU load: {cpu_load_value}")
        await asyncio.sleep(5)



async def get_server_status_last_hour():
    last_hour = datetime.now() - timedelta(hours=1)
    statuses = await ServerStatus.query.where(ServerStatus.timestamp >= last_hour).order_by(ServerStatus.timestamp).gino.all()
    print(statuses)
    return statuses


async def get_average_load_per_minute():
    cpu_loads = await get_cpu_load_last_hour()

    average_loads_per_minute = defaultdict(list)

    for load in cpu_loads:
        minute = load.timestamp.replace(second=0, microsecond=0)
        minute_str = minute.strftime('%Y-%m-%d %H:%M:%S')
        average_loads_per_minute[minute_str].append(load.load)



    average_load_per_minute = {}
    for minute_str, loads in average_loads_per_minute.items():
        float_loads = [load for load in loads if isinstance(load, float)]
        if float_loads:
            average_load_per_minute[minute_str] = sum(float_loads) / len(float_loads)
        else:
            average_load_per_minute[minute_str] = None

    return average_load_per_minute



async def get_cpu_load_last_hour():
    last_hour = datetime.now() - timedelta(hours=1)
    statuses = await ServerStatus.query.where(ServerStatus.timestamp >= last_hour).order_by(ServerStatus.timestamp).gino.all()

    off_periods = []
    current_off_start = last_hour

    for status in statuses:
        if status.status == "STOP":
            current_off_start = status.timestamp
        elif status.status == "START" and current_off_start is not None:
            off_periods.append((current_off_start, status.timestamp))
            current_off_start = None

    if current_off_start is not None:
        off_periods.append((current_off_start, datetime.now()))

    cpu_loads = await CPULoad.query.where(CPULoad.timestamp >= last_hour).order_by(CPULoad.timestamp).gino.all()

    interpolated_cpu_loads = []
    index = 0

    for start, end in off_periods:
        while (index < len(cpu_loads)) and (cpu_loads[index].timestamp < start):
            interpolated_cpu_loads.append(cpu_loads[index])
            index += 1

        current_time = start
        while current_time < end:
             interpolated_cpu_loads.append(CPULoad(timestamp=current_time, load=None))
             current_time += timedelta(seconds=5)
        # interpolated_cpu_loads.append(CPULoad(timestamp=start, load=None))
        # interpolated_cpu_loads.append(CPULoad(timestamp=end, load=None))


        while (index < len(cpu_loads)) and (cpu_loads[index].timestamp < end):
            index += 1

    while index < len(cpu_loads):
        interpolated_cpu_loads.append(cpu_loads[index])
        index += 1
        
    #print(interpolated_cpu_loads)

    return interpolated_cpu_loads


