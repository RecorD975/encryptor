import argparse

parser = argparse.ArgumentParser(description = "Encryptor")
parser.add_argument("regime", help = "4 regimes: encode, decode, train and hack", choices = ["encode", "decode", "train", "hack"])
parser.add_argument("--input-file", help = "not neccessary argument, input.txt", default = "None")
parser.add_argument("--cipher", help = "Caesar and Vigenere", choices = ["caesar", "vigenere"], default = "None")
parser.add_argument("--key", help = "number for caesar or word for vigenere", default = 0)
parser.add_argument("--output-file", help = "not neccessary argument, output.txt", default = "None")
parser.add_argument("--model-file", help = "training results output file, output.txt or model for hacking, input.txt", default = "None")
parser.add_argument("--text-file", help = "input file for training, input.txt", default = "None")
args = parser.parse_args()

def encodeC(text, key):
    Alphavit = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    alphavit = "abcdefghijklmnopqrstuvwxyz"
    restext = ''
    for i in range(len(text)):
        if text[i].isalpha() == 0:
            restext = restext + text[i]
            continue
        if text[i].isupper() == 0:
            for j in range(len(alphavit)):
                if text[i] == alphavit[j]:
                    if j + key >= len(alphavit):
                        restext = restext + alphavit[j + key - len(alphavit)]
                        continue
                    restext = restext + alphavit[j + key]
            continue
        for j in range(len(Alphavit)):
            if text[i] == Alphavit[j]:
                if j + key >= len(Alphavit):
                    restext = restext + Alphavit[j + key - len(Alphavit)]
                    continue
                restext = restext + Alphavit[j + key]
    return restext

def decodeC(text, key):
    Alphavit = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    alphavit = "abcdefghijklmnopqrstuvwxyz"
    restext = ''
    for i in range(len(text)):
        if text[i].isalpha() == 0:
            restext = restext + text[i]
            continue
        if text[i].isupper() == 0:
            for j in range(len(alphavit)):
                if text[i] == alphavit[j]:
                    if j - key < 0:
                        restext = restext + alphavit[j - key + len(alphavit)]
                        continue
                    restext = restext + alphavit[j - key]
            continue
        for j in range(len(Alphavit)):
            if text[i] == Alphavit[j]:
                if j - key < 0:
                    restext = restext + Alphavit[j - key + len(Alphavit)]
                    continue
                restext = restext + Alphavit[j - key]
    return restext

def encodeV(text, key):
    Alphavit = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    alphavit = "abcdefghijklmnopqrstuvwxyz"
    restext = ''
    key_text = ''
    m = 0
    for n in range(len(text)):
        if text[n].isalpha() == 1:
            key_text = key_text + key[m]
            m = m + 1
            if m == len(key):
                m = 0
        else:
            key_text = key_text + text[n]
    for i in range(len(text)):
        if text[i].isalpha() == 0:
            restext = restext + text[i]
            continue
        if text[i].isupper() == 0:
            for j in range(len(alphavit)):
                if text[i] == alphavit[j]:
                    num_text = j
                if key_text[i].lower() == alphavit[j]:
                    num_key = j
            restext = restext + alphavit[(num_text + num_key) % 26]
        else:
            for j in range(len(Alphavit)):
                if text[i] == Alphavit[j]:
                    num_text = j
                if key_text[i].upper() == Alphavit[j]:
                    num_key = j
            restext = restext + Alphavit[(num_text + num_key) % 26]
    return restext

def decodeV(text, key):
    Alphavit = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    alphavit = "abcdefghijklmnopqrstuvwxyz"
    restext = ''
    key_text = ''
    m = 0
    for n in range(len(text)):
        if text[n].isalpha() == 1:
            key_text = key_text + key[m]
            m = m + 1
            if m == len(key):
                m = 0
        else:
            key_text = key_text + text[n]
    for i in range(len(text)):
        if text[i].isalpha() == 0:
            restext = restext + text[i]
            continue
        if text[i].isupper() == 0:
            for j in range(len(alphavit)):
                if text[i] == alphavit[j]:
                    num_text = j
                if key_text[i].lower() == alphavit[j]:
                    num_key = j
            restext = restext + alphavit[(num_text - num_key) % 26]
        else:
            for j in range(len(Alphavit)):
                if text[i] == Alphavit[j]:
                    num_text = j
                if key_text[i].upper() == Alphavit[j]:
                    num_key = j
            restext = restext + Alphavit[(num_text - num_key) % 26]
    return restext

