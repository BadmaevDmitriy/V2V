import matplotlib.pyplot as plt
from math import *
import random as rnd
import numpy as np


def poisson(lambd, frames):
    messages = []
    for i in range(len(lambd)):
        messages.append(i)
        messages[i] = np.random.poisson(lambd[i], frames)
    # lout = []
    # for i in range(len(lambd)):
    #     msg = 0
    #     for j in range(frames):
    #         msg += messages[i][j]
    #     msg /= frames
    #     lout.append(msg)
    # for i in range(len(lambd)):
    #     print(lout[i])
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


def processing(subscribers, slots, polynomial):
    queue = [[] for i in range(slots)]
    msg_left = subscribers
    copy = 2
    if polynomial == 2:
        copy = 1
    for k in range(subscribers):
        rand_num = rnd.random()
        if polynomial == 1:
            if rand_num <= 0.5:
                copy = 2
            elif 0.5 < rand_num <= 0.78:
                copy = 3
            else:
                copy = 8
        j = 0
        while j < copy:
            rand = rnd.randint(0, slots - 1)
            if not(contains(queue[rand], k)):
                if not(queue[rand])
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


def slotted_aloha(mas_msg, num_of_frames, num_of_slots, polynomial):
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
                packet_loss[i] += processing(queue, num_of_slots, polynomial)
            if mas_msg[i][j] > 0:
                queue = mas_msg[i][j]
        lambd_out[i] = (total_msg[i] - packet_loss[i]) / frames
        packet_loss[i] /= total_msg[i]
        packet_loss[i] *= 100
    return lambd_out, packet_loss


if __name__ == "__main__":
    simulation_time = 100000
    slots = 100
    frames = simulation_time // slots
    nfig = 1
    lambd = []
    for i in range(1, 11):
        lambd.append(i * slots / 10)

    messages = poisson(lambd, frames)

    res = slotted_aloha(messages, frames, slots, 0)
    res2 = slotted_aloha(messages, frames, slots, 1)
    res3 = slotted_aloha(messages, frames, slots, 2)

    for i in range(len(lambd)):
        lambd[i] /= slots
        res[0][i] /= slots
        res2[0][i] /= slots
        res3[0][i] /= slots

    # info1 = "CRDSA. Frames = " + str(frames) + ", Size of frame = " + str(slots)
    # info2 = "IRSA. Frames = " + str(frames) + ", Size of frame = " + str(slots)
    # info3 = "SA. Frames = " + str(frames) + ", Size of frame = " + str(slots)
    info1 = "CRDSA"
    info2 = "IRSA"
    info3 = "SA"
    info4 = str(slots) + " slots"

    nfig += 1
    plt.figure(nfig)
    plt.plot(lambd, res[0], "-r", label=info1)
    plt.plot(lambd, res2[0], "-y", label=info2)
    plt.plot(lambd, res3[0], "-b", label=info3)
    plt.xlabel("$\lambda$\n" + str(slots) + " slots")
    plt.ylabel("$\lambda$out")
    plt.xlim([0, 1])
    plt.ylim([0, 0.7])
    plt.grid()
    plt.legend()
    plt.show()

    for i in range(len(lambd)):
        print("Packet loss for lambd = " + str(lambd[i]) + " : CRDSA " + "%.2f" % res[1][i] + " %  IRSA " + "%.2f" % res2[1][i] + " %  SA " + "%.2f" % res3[1][i] + " %")