import matplotlib.pyplot as plt
from math import *
import random as rnd
import numpy as np


def poisson(lambd, frames, frame_size):
    messages = []
    temp = []
    mes_time = []
    l_bracket = 0
    r_bracket = frame_size
    for i in range(len(lambd)):
        messages.append(i)
        temp.append(i)
        temp[i] = np.random.poisson(lambd[i], frames)
        l_bracket = 0
        r_bracket = frame_size
        for j in range(frames):
            while temp[i][j] > 0:
                mes_time.append(rnd.uniform(l_bracket, r_bracket))
                temp[i][j] -= 1
            l_bracket += frame_size
            r_bracket += frame_size
        messages[i] = mes_time
        mes_time = []
        messages[i].sort()
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


def find_success(mas, l_bracket, r_bracket, item):
    for i in range(l_bracket, r_bracket, 1):
        if len(mas[i]) == 0:
            continue
        for j in mas[i]:
            if j == item and len(mas[i]) == 1:
                return True
    return False


def min_len_slot(mas, start, stop):
    for i in range(start, stop, 1):
        if len(mas[i]) == 1:
            return True
    return False


def proc_conflict(mas, start, stop, slot, total_msg):
    out_msg = 0
    copy_mas = []
    for t in range(len(mas[slot])):
        copy_mas.append(mas[slot][t])
    for j in range(len(copy_mas)):
        if find_success(mas, start, stop, copy_mas[j]): #
            out_msg += 1
            total_msg.pop(copy_mas[j])             # Удаляем из всего потока сообщений абонента, удаленного из конфликта
            delete_same_mes(mas, copy_mas[j])
    if len(copy_mas) - out_msg == 1:
        for j in range(len(copy_mas)):
            if find_success(mas, start, stop, copy_mas[j]):
                out_msg += 1
                total_msg.pop(copy_mas[j])
                delete_same_mes(mas, copy_mas[j])
    return out_msg


def queue_format(mas, border):
    for i in range(border):
        mas[i].clear()


def asynchV2V(mas_msg, num_of_frames, num_of_slots, polynomial):
    throughput = []
    packet_loss = []
    total_msg = []
    delay = []
    for i in range(len(mas_msg)):  # Проход по лямбдам
        queue = [[] for slots in range(num_of_slots * num_of_frames)]
        throughput.append(0)
        packet_loss.append(0)
        total_msg.append(0)
        total_msg += mas_msg[i]
        total_msg.pop(0)
        delay.append(0)
        l_bracket = 0
        r_bracket = num_of_slots * 5
        sub = 0
        while r_bracket <= num_of_frames * num_of_slots and len(total_msg) > 0:            # Проход по всей симуляции
            queue_format(queue, l_bracket)                                   # Удаляем копии, не попадающие в суперфрейм
            while sub < len(total_msg) and l_bracket <= total_msg[sub] <= r_bracket - 1:                # Просмотр всех сообщений, попавших в суперфрейм
                    rand_num = rnd.random()
                    if polynomial == 1:
                        if rand_num <= 0.86:
                            copy = 3
                        else:
                            copy = 8
                    j = 0
                    while j < copy:
                        if j == 0:
                            queue[ceil(total_msg[sub])].append(sub)              # Первая копия всегда в первый слот
                            j += 1
                            continue
                        rand = rnd.randint(ceil(total_msg[sub]), ceil(total_msg[sub]) + num_of_slots - 1)    # выбор своего слота
                        if rand >= num_of_slots * num_of_frames:
                            j += 1
                            continue
                        if not (contains(queue[rand], sub)):
                            queue[rand].append(sub)
                            j += 1
                    sub += 1
            while min_len_slot(queue, l_bracket, r_bracket):              # Проверяем текущую очередь на наличие 1 сообщения в слоте для погашения
                msg_left = len(total_msg)
                for cur_slot in range(l_bracket, r_bracket, 1):             # Проход по всем слотам текущего суперфрейма
                    if msg_left == 0:
                        break
                    queue1 = len(queue[cur_slot])
                    queue2 = cur_slot
                    if len(queue[cur_slot]) == 1:
                        ind = queue[cur_slot][0]
                        total_msg.pop(ind)                         # удаляем сообщение из всей симуляции
                        delete_same_mes(queue, ind)                               # удаляем сообщение из очереди
                        msg_left -= 1
                    elif len(queue[cur_slot]) > 1:
                        msg_left -= proc_conflict(queue, l_bracket, r_bracket, cur_slot, total_msg)
            l_bracket += 1
            r_bracket += 1
        packet_loss[i] = len(total_msg) / len(mas_msg[i])
        throughput[i] = (len(mas_msg[i]) - len(total_msg)) / num_of_slots
    return throughput, packet_loss


if __name__ == "__main__":
    simulation_time = 1720
    slots = 172
    frames = simulation_time // slots
    nfig = 1
    lambd = []
    for i in range(1, 11):
        lambd.append(i * slots / 10)

    messages = poisson(lambd, frames, slots)
    res = asynchV2V(messages, frames, slots, 1)

    for i in range(len(lambd)):
        lambd[i] /= slots

    nfig += 1
    plt.figure(nfig)
    plt.plot(lambd, res[1])
    plt.yscale('log')
    plt.grid(True)
    plt.show()