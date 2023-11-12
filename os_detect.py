import sys

def detect(sys):
    if sys == "aix":
        os = "aix"
    elif sys == "linux":
        os = "Linux"
    elif sys == "win32":
        os = "Windows"
    elif sys == "cygwin":
        os = "Windows"
    elif sys == "darwin":
        os = "MacOS"
    else:
        os = "unknown"
    return os

if __name__ == "__main__":
    # example
    os = detect(sys.platform)
    print(f"Current OS: {os}")