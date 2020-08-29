import multiprocessing as mp
import logging
from janome.tokenizer import Tokenizer
from jawiki.post_validate import PostValidator

if __name__ == '__main__':
    import time

    logger = mp.log_to_stderr()
    logger.setLevel(logging.INFO)

    t0 = time.time()

    tokenizer = Tokenizer("user_simpledic.csv", udic_type="simpledic", udic_enc="utf8")

    post_validator = PostValidator(tokenizer)

    def worker(chunk):
        results = []
        for line in chunk:
            splitted = line.strip().split("\t")
            if len(splitted) != 2:
                continue
            kanji, yomi = splitted
            skip_reason = post_validator.post_validate(kanji, yomi)
            results.append([kanji, yomi, skip_reason])
        return results

    numprocs = mp.cpu_count()
    pool = mp.Pool(processes=numprocs)
    results_pool = []
    with open('dat/converted.tsv', 'r', encoding='utf-8') as rfp:
        buf = []
        for line in rfp:
            buf.append(line)
            if len(buf) > 20000:
                result = pool.apply_async(worker, args=(buf,))
                results_pool.append(result)
                buf = []
        if len(buf) > 0:
            result = pool.apply_async(worker, args=(buf,))
            results_pool.append(result)

    with open('logs/skipped.log', 'w', encoding='utf-8') as skipfp, \
            open('dat/post_validated.tsv', 'w', encoding='utf-8') as wfp:
        finished_cnt = 0
        total_pool_cnt = len(results_pool)
        while len(results_pool):
            for r in [r for r in results_pool if r.ready()]:
                results = r.get()
                for result in results:
                    kanji, yomi, skip_reason = result
                    if skip_reason:
                        skipfp.write(f"{skip_reason}\t{kanji}\t{yomi}\n")
                    else:
                        wfp.write(f"{kanji}\t{yomi}\n")
                finished_cnt += 1
                print(f"{finished_cnt}/{total_pool_cnt}")
                results_pool.remove(r)
            time.sleep(0.1)

    print(f"Post validated in {str(time.time() - t0)} seconds")
