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


def asynchV2V(mas_msg, num_of_frames, num_of_slots, polynomial):
    lambd_out = []
    packet_loss = []
    total_msg = []
    cur_msg = []
    delay = []
    queue = 0
    l_bracket = 0
    r_bracket = num_of_slots
    for i in range(len(mas_msg)):
        lambd_out.append(0)
        packet_loss.append(0)
        total_msg.append(0)
        delay.append(0)
        total_msg += mas_msg[i]
        l_bracket = 0
        r_bracket = num_of_slots * 5
        j = 0
        while r_bracket <= num_of_frames * num_of_slots:
            while total_msg[i][j] < r_bracket - 1:
                cur_msg.append(total_msg[i][j])
                j += 1
            if len(cur_msg) > 1:
                processing
    return lambd_out, packet_loss


if __name__ == "__main__":
    simulation_time = 100
    sframe_size = 10
    frames = simulation_time // sframe_size
    nfig = 1
    lambd = []
    for i in range(1, 11):
        lambd.append(i * sframe_size / 10)

    messages = poisson(lambd, frames, sframe_size)
    res = asynchV2V(messages, frames, sframe_size, 1)
