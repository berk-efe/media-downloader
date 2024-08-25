from datetime import timedelta
import re

def strip_ansi_codes(text):
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)


def strip_extra_letters(text, lenght):
    count = 0
    result = []
    for letter in text:
        if count < lenght:
            result.append(letter)
            count += 1
            continue
        else:
            result.append("...")
            return "".join(result)

def format_bytes(bytes):
    if bytes >= 1024*1024:  # 1 MB
        return f"{bytes / 1024*1024:.2f} MB"
    elif bytes >= 1024:  # 1 KB
        return f"{bytes / 1024:.2f} KB"
    else:
        return f"{bytes} bytes"

def format_speed(speed):
    if speed >= 1024*1024:  # 1 MB
        return f"{speed / 1024*1024:.2f} MB/s"
    elif speed >= 1024:  # 1 KB
        return f"{speed / 1024:.2f} KB/s"
    else:
        return f"{speed} bytes/s"

def format_time(seconds):
    delta = timedelta(seconds=seconds)
    hours, remainder = divmod(delta.seconds, 60 * 60)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

if __name__ == "__main__":
    pass
