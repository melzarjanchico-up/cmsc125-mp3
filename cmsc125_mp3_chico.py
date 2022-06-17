"""
    FILE:       cmsc125_mp3_chico.py
    ABOUT:      Implement the worst-fit, best-fit, and first-fit allocation processes
    
    NAME:       Melzar Jan E. Chico & Vergel Jabello
    COURSE:     CMSC125 B
    DATE:       2022 April 10

    TASK:       Machine Problem 3
    NOTES:      Job & Block values are supplied via the text files inside './data'.
    ADL NOTES:  The Q&A portion of this machine problem is written below the code or in the README.md file. Thank you.  
"""

#* Job Class
class Job:
    def __init__(self, stream_no, time, size) -> None:
        self.__index = stream_no    # index no. of the job. pos. of entry
        self.__btime = time         # burst time of the job 
        self.__size = size          # size of the job

        self.__status = "waiting"   # job status - can be "waiting", "allocated", or "done"
        self.__assignable = True    # bool whether the job is assignable
        self.__rtime = time         # remaining time of job (based burst time). decremented
        self.__wtime = 0            # time taken by job to be allocated. incremented

    # get index of this job
    def get_index(self) -> int:
        return self.__index

    # get burst time of this job
    def get_btime(self) -> int:
        return self.__btime

    # get burst time of this job
    def get_size(self) -> int:
        return self.__size

    # get status of this job
    def get_status(self) -> str:
        return self.__status

    # get status of this job
    def get_assignable(self) -> bool:
        return self.__assignable

    # get remaining time of this job
    def get_rtime(self) -> int:
        return self.__rtime

    # get waiting time of this job
    def get_wtime(self) -> int:
        return self.__wtime

    # set status of this job
    def set_status(self, status:str) -> None:
        self.__status = status

    # set assignable of this job
    def set_assignable(self, is_assignable:bool) -> None:
        self.__assignable = is_assignable

    # increment waiting time by 1
    def wait(self) -> None:
        if self.__status == "waiting":
            self.__wtime += 1

    # decrement remaining time by 1
    def elapse(self) -> None:
        self.__rtime -= 1

    # for debugging
    def __repr__(self) -> str:
        return f'Job{self.__index}: <[{self.__wtime}], {self.__rtime}, {self.__status}, {self.__btime}, {self.__size}>\n'

#* Memory Block Class
class MemBlock:
    def __init__(self, mem_blk, size) -> None:
        self.__index = mem_blk          # index no. of the memory block
        self.__size = size              # size of the block

        self.__status = "free"          # block status - can be "free" or "occupied"
        self.__allocjob = None          # holds the job currently allocated to the block
        self.__unUsedSpace = size       # holds the heavily-used space of the block
        self.__mostUsedSpace = size     # holds the non-used space of the block   
        self.__allocatedJobs = 0        # holds total no. of jobs allocated by this block
        self.__totalIF = 0              # holds the total internal frag. of this block

    # get index of a block
    def get_index(self) -> int:
        return self.__index

    # get size of a block
    def get_size(self) -> int:
        return self.__size

    # get current status of a block
    def get_status(self) -> str:
        return self.__status

    # get current status of a block
    def get_allocjob(self) -> Job:
        return self.__allocjob

    # get unused space
    def get_unUnUsedSpace(self) -> int:
        return self.__unUsedSpace

    # get most used space
    def get_mostUsedSpace(self) -> int:
        return self.__mostUsedSpace

    # get allocated jobs
    def get_allocatedJobs(self) -> int:
        return self.__allocatedJobs

    # get total internal frag
    def get_totalIF(self) -> int:
        return self.__totalIF

    # allocate a job in this block
    def allocate(self, job:Job) -> None:
        self.__allocjob = job
        self.__allocjob.set_status('allocated')
        self.__status = "occupied"
        self.__allocatedJobs += 1

        self.__totalIF += (self.__size - job.get_size())
        # checks for the non used memory
        if (self.__size - job.get_size()) <= self.__unUsedSpace:
            self.__unUsedSpace = (self.__size - job.get_size())
        # checks for the most used memory
        if job.get_size() <= self.__mostUsedSpace:
            self.__mostUsedSpace = job.get_size()

    # deallocate the job contained in this block
    def deallocate(self) -> None:
        self.__allocjob.set_status('done')
        self.__allocjob = None
        self.__status = "free"

    # for debugging
    def __repr__(self) -> str:
        return f'Memory{self.__index}: <{self.__allocjob}, {self.__status}, {self.__size}>\n'

