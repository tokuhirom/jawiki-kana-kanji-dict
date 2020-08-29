import logging
import multiprocessing as mp

from jawiki import converter

if __name__ == '__main__':
    import time

    logger = mp.log_to_stderr()
    logger.setLevel(logging.INFO)

    t0 = time.time()

    with open('converted.tsv', 'w', encoding='utf-8') as ofh:
        jawiki_converter = converter.Converter()

        def worker(chunk):
            results = []
            for line in chunk:
                splitted = line.strip().split("\t")
                if len(splitted) != 3:
                    continue
                title, kanji, yomi = splitted
                kanji, yomi = jawiki_converter.convert(kanji, yomi)
                if len(yomi) > 0:
                    results.append([kanji, yomi])
            return results

        numprocs = mp.cpu_count()
        pool = mp.Pool(processes=numprocs)
        with open('pre_validated.tsv', 'r', encoding='utf-8') as fp:
            results_pool = []
            buf = []
            for line in fp:
                buf.append(line)
                if len(buf) > 20000:
                    result = pool.apply_async(worker, args=(buf,))
                    results_pool.append(result)
                    buf = []
            if len(buf) > 0:
                result = pool.apply_async(worker, args=(buf,))
                results_pool.append(result)

            finished_cnt = 0
            pool_size = len(results_pool)
            while len(results_pool) > 0:
                for r in results_pool:
                    if r.ready():
                        results = r.get()
                        for result in results:
                            kanji, yomi = result
                            ofh.write(f"{kanji}\t{yomi}\n")
                        finished_cnt += 1
                        results_pool.remove(r)
                time.sleep(0.1)
                print(f"{finished_cnt}/{pool_size}")

    print(f"Converted in {str(time.time() - t0)} seconds")
