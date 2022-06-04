
#* Job Class
class Job:
    def __init__(self, stream_no, time, size) -> None:
        self.__index = stream_no    # index no. of the job. pos. of entry
        self.__btime = time         # burst time of the job 
        self.__size = size          # size of the job

        self.__status = "waiting"   # job status - can be "waiting", "allocated", or "done"
        self.__wtime = time         # waiting time of job. shall be decremented

    # get status of this job
    def get_status(self) -> str:
        return self.__status

    # get waiting time of this job
    def get_wtime(self) -> int:
        return self.__wtime

    # increment waiting time by 1
    def elapse(self) -> None:
        self.__wtime -= 1

    def __repr__(self) -> str:
        return f'Job{str(self.__index).zfill(2)}: <{self.__btime},{self.__size}>'

#* Memory Block Class
class MemBlock:
    def __init__(self, mem_blk, size) -> None:
        self.__index = mem_blk      # index no. of the memory block
        self.__size = size          # size of the block

        self.__status = "free"      # block status - can be "free" or "occupied"
        self.__allocjob = None      # holds the job currently allocated to the block
    
    # gets size of a block
    def get_size(self) -> int:
        return self.__size

    # gets current status of a block
    def get_status(self) -> str:
        return self.__status

    # allocate a job in this block
    def allocate(self, job) -> None:
        self.__allocjob = job
        self.__status = "occupied"

    # deallocate the job contained in this block
    def deallocate(self) -> None:
        self.__allocjob = None
        self.__status = "free"

    def __repr__(self) -> str:
        return f'Memory{str(self.__index).zfill(2)}: <{self.__size}>'

#* Job List
class JobList:
    def __init__(self) -> None:
        self.__rawlist:list[Job] = []

    # appends jobs to job list
    def add(self, job) -> None:
        self.__rawlist.append(job)

    # allows the object to be indexed by []
    def __getitem__(self, key) -> Job:
        return self.__rawlist[key]

    def __repr__(self) -> str:
        return repr(self.__rawlist)

#* Memory List
class MemList:
    def __init__(self) -> None:
        self.__rawlist:list[MemBlock] = []

    # appends blocks to memory list
    def add(self, block) -> None:
        self.__rawlist.append(block)

    # sorts memory list depending on chosen algo
    def sort(self, algo) -> None:
        if algo == '1':
            self.__rawlist.sort(key = lambda blk: blk.get_size(), reverse=True)
        elif algo == '2':
            self.__rawlist.sort(key = lambda blk: blk.get_size())

    # allows the object to be indexed by []
    def __getitem__(self, key) -> MemBlock:
        return self.__rawlist[key]

    def __repr__(self) -> str:
        return str(self.__rawlist)

#* Main Program
def main():

    jobList = JobList()
    memoryList = MemList()

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
    
    # ! ask user with chosen algo w/ validation
    print('Choose Algorithm: [1] Worst-Fit [2] Best Fit [3] First-Fit')
    chosenAlgo = input()
    while chosenAlgo not in ['1','2','3']:
        print('Invalid choice of allocation algorithm. Try again.')
        chosenAlgo = input()

    # ! prepare job/memory list based on chosen algo
    memoryList.sort(chosenAlgo)

    # ! main program loop
    for memblock in memoryList:
        print(memblock)

main()