#* Job List
class JobList:
    def __init__(self) -> None:
        self.__rawlist:list[Job] = []
        self.__countWaitingJobs = 0

    # get count waiting jobs
    def get_cwj(self) -> None:
        return self.__countWaitingJobs

    # get total waiting times of done jobs
    def get_jobWaits(self) -> None:
        total = 0
        for job in self.__rawlist:
            if job.get_assignable() and job.get_status() == 'done':
                total += job.get_wtime()
        return total

    # appends jobs to job list
    def add(self, job:Job) -> None:
        self.__rawlist.append(job)

    # prepare job list for any stuff in jobs
    def prep(self, max_block:int) -> None:
        # checks whether a job has size bigger than the max block
        for job in self.__rawlist:
            if job.get_size() > max_block:
                job.set_assignable(False)

    # increase waiting time for all waiting jobs + count waiting processes
    def inc_jobWaits(self) -> None:
        for job in self.__rawlist:
            if job.get_assignable() and job.get_status() == "waiting":
                self.__countWaitingJobs += 1
                job.wait()

    # check if all jobs are finished
    def are_finished(self) -> bool:
        for job in self.__rawlist:
            if not job.get_assignable():
                continue
            if job.get_status() != 'done':
                return False
        return True

    # allows the object to be indexed
    def __getitem__(self, key:str) -> Job:
        return self.__rawlist[key]

    # for debugging
    def __repr__(self) -> str:
        return repr(self.__rawlist)

#* Memory List
class MemList:
    def __init__(self) -> None:
        self.__rawlist:list[MemBlock] = []
        self.__countProcessedJobs:int = 0
        self.__countCompletedJobs:int = 0

    # get count processed jobs
    def get_cpj(self) -> int:
        return self.__countProcessedJobs

    # get count completed jobs
    def get_ccj(self) -> int:
        return self.__countCompletedJobs

    # get total heavily used space
    def get_heavy_us(self) -> int:
        total = 0
        for block in self.__rawlist:
            if block.get_allocatedJobs() > 0:
                total += block.get_mostUsedSpace()
        return total

    # get total non used space
    def get_non_us(self) -> int:
        total = 0
        for block in self.__rawlist:
            if block.get_allocatedJobs() > 0:
                total += block.get_unUnUsedSpace()
        return total

    # appends blocks to memory list
    def add(self, block:MemBlock) -> None:
        self.__rawlist.append(block)

    # prepare memory list for algo (e.g. sorting, etc.)
    def prep(self, algo:str) -> None:
        # sorts the memlist depending on algo chosen
        if algo == '1':
            self.__rawlist.sort(key = lambda blk: blk.get_size(), reverse=True)
        elif algo == '2':
            self.__rawlist.sort(key = lambda blk: blk.get_size())

    # assign jobs to blocks
    def assign(self, joblist:JobList) -> None:
        for job in joblist:
            # check if job is assigable
            if (not job.get_assignable()):
                continue
            # check if job is waiting
            if (job.get_status() == 'allocated') or (job.get_status() == 'done'):
                continue
            # find a block that can accomodate
            for block in self.__rawlist:
                # check if block is not occupied
                if block.get_status() == 'occupied':
                    continue
                # check if block can accomodate the job
                if job.get_size() <= block.get_size():
                    block.allocate(job)
                    break

    # execute all jobs allocated in the blocks
    def execute(self) -> None:
        for block in self.__rawlist:
            if block.get_status() != 'occupied':
                continue

            block.get_allocjob().elapse()
            self.__countProcessedJobs += 1

            if block.get_allocjob().get_rtime() <= 0:
                self.__countCompletedJobs += 1
                block.deallocate()

    # print the jobs and time from the memory
    def display_memlist(self) -> None:
        for block in self.__rawlist:
            if block.get_status() == 'occupied':
                x = str(block.get_allocjob().get_index()).zfill(2)
                y = str(block.get_index()).zfill(2)
                z = str(block.get_allocjob().get_rtime()).zfill(2)
                print(f'Job {x} has been allocated in memory block {y} and will reside for {z} ms')

    # display internal fragmentation
    def display_if(self, time) -> None:
        for block in self.__rawlist:
            x = str(block.get_index()).zfill(2)
            if block.get_totalIF() > 0:
                print(f'Block {x}\'s total internal fragmentation: {(block.get_totalIF())} units of memory')
                print(f'Block {x}\'s average internal fragmentation: {round(block.get_totalIF()/time, 2)} units of memory')
            else:
                print(f'Block {x} was not allocated to any job.')
            print()

    # allows the object to be indexed
    def __getitem__(self, key:int) -> MemBlock:
        return self.__rawlist[key]

    # for debugging
    def __repr__(self) -> str:
        return str(self.__rawlist)

