#! /usr/bin/env python

import os
import subprocess
import argparse
import glob

def main():
	
	parser = argparse.ArgumentParser()
	parser.add_argument('FileToTest', help='File to test coverage of')
	parser.add_argument('-t', help='Test files to compile', nargs='+', dest='tests')
	parser.add_argument('-d', help='Dependencies to link with test files', nargs='*', dest='testDeps')
	
	args = parser.parse_args()
	
	FileToTest = args.FileToTest[:-4]
	tests = args.tests
	testDeps = args.testDeps
	
	testDepObjs = []
	
	for testDep in testDeps:
		subprocess.call(['g++', '-std=c++11', '-g', '-O0', '--coverage', testDep, '-c', '-o', testDep[:-4]+'.o'])
		testDepObjs.append(testDep[:-4]+'.o')
	
	for test in tests:
		subprocess.call(['g++', '-std=c++11', '-g', '-O0', '--coverage', test, '-c', '-o', test[:-4]+'_cov.o'])
		subprocess.call(['g++', '-std=c++11', '-g', '--coverage'] + testDepObjs + [test[:-4]+'_cov.o', '-o', test[:-4]+'_cov'])
	
	for test in tests:
		subprocess.call(['./' + test[:-4]+'_cov'])
		
	gcovOutput = subprocess.check_output(['gcov', args.FileToTest]).split('\n')
	print(gcovOutput[0])
	print(gcovOutput[1])
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