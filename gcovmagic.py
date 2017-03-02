#! /usr/bin/env python

import os
import subprocess
import argparse
import glob

def main():
	
	parser = argparse.ArgumentParser()
	parser.add_argument('FileToTest', help='File to test coverage of')
	parser.add_argument('Tests', help='Test files to compile', nargs='+')
	args = parser.parse_args()
	
	FileToTest = args.FileToTest[:-4]
	
	subprocess.call(['g++', '-std=c++11', '-g', '-O0', '--coverage', args.FileToTest, '-c', '-o', FileToTest+'.o'])
	
	for test in args.Tests:
		subprocess.call(['g++', '-std=c++11', '-g', '-O0', '--coverage', test, '-c', '-o', test[:-4]+'_cov.o'])
		subprocess.call(['g++', '-std=c++11', '-g', '--coverage', FileToTest+'.o', test[:-4]+'_cov.o', '-o', test[:-4]+'_cov'])
	
	for test in args.Tests:
		subprocess.call(['./' + test[:-4]+'_cov'])
		
	subprocess.call(['gcov', args.FileToTest])
	subprocess.call(['mv', args.FileToTest+'.gcov', 'coverage.txt'])
	
	clean()
	
def clean():
	
	files = glob.glob('*.gcda')
	for file in files:
		os.remove(file)
		
	files = glob.glob('*.gcno')
	for file in files:
		os.remove(file)
		
	files = glob.glob('*.gcov')
	for file in files:
		os.remove(file)
		
	files = glob.glob('*_cov')
	for file in files:
		os.remove(file)
		
	files = glob.glob('*.o')
	for file in files:
		os.remove(file)
	
if __name__ == '__main__':
    main()