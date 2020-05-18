import matplotlib.pyplot as plt
from math import *
import random as rnd
import numpy as np


def poisson(lambd, frames, bs):
    messages = []
    for i in range(len(lambd)):
        messages.append(i)
        messages[i] = np.random.poisson(lambd[i], frames)
    if bs:
        for lam in range(len(lambd)):
            for l in range(frames):
                rand = rnd.random()
                if rand <= lambd[lam]:
                    messages[lam][l] = 1
                else:
                    messages[lam][l] = 0
        return messages
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


def proc_conflict(mas, i, delay, lamb, cur_frame, slots):
    out_msg = 0
    copy_mas = []
    for t in range(len(mas[i])):
        copy_mas.append(mas[i][t])
    for j in range(len(copy_mas)):
        if find_success(mas, copy_mas[j]):
            out_msg += 1
            delay[lamb] += (cur_frame + 1) * slots - rnd.randint((cur_frame - 1) * slots, cur_frame * slots - 1)
            delete_same_mes(mas, copy_mas[j])
    if len(copy_mas) - out_msg == 1:
        for j in range(len(copy_mas)):
            if find_success(mas, copy_mas[j]):
                out_msg += 1
                delay[lamb] += (cur_frame + 1) * slots - rnd.randint((cur_frame - 1) * slots, cur_frame * slots - 1)
                delete_same_mes(mas, copy_mas[j])
    return out_msg


def processing2(subscribers, delay, lamb, slots, cur_frame, polynomial, flag):
    queue = [[] for i in range(slots)]
    msg_left = subscribers
    copy = 2
    if flag:
        rand_num = rnd.random()
        if polynomial == 1:
            if rand_num <= 0.86:
                copy = 3
            else:
                copy = 8
        j = 0
        while j < copy:
            rand = rnd.randint(0, slots - 1)
            if not (contains(queue[rand], -1)):
                queue[rand].append(-1)
                j += 1
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
            if contains(queue[rand], -1):
                j += 1
                continue
            if not(contains(queue[rand], k)):
                queue[rand].append(k)
                j += 1
    while min_len_slot(queue):
        for i in range(slots):
            if msg_left + flag == 0:
                break
            if len(queue[i]) != 0:
                if len(queue[i]) == 1:
                    if queue[i][0] == -1:
                        delay[lamb] += (cur_frame + 1) * slots - rnd.randint((cur_frame - 1) * slots,
                                                                           cur_frame * slots - 1)
                        delete_same_mes(queue, queue[i][0])
                        flag = 0
                    else:
                        delay[lamb] += (cur_frame + 1) * slots - rnd.randint((cur_frame - 1) * slots, cur_frame * slots - 1)
                        delete_same_mes(queue, queue[i][0])
                        msg_left -= 1
                else:
                    msg_left -= proc_conflict(queue, i, delay, lamb, cur_frame, slots)
    return msg_left


def syncV2V(mas_msg, mas_msg_bs, num_of_frames, num_of_slots, polynomial):
    lambd_out = []
    packet_loss = []
    total_msg = []
    total_msg_bs = []
    delay = []
    queue = 0
    for i in range(len(mas_msg)):
        delay.append(0)
        lambd_out.append(0)
        packet_loss.append(0)
        total_msg.append(0)
        total_msg_bs.append(0)
        flag_bs = 0
        for j in range(num_of_frames):
            total_msg[i] += mas_msg[i][j]
            total_msg_bs[i] += mas_msg_bs[i][j]
            if flag_bs:
                flag = 1
                packet_loss[i] += processing2(queue, delay, i, num_of_slots, j, polynomial, flag)
            elif queue > 0:
                flag = 0
                packet_loss[i] += processing2(queue, delay, i, num_of_slots, j, polynomial, flag)
            if mas_msg[i][j] > 0:
                queue = mas_msg[i][j]
            if mas_msg_bs[i][j] > 0:
                flag_bs = 1
            else:
                flag_bs = 0
        lambd_out[i] = (total_msg[i] + 1 - packet_loss[i]) / num_of_slots
        print("throughput[", i, "] = ", lambd_out[i])
        delay[i] /= total_msg[i] + total_msg_bs[i] - packet_loss[i]
        print("delay[", i, "] = ", delay[i])
        packet_loss[i] /= total_msg[i]
        print("PLR[", i, "] = ", packet_loss[i])
    return lambd_out, packet_loss, delay


if __name__ == "__main__":
    simulation_time = 1720
    slots = 172
    frames = simulation_time // slots
    nfig = 1
    lambd = []
    lambd_bs = []
    for i in range(1, 11):
        if ((i * slots / 10) - 1) > 1:
            lambd.append((i * slots / 10) - 1)
        else:
            lambd.append((i * slots / 10))
        lambd_bs.append(i / 10)     # Абонент с шансом i имеет или не имеет 1 сообщение во фрейме

    messages = poisson(lambd, frames, 0)
    messages_bs = poisson(lambd_bs, frames, 1)
    res = syncV2V(messages, messages_bs, frames, slots, 1)

    for i in range(len(lambd)):
        lambd[i] /= slots

    # nfig += 1
    # plt.figure(nfig)
    # plt.plot(lambd, res[1])
    # plt.yscale('log')
    # plt.grid(True)
    # plt.show()