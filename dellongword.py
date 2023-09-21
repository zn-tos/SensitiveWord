import os

filePath = '.\\s\\'
wordlist = os.listdir(filePath)
print(wordlist)
for i in wordlist:
    w = []
    path = os.getcwd() + '\\s\\' + i
    wordsFile = open(path, 'r+', encoding='utf-8')
    for q in wordsFile.readlines():
        q = q.strip('\n')
        j = str(q)
        if(len(j)<=10):
            w.append(j)
    print(w)
    wordsFile.truncate(0)
    wordsFile.close()
    os.remove(path)
    wordsFile1 = open(path, 'w+', encoding='utf-8')
    for p in range(len(w)):
        wordsFile1.write(str(w[p]))
        wordsFile1.write('\n')
    wordsFile1.close()
