from jawiki import filter
import multiprocessing as mp
import logging

if __name__=='__main__':
    import sys
    import time

    logger = mp.log_to_stderr()
    logger.setLevel(logging.INFO)

    srcfname = sys.argv[1]

    t0 = time.time()


    with open('filtered.tsv', 'w', encoding='utf-8') as ofh, \
         open('skipped.tsv', 'w', encoding='utf-8') as skipfh:

        def skip_logger(reason, line):
            skipfh.write("%s\t%s\n" % (reason.replace("\t", ' '), str(line).replace("\t", ' ')))

        wikipedia_filter = filter.WikipediaFilter(skip_logger)

        queue = mp.JoinableQueue()

        def worker(chunk):
            results = []
            for line in chunk:
                splitted = line.strip().split("\t")
                if len(splitted) != 3:
                    continue
                title, kanji, yomi = splitted
                m = wikipedia_filter.filter_entry(title, kanji, yomi)
                if m:
                    kanji, yomi = m
                    results.append([kanji, yomi])
            return results

        numprocs = mp.cpu_count()
        pool = mp.Pool(processes=numprocs)
        with open(srcfname, 'r', encoding='utf-8') as fp:
            results_pool = []
            buf = []
            for line in fp:
                buf.append(line)
                if len(buf) > 20000:
                    result = pool.apply_async(worker, args=(buf,))
                    results_pool.append(result)
                    buf = []
            if len(buf)>0:
                result = pool.apply_async(worker, args=(buf,))
                results_pool.append(result)


            while True:
                num = [ r.ready() for r in results_pool].count(True)
                for r in results_pool:
                    if r.ready():
                        results = r.get()
                        for result in results:
                            kanji, yomi = result
                            ofh.write("%s\t%s\n" % (
                                kanji.replace("\t", " "),
                                yomi.replace("\t", " "),
                            ))
                time.sleep(1)
                if num == len(results_pool):
                    break

        print("Filtered in " + str(time.time()-t0) + " seconds")

