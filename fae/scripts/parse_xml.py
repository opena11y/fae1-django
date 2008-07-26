import sys
from lxml import etree

#------------------------------------------------
def main():
    if len(sys.argv) < 2:
        print 'Please provide XML filename!'
        sys.exit(0)
    filename = sys.argv[1]
    parser = etree.XMLParser(dtd_validation=True)
    try:
        tree = etree.parse(filename, parser)
    except etree.XMLSyntaxError:
        # print 'Parsing errors occurred!'
        for error in parser.error_log:
            print error.message, 'AT LINE', error.line

if __name__ == "__main__":
    main()
