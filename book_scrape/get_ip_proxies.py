

infile = '/Users/luoshuai/Documents/Course/InformationRetrieval/Assignments/proj/book_scrape/book_scrape/Untitled.txt'
outfile = './list.txt'

outf = open(outfile, 'w')

with open(infile, 'r') as inf:
    for line in inf:
        l = line.split()
        outf.write('http://{:s}:{:s}\n'.format(l[0], l[1]))

outf.close()

