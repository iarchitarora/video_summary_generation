import argparse

parser = argparse.ArgumentParser(description="integer input")

parser.add_argument('-i','--out', '--input-in',"--pin-to", type=float,
     default=10, help="input video")
args = parser.parse_args()
def run2():
    print("from import")
def run():
    print("from main")
    print("the number is: ", args.out)

if __name__ == '__main__':
    run()
else:
    run2()