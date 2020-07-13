import sys

if __name__ == "__main__":
    try:
        standardize_snapchat(sys.argv[1])
    except IndexError:
        print("Please enter the directory!")
