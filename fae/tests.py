import unittest
import sys
from datetime import datetime

from evaluate import download_resources, analyze_resources

def message(obj, frame):
    """Construct a test message that includes the method and class names."""

    method_name = frame.f_code.co_name
    class_name  = obj.__class__.__name__
    return '\nRunning ' + method_name + ' in ' + class_name + '...\n'

class SystemCallsTestCase(unittest.TestCase):
    def setUp(self):
        self.params = {
            'url': 'http://www.ibm.com',
            'title': 'IBM Test Report',
            'depth': '2',
            'span': '1',
            'username': 'user1',
            }
        self.is_logged_in = True
        self.uid = 'abcdef0123456789'
        self.timestamp = datetime.now()

    def testDownloadResources(self):
        """Examine the wget command line called by download_resources."""
        print message(self, sys._getframe())
        print download_resources(self.params, self.is_logged_in, self.uid, test=True)

    def testAnalyzeResources(self):
        """Examine the wamt command line called by analyze_resources."""
        print message(self, sys._getframe())
        print analyze_resources(self.params, self.is_logged_in, self.uid, self.timestamp, test=True)
