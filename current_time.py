from time import gmtime, strftime

def current_time():
    return strftime("%Y-%m-%d %H:%M:%S", gmtime())
