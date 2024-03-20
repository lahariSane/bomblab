import os, time
result = ""


def phase_1(file_location):
    os.system(f"strings  '{file_location}' > strings.txt")
    with open("strings.txt") as file:
        strings = file.readlines()
    for string in strings:
        if len(string) > 7 and "%s" not in string and "number 2" not in string:
            os.system(f"echo '{string}' |  '{file_location}' > status.txt")
            with open('status.txt', 'r') as file:
                status = file.read()
                if 'BOOM' not in status:
                    result = string
                    os.remove("strings.txt")
                    os.remove("status.txt")
                    with open('answers.txt', 'w') as file:
                        file.write(result)
                    print(result)
                    return result
    exit()

def phase_2(result_1, file_location):
    ans = ["1 2 4 8 16 32", "0 1 3 6 10 15", "0 1 1 2 3 5"]
    for res in ans:
        result = f"{result_1}{res}"
        os.system(f"echo '{result}' |  '{file_location}' |  cat > new.txt")
        with open("./new.txt", 'r') as file:
            res = file.read()
            if 'BOOM!!!' not in res:
                with open('answers.txt', 'w') as file:
                    file.write(result)
                print(result)
                return result

    for i in range(0, 10):
        for j in range(0, 10):
            for k in range(0, 10):
                for l in range(0, 10):
                    for m in range(0, 20):
                        for n in range(0, 50):
                            result = f"{result_1}{i} {j} {k} {l} {m} {n}"
                            os.system(f"echo '{result}' |  '{file_location}' |  cat > new.txt")
                            with open("./new.txt", 'r') as file:
                                res = file.read()
                                if 'BOOM!!!' not in res:
                                    with open('answers.txt', 'w') as file:
                                        file.write(result)
                                    print(result)
                                    return result
    exit()

def phase_3(result_2, file_location):
    for i in range(0, 7):
        for j in range(-500, 500):
            result = f"{result_2}\n{i} {j}"
            os.system(f"echo '{result}' |  '{file_location}' |  cat > new.txt")
            with open("./new.txt", 'r') as file:
                res = file.read()
                if 'BOOM!!!' not in res:
                    with open('answers.txt', 'w') as file:
                        file.write(result)
                    print(result)
                    return result
                
    for i in range(0, 3):
        for j in range(97, 123): 
            for k in range(-1000, 1000):
                result = f"{result_2}\n{i} {chr(j)} {k}"
                print(result)
                os.system(f"echo '{result}' |  '{file_location}' |  cat > new.txt")
                with open("./new.txt", 'r') as file:
                    res = file.read()
                    if 'BOOM!!!' not in res:
                        with open('answers.txt', 'w') as file:
                            file.write(result)
                        print(result)
                        return result

    exit()
         
def phase_4(result_3, file_location):
    os.system(f"strings  '{file_location}' > strings.txt")
    with open("strings.txt") as file:
        strings = file.readlines()
    for i in range(0, len(strings)):
        if len(strings[i]) == 7:
            str1 = strings[i+1]
            str2 = strings[i]
            res = ""
            for j in range(0, len(str2)):
                for i in range(0, len(str1)):
                    if str2[j] == str1[i]:
                        res += hex(i)[-1]
                        break
                if len(res) == 6:
                    break

            di = {'1': 'a', '2': 'b', '3': 'c', '4': 'd', '5': 'e', '6': 'f', '7': 'g', '8': 'h', '9': 'i', 'a': 'j', 'b': 'k', 'c': 'l', 'd': 'm', 'e': 'n', 'f': 'o'}
            for i in res:
                try: res = res.replace(i, di[i])
                except: pass
            result = f"{result_3}\n{res}"
            os.system(f"echo '{result}' |  '{file_location}' |  cat > new.txt")
            with open("./new.txt", 'r') as file:
                res = file.read()
                if 'BOOM!!!' not in res:
                    with open('answers.txt', 'w') as file:
                        file.write(result)
                    print(result)

    for i in range(0, 500):
        for j in range(-500, 500):
            result = f"{result_3}\n{i} {j}"
            os.system(f"echo '{result}' |  '{file_location}' |  cat > new.txt")
            with open("./new.txt", 'r') as file:
                res = file.read()
                if 'BOOM!!!' not in res:
                    with open('answers.txt', 'w') as file:
                        file.write(result)
                    print(result)    
                    return result


def phase_6(result_5, file_location):
    for i in range(1, 7):
        for j in range(1, 7):
            for k in range(1, 7):
                for l in range(1, 7):
                    for m in range(1, 7):
                        for n in range(1, 7):
                            result = f"{result_5}\n{i} {j} {k} {l} {m} {n}"
                            os.system(f"echo '{result}' | '{file_location}' |  cat > new.txt")
                            with open("./new.txt", 'r') as file:
                                res = file.read()
                                if 'BOOM!!!' not in res:
                                    with open('answers.txt', 'w') as file:
                                        file.write(result)
                                    print(result)
                                    exit()


def extract_bomb(file_location):
    try:
        with open("./answers.txt", 'r') as file:
            result = file.read()
            length = len(result.splitlines())
    except:
        length = 0

    if length == 0:
        print("Testing phase 1....")
        result = phase_1(file_location)
        length += 1
    if length == 1:
        print("Testing phase 2....")
        result = phase_2(result, file_location)
        length += 1
    if length == 2:
        print("Testing phase 3....")
        result = phase_3(result, file_location)
        length += 1
    if length == 3:
        print("Testing phase 4....")
        result = phase_4(result, file_location)
        length += 1
    if length == 4:
        print("Testing phase 5....")
        result = phase_4(result, file_location)
        length += 1
    if length == 5:
        print("Testing phase 6....")
        result = phase_6(result, file_location)