def train(text):
    restext = ''
    numofletters = 0
    for j in range(len(text)):
        if text[j] == ' ':
            continue
        numofletters = numofletters + 1
    for i in range(26):
        restext = restext + str(round(text.count(chr(ord('a') + i)) / numofletters, 3)) + ' '
    return restext

def hack(text, modeltext):
    model_list1 = []
    max_norma = []
    for i in modeltext.split():
        model_list1.append(float(i))
    for key in range(26):
        model_list2 = []
        norma = []
        restext = decodeC(text, key)
        modeltext2 = train(restext)
        for i in modeltext2.split():
            model_list2.append(float(i))
        for k in range(26):
            norma.append(abs(model_list1[k] - model_list2[k]))
        max_norma.append(max(norma))
    for j in range(len(max_norma)):
        if max_norma[j] == min(max_norma):
            break
    restext = decodeC(text, j)
    return restext

if args.regime == "encode" or args.regime == "decode":
    if args.cipher == "None":
        print("Error: cipher is required argument for encode and decode")
        exit()
    if args.key == 0:
        print("Error: key is required argument for encode and decode")
        exit()
    if args.model_file != "None" or args.text_file != "None":
        print("Error: --model-file and --text-file are used for hack or train")
        exit()
elif args.regime == "train" or args.regime == "hack":
    if args.input_file != "None" and args.regime == "train":
        print("Error: --text-file is used for train")
        exit()
    if args.text_file != "None" and args.regime == "hack":
        print("Error: --input-file is used for hack")
        exit()
    if args.cipher != "None" or args.key != 0:
        print("Error: --cipher and --key are used for encode and decode")
        exit()
    if args.model_file == "None":
        print("Error: --model-file is required argument for train and hack")
        exit()

if args.regime == "encode" or args.regime == "decode":
    #Проверка: откуда будут передавать текст в программу
    if args.input_file == "None":
        text = input()
    else:
        file_in = open(args.input_file, 'r')
        text = file_in.read()
        file_in.close()
#Проверка: какой шифр нужно использовать
    if args.cipher == "caesar":
        #Проверка корректность введенных ключей
        if args.key.isdigit() == 0:
            print("key for Caesar must be positive integer")
            exit()
        args.key = int(args.key) 
        if args.regime == "encode":
            restext = encodeC(text, args.key)
        else:
            restext = decodeC(text, args.key)
    else:
        #Проверка корректности введенных ключей
        if args.key.isdigit() == 1:
            print("key for Vigenere must be word")
            exit()
        if args.regime == "encode":
            restext = encodeV(text, args.key)
        else:
            restext = decodeV(text, args.key)

    #Проверка: куда выводить полученный текст
    if args.output_file == "None":
        print(restext)
        exit()
    file_out = open(args.output_file, 'w')
    file_out.write(restext)
    file_out.close()
    exit()

elif args.regime == "train":
    if args.text_file == "None":
        text = input()
    else:
        file_in = open(args.text_file, 'r')
        text = file_in.read()
        file_in.close()
    restext = train(text)
    file_out = open(args.model_file, 'w')
    file_out.write(restext)
    file_out.close()

elif args.regime == "hack":
    if args.input_file == "None":
            text = input()
    else:
        file_in = open(args.input_file, 'r')
        text = file_in.read()
        file_in.close()
    file_model = open(args.model_file, 'r')
    modeltext = file_model.read()
    restext = hack(text, modeltext)
    if args.output_file == "None":
        print(restext)
    else:
        file_out = open(args.output_file, 'w')
        file_out.write(restext)
        file_out.close()