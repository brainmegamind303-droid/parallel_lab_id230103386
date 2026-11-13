import ctypes
import multiprocessing as mp
from multiprocessing import shared_memory
from harness import run_benchmark, emit_verify_tag

def fs_worker(shm_name: str, slot_idx: int, iters: int) -> None:
    shm = shared_memory.SharedMemory(name=shm_name)
    arr = (ctypes.c_uint64 * 512).from_buffer(shm.buf)
    acc = arr[slot_idx]
    mask = 0xFFFFFFFFFFFFFFFF
    mult = 6364136223846793005
    for i in range(iters):
        acc = (acc * mult + (i ^ 1)) & mask
    arr[slot_idx] = acc
    del arr
    shm.close()

def run_experiment(p: int, stride: int, total_iters: int = 24_000_000):
    shm = shared_memory.SharedMemory(create=True, size=4096)
    iters_per_worker = total_iters // p
    
    def target():
        procs = []
        for t in range(p):
        # Вычисляем индекс с учетом шага (stride)
            slot_idx = t * stride
            proc = mp.Process(target=fs_worker, args=(shm.name, slot_idx, iters_per_worker))
            procs.append(proc)
            proc.start()
        for proc in procs:
            proc.join()

    stats = run_benchmark(target, warmup_runs=2, timed_runs=7)
    shm.close()
    shm.unlink()
    return stats.median_ms

if __name__ == "__main__":
    student_seed = 230103386
    p_phys = mp.cpu_count() // 2 if mp.cpu_count() > 1 else 1 # Оценочно физические ядра
    
    print("--- 1. Stride Sweep at p = P_phys ---")
    strides = [1, 2, 4, 8, 16, 32]
    stride_results = {}
    for s in strides:
        med_ms = run_experiment(p=max(1, p_phys), stride=s)
        stride_results[s] = med_ms
        print(f"Stride {s:2d}: Median Time = {med_ms:.2f} ms")
        
    # Базовые значения для верификации (например, stride=1 и stride=16)
    med_s1 = stride_results[1]
    med_s16 = stride_results.get(16, stride_results[max(stride_results.keys())])
    
    tag = emit_verify_tag("PHASE1", student_seed, med_s1, med_s16)
    print(tag)

if __name__ == "__main__":
    # ... ваш код расчетов ...
    tag = emit_verify_tag("PHASE1", student_seed, med_s1, med_s16)
    print(tag)  # <--- Обязательно должен быть print(), чтобы увидеть результат в консоли!