#* Main Program
def main():

    jobList = JobList()
    memoryList = MemList()
    max_block = 0

    # ! get all jobs
    with open('./data/joblist.txt') as f:
        # read the header line first
        f.readline()
        # read each line
        for line in f.readlines():
            j = line.split()
            jobList.add(Job(int(j[0]), int(j[1]), int(j[2])))

    # ! get all memory blocks
    with open('./data/memorylist.txt') as f:
        # read the header line first
        f.readline()
        # read each line
        for line in f.readlines():
            m = line.split()
            memoryList.add(MemBlock(int(m[0]), int(m[1])))
            if int(m[1]) > max_block:
                max_block = int(m[1])

    # ! ask user with chosen algo w/ validation
    print('Choose Algorithm: [1] Worst-Fit [2] Best Fit [3] First-Fit')
    chosenAlgo = input()
    while chosenAlgo not in ['1','2','3']:
        print('Invalid choice of allocation algorithm. Try again.')
        chosenAlgo = input()

    # ! prepare job list and memory list before the allocation process
    memoryList.prep(chosenAlgo)
    jobList.prep(max_block)     

    # ! main allocation loop
    time = 1
    while not jobList.are_finished():
        # allocate jobs
        memoryList.assign(jobList)
        # print the current memory list
        print('-'*27 + f' AT TIME t = {str(time).zfill(2)} ' + '-'*27)
        memoryList.display_memlist()
        # increase wait times for waiting jobs
        jobList.inc_jobWaits()
        # execute the jobs inside memory list
        memoryList.execute()

        time += 1
        print()

    # ! evaluation
    str_algo = ['WORST-FIT', 'BEST-FIT', 'FIRST-FIT']
    print('='*30 + f' {str_algo[int(chosenAlgo)-1]} ' + '='*30)
    print()
    print(f'AVERAGE THROUGHPUT: {round(memoryList.get_cpj()/(time-1), 2)} jobs per unit time')
    print(f'AVERAGE WAITING QUEUE LENGTH: {round(jobList.get_cwj()/(time-1), 2)} jobs per unit time')
    print(f'AVERAGE WAITING TIME: {round(jobList.get_jobWaits()/memoryList.get_ccj(), 2)} time units')
    print()
    print(f'TOTAL UNUSED PARTITION: {round((memoryList.get_non_us()/50000)*100, 2)}% out of 50 000 memory capacity')
    print(f'TOTAL HEAVILY USED PARTITION: {round((memoryList.get_heavy_us()/50000)*100, 2)}% out of 50 000 memory capacity')
    print()
    print('-'*30 + ' INTERNAL FRAGMENTATION ' + '-'*30)
    print('Note: I.F. refers to free spaces in each allocation, where current job\'s size < block\'s size.')
    print()
    memoryList.display_if(time-1)

main()

"""
1.) Explain what the results indicate about the performance of the system for this job mix and memory organization. 

- The result indicates that performance system for this job mix does not necessarily matter since all allocation algorithms fall in same ranges of time taken (around 20-30s mark). Although, queue length and times were different. The best-fit had the lowest queue length and average queue time, and worst-fit had the opposite.
- What matters though was how the algorithms handled the memory. In this system, the worst fit has the lowest unused partition percentage (means most of the partition was atleast used during the liftime). In the highest exhausted partition, best fit came on top (this means, more than half of the systems memory did substantial job in keeping it utilized)

2.) Is one method of partitioning better than the other? Why or why not?

- Nope. There is a reason why our lectures never reasoned for the "best" allocation algorithm. All of the allocation algorithms have their best times and their worst times, depending on job placements, partition conditions, and just the overall specifications of the system. If there was an allocation system that was more "better" than three, there would have been no need to discuss it in the lessons, no? As such, no method of partitioning is better than the other.

3.) Could you recommend one method over the other based on your sample run? Would this hold in all cases? Write some conclusions and recommendations.

- In terms of overall systems, based on my last answers, I really could not conclude the best one. But when recommending one method over this system, I would probably recommend the best-fit allocation method, it has a middle ground throughput; it has the best average queue length and waiting time; it middles on unused partition and is the best utilizing almost half of its memory. The internal fragmentation is fine as well with no blocks that was not allocated. Yes, the other allocation algorithms had ups, but the best-fit system did not have the downs (only middles). Remember, I am only assuming for this system.
"""