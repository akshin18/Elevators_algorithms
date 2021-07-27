mport os
from time import sleep
from threading import Thread as th
import ujson
import sqlite3
from math import fabs
###########################


ELEVATORS_DIC =  []


con = sqlite3.connect('test.db')
cur = con.cursor()
cur.execute('''  UPDATE akshin SET floor = '1',direction = 'XX',dir_floor = '[]',dir_go = '[]',access = '0',people = 0,may = 1   ''')
con.commit()
samata = ['03102','01032']
cur.execute('''SELECT name from akshin''')
for i in cur.fetchall():

    ELEVATORS_DIC.append({'name':i[0],'floor':1,'direction':'XX','dir_floor':[],'dir_go':[],'access':0,'people':0,'may':1})



tumba = len(ELEVATORS_DIC)

def main():
    for zi,a in enumerate(samata):


        th(target=con,args=[a,zi]).start()
        sleep(30)



def con(my_flor,zizo):
    global tumba,ELEVATORS_DIC
    con = sqlite3.connect('test.db')
    cur = con.cursor()
    my_floor = int(my_flor[:2])
    get_floor = int(my_flor[2:4])
    people = {}
    pip = {}
    RESSA_DIR = {}
    cur.execute('''SELECT name from akshin''')
    for i in cur.fetchall():
        pip.update({i[0]: 0})
        people.update({i[0]: int(my_flor[-1])})
        RESSA_DIR.update({i[0]: ''})


    numba = 0
    ###############################################################################################
    while 0 not in [people[x] for x in people]:

        RESSA = {}
        cur.execute('''SELECT name from akshin''')
        for i in cur.fetchall():
            RESSA.update({i[0]:None})



        if tumba != 0 or 1 in [people[x] for x in people] :

            if tumba != 0 :
                tumba -= 1
                numba = 1




            for i in ELEVATORS_DIC:

                elevator_floor = i.get('floor')

                if i.get('people') <2:

                    if elevator_floor <= my_floor < get_floor:
                        if i.get('direction') == 'XX' or i.get('direction') == 'AA':
                            direction = 'AA'
                            RESSA_DIR.update({i.get('name'): direction})
                            RESSA.update({i.get('name'): int(fabs(my_floor - elevator_floor))})
                    if elevator_floor <= my_floor > get_floor:
                        if i.get('direction') == 'XX' or i.get('direction') == 'AV':
                            direction = 'AV'
                            RESSA_DIR.update({i.get('name'): direction})
                            RESSA.update({i.get('name'): int(fabs(my_floor - elevator_floor))})
                    if elevator_floor >= my_floor > get_floor:
                        if i.get('direction') == 'XX' or i.get('direction') == 'VV':
                            direction = 'VV'
                            RESSA_DIR.update({i.get('name'): direction})
                            RESSA.update({i.get('name'): int(fabs(my_floor - elevator_floor))})
                    if elevator_floor >= my_floor and my_floor < get_floor:
                        if i.get('direction') == 'XX' or i.get('direction') == 'VA':
                            direction = 'VA'
                            RESSA_DIR.update({i.get('name'): direction})
                            RESSA.update({i.get('name'): int(fabs(my_floor - elevator_floor))})
                    same = i.get('direction')

                    if [x for x in RESSA_DIR.values()].count('') != len(RESSA_DIR):

                        if direction == same or numba == 1:
                            if people[i.get('name')] + i.get('people') <= 2:

                                # print('!!!!!!!!!!!!!!!!!!!!!!!!!!',tumba,my_flor)
                                pip[i.get('name')] = people[i.get('name')]
                                people[i.get('name')] = 0
                                numba = 1

                            else:
                                pip[i.get('name')] = 2 - i.get('people')
                                people[i.get('name')] = people.get(i.get('name')) - pip.get(i.get('name'))



        ###############################################################################################

        ###############################################################################################

        if [x for x in RESSA.values()].count(None) != len(RESSA) and [x for x in RESSA.values()].count(999) != len(RESSA):

            for izi in RESSA:
                if RESSA[izi] == None:
                    RESSA[izi] = 9999




            name = []
            for x in RESSA:
                if 'XX' in [y.get('direction') for y in ELEVATORS_DIC] and RESSA[x] == min(RESSA.values()):
                    for rwe in ELEVATORS_DIC:
                        if rwe.get('name') ==x:
                            if rwe.get('direction') == 'XX':
                                name.append(x)
                else:
                    if RESSA[x] == min(RESSA.values()):
                        name.append(x)

            print(RESSA, '!!!!!!!!!!!!!!!!!!!!!!!!!!@@@@@@@@@@@@@@@@@',name)


            for fi in name:

                    if [x for x in ELEVATORS_DIC if x.get('name') == fi][0].get('people') < 2 and [x for x in ELEVATORS_DIC if x.get('name') == fi][0].get('direction') == 'XX':
                        name = fi
                        break

            # print(name, '............................', RESSA, my_flor)
            while True:
                part = 0
                for i in RESSA:
                    if name == i:
                        part = 1
                        break
                if part != 1:
                    for i in RESSA:
                        if name[0] == i:
                            name = name[0]
                            part = 1
                            break
                if part == 1:
                    break

            may = [x for x in ELEVATORS_DIC if x.get('name') == name][0].get('may')

            if numba == 1 :


                [x for x in ELEVATORS_DIC if x.get('name') == name][0].update({'may':0})
                # print('1    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%', [people[x] for x in people], RESSA,RESSA_DIR,my_flor)
                cur.execute(f'''SELECT dir_floor from akshin where name = '{name}' ''')
                busa = ujson.loads(cur.fetchall()[0][0])
                cur.execute(f'''SELECT dir_go from akshin where name = '{name}' ''')
                susa = ujson.loads(cur.fetchall()[0][0])
                susa.append(get_floor)
                busa.append(my_floor)
                cur.execute(f'''SELECT people from akshin where name = '{name}' ''')
                peop = cur.fetchall()[0][0]
                peop += pip[name]
                [x for x in ELEVATORS_DIC if x.get('name') == name][0].update(
                    {'direction': RESSA_DIR.get(f'{name}'), 'dir_floor': busa, 'dir_go': susa,
                     'people': peop})
                cur.execute(
                    f"""UPDATE akshin SET may = 0, direction = '{RESSA_DIR.get(f'{name}')}', dir_floor = '{ujson.dumps(busa)}',dir_go = '{ujson.dumps(susa)}',people = {peop} where name = '{name}' """)
                con.commit()
                print([x for x in ELEVATORS_DIC if x.get('name') == name][0],zizo)
                if may == 1:
                    [x for x in ELEVATORS_DIC if x.get('name') == name][0].update(
                        {'direction': RESSA_DIR.get(f'{name}'), 'dir_floor': busa, 'dir_go': susa, 'access': 1,
                         'people': peop})

                    cur.execute(
                        f"""UPDATE akshin SET may = 0, direction = '{RESSA_DIR.get(f'{name}')}', dir_floor = '{ujson.dumps(busa)}',dir_go = '{ujson.dumps(susa)}',access = {1},people = {peop} where name = '{name}' """)
                    con.commit()
                    th(target=timer,args=(name,)).start()
                break
    # print('2    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%',[people[x] for x in people],RESSA,RESSA_DIR,my_flor)

