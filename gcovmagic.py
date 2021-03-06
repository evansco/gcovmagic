#! /usr/bin/env python

import os
import subprocess
import argparse
import glob

def main():
	
	# Set up command line arguments
	parser = argparse.ArgumentParser()
	parser.add_argument('FileToTest', help='File to test coverage of')
	parser.add_argument('-t', help='Test files to compile', nargs='+', dest='tests')
	parser.add_argument('-d', help='Dependencies to link with test files', nargs='*', dest='testDeps')
	
	# Parse command line args into list
	args = parser.parse_args()
	
	# Grab filenames needed
	FileToTest = args.FileToTest[:-4]
	tests = args.tests
	testDeps = args.testDeps
	
	# Compile the file to test the coverage of
	subprocess.call(['g++', '-std=c++11', '-g', '-O0', '--coverage', FileToTest+'.cpp', '-c', '-o', FileToTest[:-4]+'.o'])
	
	testDepObjs = []
	
	# Compile the object file for each dependency of the tests
	for testDep in testDeps:
		subprocess.call(['g++', '-std=c++11', '-g', '-O0', '--coverage', testDep, '-c', '-o', testDep[:-4]+'.o'])
		testDepObjs.append(testDep[:-4]+'.o')
	
	# Compile the object file for each test,
	# 	then link test and dependency object files to make executable tests
	for test in tests:
		subprocess.call(['g++', '-std=c++11', '-g', '-O0', '--coverage', test, '-c', '-o', test[:-4]+'_cov.o'])
		subprocess.call(['g++', '-std=c++11', '-g', '--coverage'] + testDepObjs + [test[:-4]+'_cov.o', '-o', test[:-4]+'_cov'])
	
	# Run each test
	for test in tests:
		subprocess.check_output(['./' + test[:-4]+'_cov'])
	
	# Print gcov's output for the file whose coverage was tested
	gcovOutput = subprocess.check_output(['gcov', args.FileToTest]).split('\n')
	print(gcovOutput[0])
	print(gcovOutput[1])
	
	# Save gcov's output to a more visible file
	subprocess.call(['mv', args.FileToTest+'.gcov', 'coverage.txt'])
	
	# Clean up intermediate files created during script execution
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