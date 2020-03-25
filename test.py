from no_list import no_list
f = open("db.txt", 'r')
i = 0
db = {}
d = open("db.py",'w')
while True:
    line = f.readline()
    line=line.split(' ')[0]
    if not line: break
    if not(line[0] in db.keys()):
        db.update({line[0] : [line]})
    else :
        if not ("(어인정)" in line or "{끄투 코리아}" in line):
            if not line in no_list:
                line = line.replace(" ","")
                line = line.strip()
                db[line[0]].append(line)
                print(line)


f.close()

d.write(str(db))
#
# str = "리(이)"
# str = str.split('(')
#
# for s in str:
#     s = s.replace(')','')
#     print(s)