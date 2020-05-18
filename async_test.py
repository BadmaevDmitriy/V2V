import matplotlib.pyplot as plt
from math import *
import random as rnd
import numpy as np


def poisson(lambd, frames, frame_size, bs):
    messages = []
    temp = []
    mes_time = []
    for i in range(len(lambd)):
        messages.append(i)
        temp.append(i)
        temp[i] = np.random.poisson(lambd[i], frames)
        if bs:
            for l in range(frames):
                rand = rnd.random()
                if rand < lambd[i]:
                    temp[i][l] = 1
                else:
                    temp[i][l] = 0
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


def proc_conflict(mas, start, stop, slot, total, messages_bs, analyzed):
    copy_mas = []
    for t in range(len(mas[slot])):
        copy_mas.append(mas[slot][t])

    j = 0
    delay = 0
    msg_left = 0
    while j < len(copy_mas):
        if msg_left == len(total):
            break
        if find_success(mas, start, stop, copy_mas[j]):
            delay += stop - getTime(total, copy_mas[j])
            analyzed.append(copy_mas[j])
            delete_same_mes(mas, copy_mas[j])
            msg_left += 1
            copy_mas.clear()
            j = 0
            for t in range(len(mas[slot])):
                copy_mas.append(mas[slot][t])
        else:
            j += 1
    return delay, msg_left

def queue_format(mas, border):
    for i in range(border):
        mas[i].clear()


def queue_search(buf, item):
    for i in range(len(buf)):
        if len(buf[i]) != 0:
            for j in range(len(buf[i])):
                if buf[i][j] == item:
                    return True
    return False


def queuecheck(buf, item):
    for i in range(len(buf)):
        if len(buf[i]) != 0:
            for j in range(len(buf[i])):
                if buf[i][j] == item:
                    return True
    return False


def getTime(buf, ind):
    for i in range(len(buf)):
        if len(buf[i]) > 0:
            if buf[i][1] == ind:
                return buf[i][0]


def checkforduplicate(buf, item):
    for i in range(len(buf)):
        if buf[i] == item:
            return True
    return False


def containsbs(buf):
    if len(buf) == 0:
        return False
    for i in range(len(buf)):
        if buf[i] < 0:
            return True
    return False

