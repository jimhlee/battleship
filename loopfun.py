def balls():
    output = []
    for i in range(10):
        output.append(i)
        ctr = 0
        while True:
            ctr += 1

        output.append(i * 100)
    output.append('rat')
    return output

def yeet():
    output = {}
    for i in range(10):
        if i % 2:
            continue
        val = []
        ctr = 0
        while True:
            if ctr % 3:
                ctr += 2
                continue
            val.append(ctr * i)
            if ctr > 10:
                break
            ctr += 1
        output[i] = val
    return output