def timer(name):
    global tumba,ELEVATORS_DIC
    con = sqlite3.connect('test.db')
    cur = con.cursor()
    [x for x in ELEVATORS_DIC if x.get('name') == name][0].update({'access':0})
    cur.execute(f'''UPDATE akshin set access = '0' WHERE name = '{name}' ''')
    con.commit()
    cur.execute(f'''SELECT * from akshin where name = '{name}' ''')
    ELEVATORS = cur.fetchall()
    print(ELEVATORS[0])
    # while ELEVATORS[0][2] != 'XX':
    while [x for x in ELEVATORS_DIC if x.get('name') == name][0].get('direction') != 'XX':
        cur.execute(f'''SELECT * from akshin where name = '{name}' ''')
        ELEVATORS = cur.fetchall()
        gloria = [x for x in ELEVATORS_DIC if x.get('name') == name][0].get('direction')


        # if ELEVATORS[0][5] == 1:

        floor = [x for x in ELEVATORS_DIC if x.get('name') == name][0].get('floor')
            # print(name, floor)

            # print(name,'----------------------------------------------------------------------------------*',b,c)
        b = ujson.loads(ELEVATORS[0][3])
        c = ujson.loads(ELEVATORS[0][4])
        passa = True
        cur.execute(f'''SELECT * from akshin where name = '{name}' ''')
        ELEVATORS = cur.fetchall()

        if gloria == 'AA' and [x for x in ELEVATORS_DIC if x.get('name') == name][0].get('access') == 0:

                if b != [] :
                    if int(str(min(b))) > floor and passa and int(str(min(c))) > int(str(min(b))):

                        floor += 1
                        cur.execute(f'''UPDATE akshin set floor = floor + 1 WHERE name = '{name}' ''')
                        con.commit()
                        [x for x in ELEVATORS_DIC if x.get('name') == name][0].update({'floor':floor})

                        print(f'Elevator : {name[-1]} ','El_Floor : ',floor, str(min(b))[0])
                        sleep(2)
                        passa = False
                    if int(str(min(b))) == floor and b != [] and passa and int(str(min(c))) > int(str(min(b))):

                        print(f'Elevator : {name[-1]} ','остановка на ' + str(min(b))[0])
                        b.remove(min(b))
                        cur.execute(
                            f'''UPDATE akshin set dir_floor = '{b}' WHERE name = '{name}' ''')
                        con.commit()
                        [x for x in ELEVATORS_DIC if x.get('name') == name][0].update({'dir_floor':b})

                        sleep(3)
                        passa = False
                if  c != []:
                    if int(str(min(c))) > floor and passa:

                        floor += 1
                        cur.execute(f'''UPDATE akshin set floor = floor + 1 WHERE name = '{name}' ''')
                        con.commit()
                        [x for x in ELEVATORS_DIC if x.get('name') == name][0].update({'floor':floor})

                        # ELEVATORS[0]['floor'] += 1
                        print(f'Elevator : {name[-1]} ','El_Floor : ',floor, str(min(c)))
                        sleep(2)
                        passa = False
                    if int(str(min(c))) == floor and passa:

                        print(f'Elevator : {name[-1]} ','остановка наr ' + str(min(c)))
                        c.remove(min(c))
                        cur.execute(
                            f'''UPDATE akshin set people = people - 1,dir_go = '{c}' WHERE name = '{name}' ''')
                        con.commit()
                        pap = [x for x in ELEVATORS_DIC if x.get('name') == name][0].get('people') - 1
                        [x for x in ELEVATORS_DIC if x.get('name') == name][0].update({'dir_go':c,'people':pap})


                        sleep(3)
                        passa = False
                if b == [] and c == [] :
                    # b.remove(b[0])
                    # c.remove(c[0])
                    cur.execute(
                        f'''UPDATE akshin set dir_floor =  '{b}',people = '0',direction = 'XX',dir_go = '{c}',may = 1 WHERE name = '{name}' ''')
                    con.commit()
                    [x for x in ELEVATORS_DIC if x.get('name') == name][0].update({'dir_floor':b,'people':0,'direction':'XX','dir_go':c,'may':1})


                    tumba +=1

                    # ELEVATORS[0]['dir_floor'] = []
                    # ELEVATORS[0]['people'] = 0
                    # ELEVATORS[0]['direction'] = 'XX'
                    # ELEVATORS[0]['dir_go'] = []


        cur.execute(f'''SELECT * from akshin where name = '{name}' ''')
        ELEVATORS = cur.fetchall()
        if gloria == 'VV' and [x for x in ELEVATORS_DIC if x.get('name') == name][0].get('access') == 0:
            if b != []:
                if int(str(max(b))) < floor and passa and int(str(max(c))) < int(str(max(b))):

                    floor -= 1
                    cur.execute(f'''UPDATE akshin set floor = floor - 1 WHERE name = '{name}' ''')
                    con.commit()
                    [x for x in ELEVATORS_DIC if x.get('name') == name][0].update({'floor': floor})

                    print(f'Elevator : {name[-1]} ','El_Floor : ',floor, str(max(b)))
                    sleep(2)
                    passa = False
                if int(str(max(b))) == floor and b != [] and passa and int(str(max(c))) < int(str(max(b))):

                    print(f'Elevator : {name[-1]} ','остановка на ' + str(max(b)))
                    b.remove(max(b))
                    cur.execute(
                        f'''UPDATE akshin set dir_floor = '{b}' WHERE name = '{name}' ''')
                    con.commit()
                    [x for x in ELEVATORS_DIC if x.get('name') == name][0].update({'dir_floor': b})

                    sleep(3)
                    passa = False
            if c != []:
                if int(str(max(c))) < floor and passa:

                    floor -= 1
                    cur.execute(f'''UPDATE akshin set floor = floor - 1 WHERE name = '{name}' ''')
                    con.commit()
                    [x for x in ELEVATORS_DIC if x.get('name') == name][0].update({'floor': floor})

                    sleep(2)
                    print(f'Elevator : {name[-1]} ','El_Floor : ',floor, str(max(c)))
                    passa = False
                if int(str(max(c))) == floor and passa:

                    print(f'Elevator : {name[-1]} ','остановка на ' + str(max(c)))
                    c.remove(max(c))
                    pap = [x for x in ELEVATORS_DIC if x.get('name') == name][0].get('people') - 1
                    cur.execute(
                        f'''UPDATE akshin set people = people - 1,dir_go = '{c}' WHERE name = '{name}' ''')
                    con.commit()
                    [x for x in ELEVATORS_DIC if x.get('name') == name][0].update({'dir_go': c,'people':pap})

                    sleep(3)
                    passa = False
            if b == [] and c == []:
                # ELEVATORS[0]['dir_floor'] = []
                # ELEVATORS[0]['people'] = 0
                # ELEVATORS[0]['direction'] = 'XX'
                # ELEVATORS[0]['dir_go'] = []
                cur.execute(
                    f'''UPDATE akshin set dir_floor =  '{b}',people = '0',direction = 'XX',dir_go = '{c}',may = 1 WHERE name = '{name}' ''')
                con.commit()
                [x for x in ELEVATORS_DIC if x.get('name') == name][0].update(
                    {'dir_floor': b, 'people': 0, 'direction': 'XX', 'dir_go': c, 'may': 1})

                tumba +=1

        cur.execute(f'''SELECT * from akshin where name = '{name}' ''')
        ELEVATORS = cur.fetchall()
        if gloria == 'VA' and [x for x in ELEVATORS_DIC if x.get('name') == name][0].get('access') == 0:
            if b != []:
                if int(str(max(b))) < floor and passa:

                    floor -= 1
                    cur.execute(f'''UPDATE akshin set floor = floor - 1 WHERE name = '{name}' ''')
                    con.commit()
                    [x for x in ELEVATORS_DIC if x.get('name') == name][0].update({'floor': floor})

                    print(f'Elevator : {name[-1]} ','El_Floor : ',floor, str(max(b)))
                    sleep(2)
                    passa = False
                if int(str(max(b))) == floor and b != [] and passa:

                    print(f'Elevator : {name[-1]} ','остановка на ' + str(max(b)))
                    b.remove(max(b))
                    cur.execute(
                        f'''UPDATE akshin set dir_floor = '{b}' WHERE name = '{name}' ''')
                    con.commit()
                    [x for x in ELEVATORS_DIC if x.get('name') == name][0].update({'dir_floor': b})

                    sleep(3)
                    passa = False
            if b == [] and c != []:
                if int(str(min(c))) > floor and passa:

                    floor += 1
                    cur.execute(f'''UPDATE akshin set floor = floor + 1 WHERE name = '{name}' ''')
                    con.commit()
                    [x for x in ELEVATORS_DIC if x.get('name') == name][0].update({'floor': floor})

                    print(f'Elevator : {name[-1]} ','El_Floor : ',floor, str(min(c)))
                    sleep(2)
                    passa = False
                if int(str(min(c))) == floor and passa:

                    print(f'Elevator : {name[-1]} ','остановка на ' + str(min(c)))
                    c.remove(min(c))
                    cur.execute(
                        f'''UPDATE akshin set people = people - 1,dir_go = '{c}' WHERE name = '{name}' ''')
                    con.commit()
                    pap = [x for x in ELEVATORS_DIC if x.get('name') == name][0].get('people') - 1
                    [x for x in ELEVATORS_DIC if x.get('name') == name][0].update({'dir_go': c,'people':pap})

                    sleep(3)
                    passa = False
            if b == [] and c == []:
                # ELEVATORS[0]['dir_floor'] = []
                # ELEVATORS[0]['people'] = 0
                # ELEVATORS[0]['direction'] = 'XX'
                # ELEVATORS[0]['dir_go'] = []
                cur.execute(
                    f'''UPDATE akshin set dir_floor =  '{b}',people = '0',direction = 'XX',dir_go = '{c}',may = 1 WHERE name = '{name}' ''')
                con.commit()
                [x for x in ELEVATORS_DIC if x.get('name') == name][0].update(
                    {'dir_floor': b, 'people': 0, 'direction': 'XX', 'dir_go': c, 'may': 1})

                tumba +=1

        cur.execute(f'''SELECT * from akshin where name = '{name}' ''')
        ELEVATORS = cur.fetchall()
        if gloria == 'AV' and [x for x in ELEVATORS_DIC if x.get('name') == name][0].get('access') == 0:
            if b != []:
                if int(str(min(b))) > floor and passa:

                    floor += 1
                    cur.execute(f'''UPDATE akshin set floor = floor + 1 WHERE name = '{name}' ''')
                    con.commit()
                    [x for x in ELEVATORS_DIC if x.get('name') == name][0].update({'floor': floor})

                    print(f'Elevator : {name[-1]} ','El_Floor : ',floor, str(min(b)))
                    sleep(2)
                    passa = False
                if int(str(min(b))) == floor and b != [] and passa:

                    print(f'Elevator : {name[-1]} ','остановка на ' + str(min(b)))
                    b.remove(min(b))
                    cur.execute(
                        f'''UPDATE akshin set dir_floor = '{b}' WHERE name = '{name}' ''')
                    con.commit()

                    [x for x in ELEVATORS_DIC if x.get('name') == name][0].update({'dir_floor': b})

                    sleep(3)
                    passa = False
            if b == [] and c != []:
                if int(str(max(c))) < floor and passa:

                    floor -= 1
                    cur.execute(f'''UPDATE akshin set floor = floor - 1 WHERE name = '{name}' ''')
                    con.commit()
                    [x for x in ELEVATORS_DIC if x.get('name') == name][0].update({'floor': floor})

                    print(f'Elevator : {name[-1]} ','El_Floor : ',floor, str(max(c)))
                    sleep(2)
                    passa = False
                if int(str(max(c))) == floor and passa:
                    print(f'Elevator : {name[-1]} ', 'остановка на ' + str(max(c)))
                    c.remove(max(c))
                    if  c == []:
                        cur.execute(
                            f'''UPDATE akshin set people = '0' ,dir_go = '{c}' WHERE name = '{name}' ''')
                        con.commit()
                        [x for x in ELEVATORS_DIC if x.get('name') == name][0].update({'dir_go': c,'people':0})

                    else:
                        cur.execute(
                            f'''UPDATE akshin set people = people - 1 ,dir_go = '{c}' WHERE name = '{name}' ''')
                        con.commit()
                        pap = [x for x in ELEVATORS_DIC if x.get('name') == name][0].get('people') - 1
                        [x for x in ELEVATORS_DIC if x.get('name') == name][0].update({'dir_go': c,'people':pap})



                    sleep(3)
                    passa = False
            if b == [] and c == [] :
                # ELEVATORS[0]['dir_floor'] = []
                # ELEVATORS[0]['people'] = 0
                # ELEVATORS[0]['direction'] = 'XX'
                # ELEVATORS[0]['dir_go'] = []
                cur.execute(
                    f'''UPDATE akshin set dir_floor =  '{b}',people = '0',direction = 'XX',dir_go = '{c}',may = 1 WHERE name = '{name}' ''')
                con.commit()
                [x for x in ELEVATORS_DIC if x.get('name') == name][0].update(
                    {'dir_floor': b, 'people': 0, 'direction': 'XX', 'dir_go': c, 'may': 1})

                tumba +=1


main()