def asynchV2V(mas_msg, mas_msg_bs, num_of_frames, num_of_slots, polynomial):
    throughput = []
    packet_loss = []
    delay = []
    for i in range(len(mas_msg)):  # Проход по лямбдам
        print("Cur i:", i)
        queue = [[] for num_of_slots in range(num_of_slots * num_of_frames)]
        throughput.append(0)
        packet_loss.append(0)
        delay.append(0)
        total_msg_bs = [[] for curi in range(len(mas_msg_bs[i]))]  # массив, где каждый элемент это [время метки, уникальный номер метки]
        for k in range(len(total_msg_bs)):
            total_msg_bs[k].append(mas_msg_bs[i][k])
            total_msg_bs[k].append(0 - k - 1)
        total_msg = [[] for curi in range(len(mas_msg[i]))]  # массив, где каждый элемент это [время метки, уникальный номер метки]
        for k in range(len(total_msg)):
            total_msg[k].append(mas_msg[i][k])
            total_msg[k].append(k)
        l_bracket = 0
        r_bracket = num_of_slots * 5
        msg_out = 0
        analyzed_message = []
        analyzed_message_bs = []
        msgin = 0
        while r_bracket <= num_of_slots * num_of_frames and len(total_msg) + len(mas_msg_bs[i]) > 0:
            #print(msg_out, '/', len(total_msg) + len(total_msg_bs))
            queue_format(queue, l_bracket)     # Удаляем из очереди все копии в слотах, не попадающих в суперфрейм
            for k in range(len(total_msg_bs)):
                if l_bracket <= total_msg_bs[k][0] <= r_bracket - 1 and not queuecheck(queue, total_msg_bs[k][1]) and not checkforduplicate(
                        analyzed_message_bs, total_msg_bs[k][1]):  # 1.проверка на попадание в суперфрейу 2. есть ли это сообщение уже в очереди ? 3. анализировано это сообщение уже?
                    rand_num = rnd.random()
                    copy = 0
                    if polynomial:
                        if rand_num <= 0.86:
                            copy = 3
                        else:
                            copy = 8
                    j = 0
                    while j < copy:
                        if j == 0:
                            rand = ceil(total_msg_bs[k][0])
                            while containsbs(queue[rand]):
                                rand = rnd.randint(ceil(total_msg_bs[k][0]),
                                                   ceil(total_msg_bs[k][0]) + num_of_slots - 1)
                                if rand >= num_of_slots * num_of_frames:
                                    j += 1
                                    break
                            if j > 0:
                                continue
                            queue[rand].clear()
                            queue[rand].append(total_msg_bs[k][1])  # Первая копия всегда в первый слот
                            j += 1
                            #print(total_msg_bs[k][1], " : roll to ", rand, queue[rand])
                            continue
                        rand = rnd.randint(ceil(total_msg_bs[k][0]),
                                           ceil(total_msg_bs[k][0]) + num_of_slots - 1)  # выбор своего слота
                        if rand >= num_of_slots * num_of_frames:
                            j += 1
                            continue
                        if not contains(queue[rand], total_msg_bs[k][1]):
                            if not containsbs(queue[rand]):
                                queue[rand].clear()
                                queue[rand].append(total_msg_bs[k][1])
                                j += 1
                                #print(total_msg_bs[k][1], " : roll to ", rand, queue[rand])
                                continue
                elif total_msg_bs[k][0] > r_bracket:
                    break
            for k in range(len(total_msg)):
                if l_bracket <= total_msg[k][0] <= r_bracket - 1 and not queuecheck(queue, total_msg[k][1]) and not checkforduplicate(
                        analyzed_message, total_msg[k][1]):  # 1.проверка на попадание в суперфрейу 2. есть ли это сообщение уже в очереди ? 3. анализировано это сообщение уже?
                    msgin += 1
                    rand_num = rnd.random()
                    copy = 0
                    if polynomial:
                        if rand_num <= 0.86:
                            copy = 3
                        else:
                            copy = 8
                    j = 0
                    while j < copy:
                        if j == 0:
                            if not containsbs(queue[ceil(total_msg[k][0])]):
                                queue[ceil(total_msg[k][0])].append(total_msg[k][1])  # Первая копия всегда в первый слот
                            j += 1
                            continue
                        rand = rnd.randint(ceil(total_msg[k][0]),
                                           ceil(total_msg[k][0]) + num_of_slots - 1)  # выбор своего слота
                        if rand >= num_of_slots * num_of_frames:
                            j += 1
                            continue
                        if not contains(queue[rand], total_msg[k][1]):
                            if not containsbs(queue[rand]):
                                queue[rand].append(total_msg[k][1])
                            j += 1
                            continue
                elif total_msg[k][0] > r_bracket:
                    break
            #print(msgin - cur_msgin)
            if min_len_slot(queue, l_bracket, r_bracket):
                for cur_slot in range(l_bracket, r_bracket, 1):  # Проход по всем слотам текущего суперфрейма
                    if msg_out == len(total_msg) + len(total_msg_bs):
                        break
                    if len(queue[cur_slot]) == 1:
                        num = queue[cur_slot][0]  # получаем уникальный номер метки
                        delete_same_mes(queue, num)  # удаляем сообщение из очереди
                        msg_out += 1  # количество вышедших сообщений +1
                        if num < 0:
                            analyzed_message_bs.append(num)
                            delay[i] += r_bracket - getTime(total_msg_bs, num)
                        else:
                            analyzed_message.append(num)  # добавляем уникальный номер сообщения в массив с уже проанализированными сообзениями, чтобы повторно не брать его
                            delay[i] += r_bracket - getTime(total_msg, num)
                    elif len(queue[cur_slot]) > 1:
                        res = proc_conflict(queue, l_bracket, r_bracket, cur_slot, total_msg,
                                                  messages_bs, analyzed_message)
                        delay[i] += res[0]
                        msg_out += res[1]
                    #print(msg_out, '/', len(total_msg) + len(total_msg_bs))
            l_bracket += 1
            r_bracket += 1
        print("TOTAL: ", msg_out, '/', len(total_msg) + len(total_msg_bs))
        print("BS: ", len(analyzed_message_bs), '/', len(total_msg_bs))
        print("Default user: ", len(analyzed_message), '/', len(total_msg))
        packet_loss[i] = (len(total_msg) + len(total_msg_bs) - msg_out) / (len(mas_msg[i]) + len(mas_msg_bs[i]))
        print("Packet loss: ", packet_loss[i])
        delay[i] /= msg_out
        throughput[i] = msg_out / num_of_slots
    return throughput, packet_loss, delay


if __name__ == "__main__":
    simulation_time = 1720
    slots = 172
    frames = simulation_time // slots
    nfig = 1
    lambd = []
    lambd_bs = []
    for i in range(1, 11):
        if ((i * slots / 10) - 1) > 1:
            lambd.append((i * slots / 10) - 1)                              # Отводим 1 сообщение на решение абоненту-БС
        else:
            lambd.append((i * slots / 10))
        lambd_bs.append(i / 10)                        # Для БС лямбда - доля фреймов, в которых БС передает 1 сообщение

    messages = poisson(lambd, frames, slots, 0)
    messages_bs = poisson(lambd_bs, frames, slots, 1)
    res = asynchV2V(messages, messages_bs, frames, slots, 1)

    for i in range(len(lambd)):
        lambd[i] /= slots

    nfig += 1
    plt.figure(nfig)
    plt.plot(lambd, res[0])
    plt.yscale('log')
    plt.grid(True)
    plt.show()

    nfig += 1
    plt.figure(nfig)
    plt.plot(lambd, res[1])
    plt.yscale('log')
    plt.grid(True)
    plt.ylim([0.0001, 1])
    plt.show()

    nfig += 1
    plt.figure(nfig)
    plt.plot(lambd, res[2])
    plt.yscale('log')
    plt.grid(True)
    plt.show()