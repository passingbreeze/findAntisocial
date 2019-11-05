# -*- encoding:utf-8 -*-

import re

## Path Config in here
readTargetFolder = 'My Path'
outTargetFolder = readTargetFolder + 'conv_'

headNumber = range(4,9)
indexNumber = range(1,100)
fileCategory = ['CM','CK','CL']

contentReg = r'<s n=\d+>(.*?)<\/s>'

def remove_tag(content):
   cleanr = re.compile('<.*?>')
   cleantext = re.sub(cleanr, '', content)
   specialr = re.compile('[\:\,\.\?\~]')
   cleantext = re.sub(specialr,'',cleantext) 
   return cleantext

def parse(fileName):
    rx = re.compile(contentReg)
    result = ""
    try:
        rf = open(readTargetFolder + fileName, 'r', encoding='utf-16-le')
        wf = open(outTargetFolder + fileName,'w', encoding='utf-8')
        lines  = rf.readlines()
        cnt = 0
        for line in lines:
            cnt += 1
            m = rx.findall(line)
            for mm in m:
                curret = remove_tag(mm)
                if not curret:
                    continue
                result += curret + ' #\n'
        
        wf.write(result)
        rf.close()
        wf.close()
    except FileNotFoundError:
        print(fileName + ': FNF Error')
        pass

def main():
    for headnumber in headNumber:
        for filecategory in fileCategory:
            for indexnumber in indexNumber:
                numberFormat = str(indexnumber).zfill(5)
                filename = str(headnumber) + filecategory + numberFormat + '.txt'
                parse(filename)

    
if __name__ == '__main__':
    main()