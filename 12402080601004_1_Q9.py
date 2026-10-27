import heapq
import threading


class Worker(threading.Thread):
    def __init__(self, worker_id, job, result, lock):
        super().__init__()
        self.worker_id = worker_id
        self.job = job
        self.result = result
        self.lock = lock

    def run(self):
        arrival, order, job_id, priority, duration, resources = self.job

        start = self.job_start
        finish = start + duration

        with self.lock:
            self.result.append(
                (
                    start,
                    job_id,
                    self.worker_id,
                    finish
                )
            )


def choose_jobs(jobs, workers):
    jobs.sort(key=lambda job: (job[0], job[1]))

    waiting = []
    worker_heap = [(0, i + 1) for i in range(workers)]
    heapq.heapify(worker_heap)

    index = 0
    current_time = 0
    assignments = []

    while index < len(jobs) or waiting:
        if not waiting and index < len(jobs):
            current_time = max(
                current_time,
                jobs[index][0]
            )

        while index < len(jobs) and jobs[index][0] <= current_time:
            heapq.heappush(
                waiting,
                (
                    -jobs[index][3],
                    jobs[index][0],
                    jobs[index][1],
                    jobs[index]
                )
            )
            index += 1

        free_time, worker_id = heapq.heappop(worker_heap)
        current_time = max(current_time, free_time)

        while index < len(jobs) and jobs[index][0] <= current_time:
            heapq.heappush(
                waiting,
                (
                    -jobs[index][3],
                    jobs[index][0],
                    jobs[index][1],
                    jobs[index]
                )
            )
            index += 1

        if not waiting:
            heapq.heappush(
                worker_heap,
                (free_time, worker_id)
            )
            continue

        _, _, _, job = heapq.heappop(waiting)

        start = max(current_time, job[0])
        finish = start + job[4]

        assignments.append(
            (start, finish, worker_id, job)
        )

        heapq.heappush(
            worker_heap,
            (finish, worker_id)
        )

        current_time = start

    return assignments


print("Threaded Job Scheduler Simulation")
print("Enter number of workers and jobs:")
w, n = map(int, input().split())

jobs = []

print("Enter job details:")
print("Format: arrival_time job_id priority duration resources")

for i in range(n):
    print(f"Job {i + 1}:")
    arrival, job_id, priority, duration, resources = input().split()

    arrival = int(arrival)
    priority = int(priority)
    duration = int(duration)
    resources = int(resources)

    jobs.append(
        (
            arrival,
            i,
            job_id,
            priority,
            duration,
            resources
        )
    )

assignments = choose_jobs(jobs, w)

result = []
lock = threading.Lock()
threads = []
# Create one thread for each scheduled job
for start, finish, worker_id, job in assignments:
    worker = Worker(
        worker_id,
        job,
        result,
        lock
    )

    worker.job_start = start
    threads.append(worker)
    worker.start()

for worker in threads:
    worker.join()

result.sort()

total_wait = 0

for start, job_id, worker_id, finish in result:
    for assignment in assignments:
        if (
            assignment[0] == start
            and assignment[2] == worker_id
            and assignment[3][2] == job_id
        ):
            total_wait += start - assignment[3][0]
            break

    print(
        job_id,
        f"W{worker_id}",
        start,
        finish
    )

print(f"AVG_WAIT {total_wait / n:.2f}")
