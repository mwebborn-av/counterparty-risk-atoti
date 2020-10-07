import datetime as dt
import time


# Log event with timestamp
def log_event(event):
    timestamp = dt.datetime.now().strftime("%H:%M:%S")
    print("[" + timestamp + "] " + event)


# Return current time in ms
def current_milli_time():
    return int(round(time.time() * 1000))


# Print execution time of a process
def print_execution_time(stage, start):
    log_event(stage + " complete in " + (current_milli_time() - start).__str__() + "ms")


# Execute any function and record timings
def execute(function, args, event_name):
    before = current_milli_time()
    var = function(**args)

    if event_name is not None:
        print_execution_time(stage=event_name, start=before)
    else:
        print_execution_time(stage=function.__name__, start=before)

    if var is not None:
        return var
