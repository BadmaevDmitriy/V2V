import matplotlib.pyplot as plt
from math import *
from decimal import Decimal
import random as rnd
import numpy as np


def poisson(lambd, frames):
    messages = []
    for i in range(len(lambd)):
        messages.append(i)
        messages[i] = np.random.poisson(lambd[i], frames)
    for i in range(len(lambd)):
        for j in range(len(messages[i])):
            messages[i][j] = floor(lambd[i])
    return messages


def contains(mas, item):
    if len(mas) == 0:
        return False
    for i in mas:
        if i == item:
            return True
    return False


def delete_same_mes(mas, item):
    for i in range(len(mas)):
        if len(mas[i]) != 0:
            for j in range(len(mas[i])):
                if mas[i][j] == item:
                    mas[i].remove(item)
                    break


def find_success(mas, item):
    for i in range(len(mas)):
        if len(mas[i]) == 0:
            continue
        for j in mas[i]:
            if j == item and len(mas[i]) == 1:
                return True
    return False


def min_len_slot(mas):
    for i in range(len(mas)):
        if len(mas[i]) == 1:
            return True
    return False


def proc_conflict(mas, i):
    out_msg = 0
    copy_mas = []
    for t in range(len(mas[i])):
        copy_mas.append(mas[i][t])
    for j in range(len(copy_mas)):
        if find_success(mas, copy_mas[j]):
            out_msg += 1
            delete_same_mes(mas, copy_mas[j])
    if len(copy_mas) - out_msg == 1:
        for j in range(len(copy_mas)):
            if find_success(mas, copy_mas[j]):
                out_msg += 1
                delete_same_mes(mas, copy_mas[j])
    return out_msg


def processing2(subscribers, slots, polynomial):
    queue = [[] for i in range(slots)]
    msg_left = subscribers
    copy = 2
    if polynomial == 2:
        copy = 1
    for k in range(subscribers):
        rand_num = rnd.random()
        if polynomial == 1:
            if rand_num <= 0.86:
                copy = 3
            else:
                copy = 8
        j = 0
        while j < copy:
            rand = rnd.randint(0, slots - 1)
            if not(contains(queue[rand], k)) and not(contains(queue[rand], 1)):
                queue[rand].append(k)
                j += 1

    while min_len_slot(queue):
        for i in range(slots):
            if msg_left == 0:
                break
            if len(queue[i]) != 0:
                if len(queue[i]) == 1:
                    delete_same_mes(queue, queue[i][0])
                    msg_left -= 1
                else:
                    msg_left -= proc_conflict(queue, i)
    return msg_left


def slotted_aloha2(mas_msg, num_of_frames, num_of_slots, polynomial):
    lambd_out = []
    packet_loss = []
    total_msg = []
    queue = 0
    for i in range(len(mas_msg)):
        lambd_out.append(0)
        packet_loss.append(0)
        total_msg.append(0)
        for j in range(num_of_frames):
            total_msg[i] += mas_msg[i][j]
            if queue > 0:
                packet_loss[i] += processing2(queue, num_of_slots, polynomial)
            if mas_msg[i][j] > 0:
                queue = mas_msg[i][j]
        lambd_out[i] = (total_msg[i] - packet_loss[i]) / frames
        packet_loss[i] /= total_msg[i]
        # packet_loss[i] *= 100
    return lambd_out, packet_loss


if __name__ == "__main__":
    simulation_time = 172
    slots = 172
    frames = simulation_time // slots
    nfig = 1
    lambd = []
    for i in range(1, 11):
        lambd.append(i * slots / 10)

    messages = poisson(lambd, frames)
    res = slotted_aloha2(messages, frames, slots, 1)

    for i in range(len(lambd)):
        lambd[i] /= slots

    nfig += 1
    plt.figure(nfig)
    plt.plot(lambd, res[1])
    plt.yscale('log')
    plt.grid(True)
    plt.show()