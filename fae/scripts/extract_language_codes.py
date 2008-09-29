"""
Extract the two-character language codes from IANA text file
at http://www.iana.org/assignments/language-subtag-registry.
"""

def main():
    f = open('language-subtag-registry', mode='r')
    codes = []

    for line in f:
        if line.startswith('Type: language'):
            subtag = f.next().strip().split(': ')[1]
            if len(subtag) == 2:
                codes.append(subtag)

    print codes
    print 'Number of codes:', len(codes)

if __name__ == '__main__':
    main()
