import collections
import subprocess

MEMORY_LIMIT_PERCENT = 80

command = subprocess.Popen(['nvidia-smi', '--query-gpu=memory.total', '--format=csv,noheader,nounits'],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
total_list = command[0].split('\n')

command = subprocess.Popen(['nvidia-smi', '--query-gpu=memory.used', '--format=csv,noheader,nounits'],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
used_list = command[0].split('\n')

command = subprocess.Popen(['nvidia-smi', '--query-gpu=pci.bus_id', '--format=csv,noheader,nounits'],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
line = command[0].split('\n')
gpu_dict = collections.OrderedDict()
i = 0

for key in line:
    if key[:1].isdigit():
        gpu_dict[key] = round(float(used_list[i]) / float(total_list[i]) * 100, 2)
        i += 1
gpu_best = min(gpu_dict, key=gpu_dict.get)

i = 0
print("Index\tGPU Bus-Id\t\tMemory-Usage\tStatus\n------------------------------------------------------")
for key, value in gpu_dict.iteritems():
    if value < MEMORY_LIMIT_PERCENT:
        if key == gpu_best:
            status = "Ready*"
        else:
            status = "Ready"
    else:
        status = "Busy"

    print("{0}\t{1}\t{2}%\t\t{3}".format(i, key, value, status))
    i += 1
print("* Candidate GPU is {0}".format(gpu_best))
