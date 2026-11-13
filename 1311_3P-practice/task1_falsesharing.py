import multiprocessing as mp
from multiprocessing import shared_memory
import ctypes
import time
from harness import run_benchmark, emit_verify_tag

def fs_worker(shm_name: str, slot_idx: int, iters: int) -> None:
    shm = shared_memory.SharedMemory(name=shm_name)
    arr = (ctypes.c_uint64 * 512).from_buffer(shm.buf)
    acc = arr[slot_idx]
    for _ in range(iters):
        acc = (acc * 6364136223846793005 + 1) & 0xFFFFFFFFFFFFFFFF
    arr[slot_idx] = acc  # Принудительная запись в общую L1 кэш-линию
    
    # КРИТИЧЕСКИ ВАЖНО: удаляем ссылку на буфер перед закрытием shared_memory
    del arr
    shm.close()

if __name__ == "__main__":
    student_id = 230103386
    p_phys = 8  # 8 физических ядер для вашего процессора Intel Core i5-13420H
    total_m = 1.6 * 10**7
    strides = [1, 2, 4, 8, 16, 32]
    
    shm = shared_memory.SharedMemory(create=True, size=4096)
    results_stride = {}
    iters_per_proc = int(total_m // p_phys)
    
    for st in strides:
        def job():
            procs = []
            for i in range(p_phys):
                slot = i * st
                p = mp.Process(target=fs_worker, args=(shm.name, slot, iters_per_proc))
                procs.append(p)
                p.start()
            for p in procs:
                p.join()
        
        stats = run_benchmark(job, warmup=1, runs=3)
        results_stride[st] = stats.median_ms
        print(f"Stride {st} (Bytes {st*8}): Median = {stats.median_ms:.2f} ms")

    tag = emit_verify_tag("PHASE1", student_id, results_stride[1], results_stride[16])
    print(tag)
    shm.close()
    shm.unlink()