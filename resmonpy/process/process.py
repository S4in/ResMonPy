import psutil


def get_pid(process_names):
    process_dict = {}
    for proc in psutil.process_iter(['pid', 'name']):
        try:

            if proc.info['name'] in process_names:
                process_dict[int(proc.info["pid"])] = proc.info['name']
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return process_dict



