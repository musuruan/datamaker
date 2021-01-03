#!/usr/bin/python3

import os
import sys
import argparse

def main():
	parser = argparse.ArgumentParser(description='C64 data maker')
	parser.add_argument('filename', type=str, nargs='?', help='C64 file')
	parser.add_argument('-d', '--dec', action='store_true', help='decimal mode (default)')		
	parser.add_argument('-x', '--hex', action='store_true', help='hexadecimal mode')			
	parser.add_argument('-p', '--pad', action='store_true', help='data padding (default off)')			
	parser.add_argument('--linestart', type=int, default=1000, help='first data line (default=1000)')	
	parser.add_argument('--lineinc', type=int, default=10, help='increment (default=10')
	parser.add_argument('--dataperline', type=int, help='maximum number of data per line (default=unbounded)')

	args = parser.parse_args()
	filename = args.filename

	if not filename:
		parser.print_help()
		sys.exit(1)

	if not os.path.isfile(filename):
		print("Cannot find file '{0}'".format(filename));
		sys.exit(1)
		
	with open(filename, "rb") as f:
		loadAddr = f.read(2)
		loadAddr = int.from_bytes(loadAddr, byteorder='little', signed=False)
		print("{0} === {1} ({2}) ===".format(filename, hex(loadAddr), loadAddr))

		lineNum = args.linestart
		currAddr = loadAddr-1
		dataLine = ""
		
		while True:
			b = f.read(1)
			if not b:
				break
			currAddr += 1;
			
			data = int.from_bytes(b, byteorder='little', signed=False)
			if args.hex:
				dataString = format("%X" % data)
				if args.pad:
					dataString = dataString.zfill(2)	
			else:
				dataString = format("%s" % data)
				if args.pad:
					dataString = dataString.zfill(3)	

			if ((args.dataperline is not None) and ((currAddr-loadAddr) % args.dataperline == 0)) or \
				((args.dataperline is None) and (len(dataLine)+len(dataString)+1 >= 80 or dataLine == "")):
				if dataLine != "":
					print(dataLine)
					lineNum += args.lineinc
				dataLine = format("%d DATA%s" % (lineNum, dataString))
			else:
				dataLine = format("%s,%s" % (dataLine, dataString))
		
		print(dataLine)
		print("{0} === {1} ({2}) ===".format(filename, hex(currAddr), currAddr))
			
	f.close()


if __name__ == "__main__":
	main()

