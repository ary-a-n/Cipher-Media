import numpy as np
import os
import cv2
import wave


def msg_to_binary(data):
    # Function to convert message/data to binary format
    if isinstance(data, str):
        return ''.join([format(ord(i), "08b") for i in data])
    elif isinstance(data, bytes) or isinstance(data, np.ndarray):
        return [format(i, "08b") for i in data]
    elif isinstance(data, int) or isinstance(data, np.uint8):
        return format(data, "08b")
    else:
        raise TypeError("Input type not supported")

# Image Stenography


def img_encoder(img, data):
    if (len(data) == 0):
        raise ValueError('Data entered to be encoded is empty')

    no_of_bytes = (img.shape[0] * img.shape[1] * 3) // 8

    # print("\t\nMaximum bytes to encode in Image :", no_of_bytes)

    if (len(data) > no_of_bytes):
        raise ValueError(
            "Insufficient bytes Error, Need Bigger Image or give Less Data !!")

    data += '**^^*'

    bin_data = msg_to_binary(data)
    # print("\n")
    # print(bin_data)
    length_data = len(bin_data)

    # print("\nThe Length of Binary data",length_data)

    index_data = 0
    for i in img:
        for pixel in i:
            r, g, b = msg_to_binary(pixel)
            if index_data < length_data:
                pixel[0] = int(r[:-1] + bin_data[index_data], 2)
                index_data += 1
            if index_data < length_data:
                pixel[1] = int(g[:-1] + bin_data[index_data], 2)
                index_data += 1
            if index_data < length_data:
                pixel[2] = int(b[:-1] + bin_data[index_data], 2)
                index_data += 1
            if index_data >= length_data:
                break
    return img


def img_decoder(img):
    data_binary = ""
    for i in img:
        for pixel in i:
            r, g, b = msg_to_binary(pixel)
            data_binary += r[-1]
            data_binary += g[-1]
            data_binary += b[-1]
            total_bytes = [data_binary[i: i+8]
                           for i in range(0, len(data_binary), 8)]
            decoded_data = ""
            for byte in total_bytes:
                decoded_data += chr(int(byte, 2))
                if decoded_data[-5:] == "**^^*":
                    return (decoded_data[:-5])
    return None



def audio_encode(input_file, output_file, data):
    song = wave.open(input_file, mode='rb')

    nframes = song.getnframes()
    frames = song.readframes(nframes)
    frame_list = list(frames)
    frame_bytes = bytearray(frame_list)

    data = data + '*^*^*'  # Mark end of message

    result = []
    for c in data:
        bits = bin(ord(c))[2:].zfill(8)
        result.extend([int(b) for b in bits])

    j = 0
    for i in range(len(result)):
        res = bin(frame_bytes[j])[2:].zfill(8)
        if res[-4] == str(result[i]):
            frame_bytes[j] = (frame_bytes[j] & 253)  # 253: 11111101
        else:
            frame_bytes[j] = (frame_bytes[j] & 253) | 2
            frame_bytes[j] = (frame_bytes[j] & 254) | result[i]
        j += 1

    frame_modified = bytes(frame_bytes)

    with wave.open(output_file, 'wb') as fd:
        fd.setparams(song.getparams())
        fd.writeframes(frame_modified)

    song.close()

def decode_audio(input_file):
    song = wave.open(input_file, mode='rb')

    nframes = song.getnframes()
    frames = song.readframes(nframes)
    frame_list = list(frames)
    frame_bytes = bytearray(frame_list)

    extracted = ""
    p = 0
    for i in range(len(frame_bytes)):
        if p == 1:
            break
        res = bin(frame_bytes[i])[2:].zfill(8)
        if res[-2] == '0':
            extracted += res[-4]
        else:
            extracted += res[-1]

    all_bytes = [extracted[i: i + 8] for i in range(0, len(extracted), 8)]
    decoded_data = ""
    for byte in all_bytes:
        decoded_data += chr(int(byte, 2))
        if decoded_data[-5:] == "*^*^*":
            decoded_data = decoded_data[:-5]
            p = 1
            break

    song.close()
    return decoded_data

#

def KSA(key):
    key_length = len(key)
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % key_length]) % 256
        S[i], S[j] = S[j], S[i]
    return S

def PRGA(S, n):
    i = 0
    j = 0
    key = []
    while n > 0:
        n = n - 1
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        key.append(K)
    return key

def preparing_key_array(s):
    return [ord(c) for c in s]

def encryption(text, key):
    key = preparing_key_array(key)
    S = KSA(key)
    keystream = np.array(PRGA(S, len(text)))
    text = np.array([ord(i) for i in text])
    cipher = keystream ^ text
    ctext = ''.join([chr(c) for c in cipher])
    return ctext

def decryption(ciphertext, key):
    key = preparing_key_array(key)
    S = KSA(key)
    keystream = np.array(PRGA(S, len(ciphertext)))
    ciphertext = np.array([ord(i) for i in ciphertext])
    decoded = keystream ^ ciphertext
    dtext = ''.join([chr(c) for c in decoded])
    return dtext

def embed(frame, data, key):
    data = encryption(data, key)
    data += '*^*^*'
    binary_data = msg_to_binary(data)
    length_data = len(binary_data)
    index_data = 0
    for i in frame:
        for pixel in i:
            r, g, b = msg_to_binary(pixel)
            if index_data < length_data:
                pixel[0] = int(r[:-1] + binary_data[index_data], 2)
                index_data += 1
            if index_data < length_data:
                pixel[1] = int(g[:-1] + binary_data[index_data], 2)
                index_data += 1
            if index_data < length_data:
                pixel[2] = int(b[:-1] + binary_data[index_data], 2)
                index_data += 1
            if index_data >= length_data:
                break
    return frame

def extract(frame, key):
    data_binary = ""
    final_decoded_msg = ""
    for i in frame:
        for pixel in i:
            r, g, b = msg_to_binary(pixel)
            data_binary += r[-1]
            data_binary += g[-1]
            data_binary += b[-1]
            total_bytes = [data_binary[i: i + 8] for i in range(0, len(data_binary), 8)]
            decoded_data = ""
            for byte in total_bytes:
                decoded_data += chr(int(byte, 2))
                if decoded_data[-5:] == "*^*^*":
                    final_decoded_msg = decryption(decoded_data[:-5], key)
                    return final_decoded_msg
    return final_decoded_msg

def encode_vid_data(video_path, output_path, frame_number, data, key):
    cap = cv2.VideoCapture(video_path)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    out = cv2.VideoWriter(output_path, fourcc, 25.0, (frame_width, frame_height))
    current_frame = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        current_frame += 1
        if current_frame == frame_number:
            frame = embed(frame, data, key)
        out.write(frame)
    cap.release()
    out.release()
    return frame

def decode_vid_data(video_path, frame_number, key):
    cap = cv2.VideoCapture(video_path)
    current_frame = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        current_frame += 1
        if current_frame == frame_number:
            return extract(frame, key)
    cap.release()
    return ""