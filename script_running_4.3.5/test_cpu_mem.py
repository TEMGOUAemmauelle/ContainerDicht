import os
import random
import time
import threading
import multiprocessing as mp
import psutil
import sys


class container():

    

    def __init__(self, x):
        os.system(f'fallocate -l 4KB {str(x)}')
        #with open(self, "w+b") as f:
        #    fallocate(f, 0, 1024)


    def write_f(self, x, step=0):
        step = step
        try:
            with open(f'{x}', "wb") as f_out:
                print(f'ecriture dans le fichier {x}')
                if (step == 0):
                    x = random.sample(range(1000),1)
                    for xx in x:
                        f_out.write(xx.to_bytes(xx.bit_length() , byteorder='big'))

                    #f_out.write(bytes(f'ecriture dans le fichier {x}', encoding = "utf-8"))
                    

                else:
                    f_out.write(step.to_bytes(step.bit_length() , byteorder='big'))
        except IOError:
            print(f'Ecriture en attente sur le fichier {x}')
            time.sleep(1)
            write_f(self, x, step)

    def read_f(self, x):
        try:
            with open(f'{x}', "rb") as f_out:
                print(f'lecture dans le fichier {x}')
                just = int.from_bytes(f_out.read(), byteorder='big')
                print(just)
                return just
                #f_out.read()
        except IOError:
            print(f'Lecture en attente sur le fichier {x}')
            time.sleep(1)
            read_f(self, x)


def child_write_f(self, x, l, step=0):
    l.acquire()
    proc = psutil.Process()  # get self pid
    #proc.cpu_affinity(affinity)
    #aff = proc.cpu_affinity()
    try:
        with open(f'{x}', "wb") as f_out:
            print(f'ecriture dans le fichier {x}')
            if (step == 0):
                x = random.sample(range(1000),1)
                for xx in x:
                    f_out.write(xx.to_bytes(xx.bit_length() , byteorder='big'))

                #f_out.write(bytes(f'ecriture dans le fichier {x}', encoding = "utf-8"))
                #full and 1500MB = 384000
                #mip_5 = get_mips(384000, "full", tab)+
            else:
                f_out.write(step.to_bytes(step.bit_length() , byteorder='big'))
    except IOError:
        print(f'Processus : Eccriture en attente sur le fichier {x}')
        time.sleep(1)
        child_write_f(self, x, step)

    finally:
        l.release()

def child_read_f(self, x):
    proc = psutil.Process()  # get self pid
    #proc.cpu_affinity(affinity)
    #aff = proc.cpu_affinity()
    try:
        with open(f'{x}', "rb") as f_out:
            print(f'lecture dans le fichier {x}')
            just = int.from_bytes(f_out.read(), byteorder='big')
            print(just)
            return just
            #f_out.read()
    except IOError:
        print(f'Processus : Lecture en attente sur le fichier {x}')
        time.sleep(1)
        child_read_f(self, x)


def operations(tab, val, n=5):
    #st = time.time()
    for i in range(0,n):
        num = random.sample(range(int(val)),5)
        tab[num[0]].write_f(num[0])
        tab[num[1]].write_f(num[1])
        tab[num[2]].write_f(num[2])
        tab[num[3]].write_f(num[3])
        tab[num[4]].write_f(num[4], step=(tab[num[0]].read_f(num[0])) + (tab[num[1]].read_f(num[1])))
        tab[num[4]].read_f(num[4])

def operations_mutex(tab, val, n=20):
    lock = mp.Lock()
    #st_time=time.time()
    p_all = list()
    for i in range(0,n):
        num = random.sample(range(int(val)),5)
        for cp in range(0, 4):
            try:
                p = mp.Process(target=child_write_f, args=(tab[num[cp]], num[cp], lock))
                p.start()
                p_all.append(p)
                
            except ValueError as e:
                print(f'Processus : écriture en attente sur le fichier {num[i]}')
                #operations_mutex(tab, num)
                #continue
            
        p_n = mp.Process(target=child_write_f, args=(tab[num[4]], num[4], lock, (child_read_f(tab[num[1]], num[1]))))
        p_n.start()
        p_all.append(p_n)

        for p in p_all:
            p.join()


tab = []
def make_memory(lenn):
    for i in range (0, int(lenn)):  # here ispecify a memory 128Mb of size
        #time.sleep(1)
        tab.append(container(i))


def drop_memory(lenn):
    for i in range (0, int(lenn)):
        if os.path.exists(str(i)):
            os.remove(str(i))  


def get_mips(mem_usage, cpu_mode, tab):
    if cpu_mode=="full":
        st_time = time.time()
        th_1 = threading.Thread(target=make_memory(lenn=mem_usage))
        th_2 = threading.Thread(target=operations(tab=tab, val=mem_usage, n=1000))
        th_1.start()
        th_2.start()
        th_1.join()
        th_2.join()
        drop_memory(mem_usage)
        return (time.time() - st_time)
    else:
        st_time = time.time()
        th_1 = threading.Thread(target=make_memory(lenn=mem_usage))
        th_2 = threading.Thread(target=operations_mutex(tab=tab, val=mem_usage, n=1000))
        th_1.start()
        th_2.start()
        th_1.join()
        th_2.join()
        drop_memory(mem_usage)
        return (time.time() - st_time)


mip0 = get_mips(sys.argv[1], "full", tab)
mip1 = get_mips(sys.argv[2], "full", tab)
mip2 = get_mips(sys.argv[3], "full", tab)
mip3 = get_mips(sys.argv[4], "full", tab)
mip4 = get_mips(sys.argv[5], "full", tab)
mip5 = get_mips(sys.argv[6], "full", tab)
mip6 = get_mips(sys.argv[7], "full", tab)
mip7 = get_mips(sys.argv[8], "full", tab)
mip8 = get_mips(sys.argv[9], "full", tab)
mip9 = get_mips(sys.argv[10], "full", tab)
print(mip0)
print(mip1)
print(mip2)
print(mip3)
print(mip4)
print(mip5)
print(mip6)
print(mip7)
print(mip8)
print(mip9)
