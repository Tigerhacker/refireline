from datetime import datetime

def gmt_string(time = None):
    '''Get timestamp in format as used by Fireline
    
    This format probably has an iso standard or something...'''
    
    if time is None:
        time = datetime.utcnow()
    return time.strftime("%a, %d %b %Y %H:%M:%S GMT")


def main():
    print(gmt_string())
  
if __name__== "__main__":
    main()
