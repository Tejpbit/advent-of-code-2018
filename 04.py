import re
from datetime import datetime, timedelta
f = open("04.data")
lines = f.readlines()


reg = re.compile(
    '\[(.+)\]\ (?:(falls asleep|wakes up|Guard \#\d+ begins shift))')


def get_type(str):
    if str.startswith("Guard"):
        parts = str.split(" ")
        return " ".join(parts[2:])
    else:
        return str


def get_guard_id(str):
    parts = groups[1].split(" ")
    return int(parts[1][1:])


events = []

for line in lines:
    groups = reg.findall(line)[0]
    date = groups[0]

    event = groups[1]

    guard_id = get_guard_id(
        groups[1]) if groups[1].startswith('Guard') else None

    event = {
        "event_type": get_type(groups[1]),
        "date": datetime.strptime(date, '%Y-%m-%d %H:%M'),
        "guard_id": guard_id
    }
    events += [event]

events = sorted(events, key=lambda x: x['date'])


def minute_diff(start, end):
    td = (end-start)
    return td.seconds / 60


def get_guard_with_most_sleep_time(events):
    sleeping_time_per_guard = {}
    active_guard = None
    fell_asleep_at = None
    for event in events:
        if event['guard_id']:
            active_guard = event['guard_id']
        elif event['event_type'] == 'falls asleep':
            fell_asleep_at = event['date']
        elif event['event_type'] == 'wakes up':
            if active_guard not in sleeping_time_per_guard:
                sleeping_time_per_guard[active_guard] = 0
            sleeping_time_per_guard[active_guard] += minute_diff(
                fell_asleep_at, event['date'])

    return max(sleeping_time_per_guard.items(), key=lambda x: x[1])


guard_with_most_sleeping_time = get_guard_with_most_sleep_time(events)
print(guard_with_most_sleeping_time)


def get_most_sleeping_minute_for_guard(guard_id, events):

    guards_sleeping_time_per_minute = {}

    fell_asleep_at = None
    active_guard = None
    for event in events:
        if event['guard_id']:
            active_guard = event['guard_id']
        elif event['event_type'] == 'falls asleep':
            fell_asleep_at = event['date']
        elif event['event_type'] == 'wakes up':
            current = fell_asleep_at
            while current < event['date']:
                if active_guard not in guards_sleeping_time_per_minute:
                    guards_sleeping_time_per_minute[active_guard] = {}
                if current.minute not in guards_sleeping_time_per_minute[active_guard]:
                    guards_sleeping_time_per_minute[active_guard][current.minute] = 0
                guards_sleeping_time_per_minute[active_guard][current.minute] += 1
                current += timedelta(0, 60)

    return guards_sleeping_time_per_minute


guards_sleeping_time_per_minute = get_most_sleeping_minute_for_guard(
    guard_with_most_sleeping_time[0], events)
print(max(guards_sleeping_time_per_minute[guard_with_most_sleeping_time[0]].items(
), key=lambda x: x[1]))


max_sleeping_time_during_a_minute = 0
guard_with_most_sleeping_time_during_single_minute = 0
minute_on_which_guard_sleept_most = 0
for (guard, sleeping_time_per_minute) in guards_sleeping_time_per_minute.items():
    for (minute, sleeping_time) in sleeping_time_per_minute.items():
        if sleeping_time > max_sleeping_time_during_a_minute:
            max_sleeping_time_during_a_minute = sleeping_time
            guard_with_most_sleeping_time_during_single_minute = guard
            minute_on_which_guard_sleept_most = minute

print('max_sleeping_time_during_a_minute ', max_sleeping_time_during_a_minute)
print('guard_with_most_sleeping_time_during_single_minute ',
      guard_with_most_sleeping_time_during_single_minute)
print('minute_on_which_guard_sleept_most ', minute_on_which_guard_sleept_most)

# a = max(guards_sleeping_time_per_minute.items(), key=lambda x:
#     max(x[1].items(), key=lambda x: x[1])
# )
# print(a[0], max(a[1].values()))
