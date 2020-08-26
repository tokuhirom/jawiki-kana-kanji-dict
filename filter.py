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

        def worker(queue):
            while True:
                item = queue.get()
                if item == None:
                    break

                title, kanji, yomi = item
                m = wikipedia_filter.filter_entry(title, kanji, yomi)
                if m:
                    kanji, yomi = m
                    ofh.write("%s\t%s\n" % (
                        kanji.replace("\t", " "),
                        yomi.replace("\t", " "),
                    ))

                queue.task_done()

        queue = mp.JoinableQueue()
        with mp.Pool(7, worker, (queue,)) as pool:
            print("Start processing")
            with open(srcfname, 'r', encoding='utf-8') as fp:
                for line in fp:
                    line = line.strip()
                    splitted = line.split("\t")
                    if len(splitted) != 3:
                        continue
                    queue.put(splitted)

            queue.join()
            queue.close()

        print("Filtered in " + str(time.time()-t0) + " seconds")

