import logging
import multiprocessing as mp
import time


class FileProcessor:
    def __init__(self):
        logger = mp.log_to_stderr()
        logger.setLevel(logging.INFO)
        self.logger = logger

    def run(self, srcfname: str, worker, writer):
        t0 = time.time()
        results_pool = self.read(srcfname, worker)
        self.write(results_pool, writer)
        self.logger.info(f"Converted in {str(time.time() - t0)} seconds")

    def read(self, srcfname, worker, chunksize=20000):
        numprocs = mp.cpu_count()
        pool = mp.Pool(processes=numprocs)
        results_pool = []
        with open(srcfname, 'r', encoding='utf-8') as fp:
            buf = []
            for line in fp:
                buf.append(line)
                if len(buf) > chunksize:
                    results_pool.append(pool.apply_async(worker, args=(buf,)))
                    buf = []
            if len(buf) > 0:
                results_pool.append(pool.apply_async(worker, args=(buf,)))
        return results_pool

    def write(self, results_pool, writer):
        finished_cnt = 0
        pool_size = len(results_pool)
        while len(results_pool) > 0:
            for r in results_pool:
                if r.ready():
                    results = r.get()
                    for result in results:
                        writer(result)
                    finished_cnt += 1
                    results_pool.remove(r)
            time.sleep(0.1)
            self.logger.info(f"{finished_cnt}/{pool_size}")
