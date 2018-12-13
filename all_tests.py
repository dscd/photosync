import fnmatch
import os
import unittest


def get_files(start_path, pattern='*_test.py'):
  """Gets recursive file list.

   Gets recursive file list starting from start_path and using pattern for
   filter
  """
  for (dirpath, dirnames, filenames) in os.walk(start_path):
    for filename in fnmatch.filter(filenames, pattern):
      yield os.path.relpath(os.path.join(dirpath, filename))
  

def main():
  start_dir = os.path.abspath(os.path.dirname(__file__))
  modules = [f.replace('/', '.').replace('\\', '.')[:-3]
             for f in get_files(start_dir)]
  suites = [unittest.defaultTestLoader.loadTestsFromName(m) for m in modules]
  suite = unittest.TestSuite(suites)
 
  runner = unittest.TextTestRunner()
  runner.run(suite)


if __name__ == '__main__':
  main()
