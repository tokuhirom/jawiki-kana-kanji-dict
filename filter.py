from jawiki import filter

if __name__=='__main__':
    import sys
    import time

    srcfname = sys.argv[1]

    t0 = time.time()

    with open('filtered.tsv', 'w', encoding='utf-8') as ofh, \
         open('skipped.tsv', 'w', encoding='utf-8') as skipfh:

        def skip_logger(reason, line):
            skipfh.write("%s\t%s\n" % (reason.replace("\t", ' '), str(line).replace("\t", ' ')))

        wikipedia_filter = filter.WikipediaFilter(skip_logger)

        for entry in wikipedia_filter.filter(srcfname):
            ofh.write("%s\t%s\n" % (
                entry[0].replace("\t", " "),
                entry[1].replace("\t", " "),
            ))

        print("Filtered in " + str(time.time()-t0) + " seconds")

