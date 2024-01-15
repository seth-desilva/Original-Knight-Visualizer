import pygame  # pip install
import math
import copy
import pyperclip  # pip install

pygame.init()

normalfont = pygame.font.Font('freesansbold.ttf', 18)
smallfont = pygame.font.Font('freesansbold.ttf', 8)
font1 = pygame.font.SysFont('Calibri', 25)
FramePerSec = pygame.time.Clock()

height = 570
width = 500
realwidth = 700
canvas = pygame.display.set_mode((width, height))

maxjumplength = 9

jumpstring = "363603636"  # len 38 max
while jumpstring == 0:
    try:
        jumpstring = input("What string to draw?:")
        for each in str(jumpstring):
            if int(each) > 7:
                jumpstring = 0
    except:
        jumpstring = 0;
        print("String invalid. Please input a valid string (nums 0 to 7).")
jumpx = 2
while jumpx == 0:
    try:
        jumpx = int(input("Jump X:"))
        if abs(jumpx) != jumpx:
            jumpx = makeerror  # <- Haha, python. I love interpreted languages.
    except:
        pass
    if jumpx == 0:
        print("Jump X invalid. Integers, please!")
jumpy = 3  #
while jumpy == 0:
    try:
        jumpy = int(input("Jump Y:"))
        if abs(jumpy) != jumpy:
            jumpx = makeerror
    except:
        pass
    if jumpy == 0:
        print("Jump Y invalid. Integers, please!")

pygame.display.set_caption("Shape drawer")


def generatenewboard(size, jump):
    if size % 2 != 1:
        return "Invalid board size."
    mid = int((size + 1) / 2) - 1
    board = [[[mid, mid]], [mid, mid], jump, size,
             ""]  # placed blocks, current position, jump distance, board size, jumpstring
    return board


def generateoldboard(size):
    if size % 2 != 1:
        return "Invalid board size."
    board = []
    for y in range(size):
        board.append([])
        for x in range(size + 5):
            board[-1].append(".")
    return board


def generateoldboard2(sizex, sizey):
    board = []
    for y in range(sizex):
        board.append([])
        for x in range(sizey):
            board[-1].append(".")
    return board


def displayboard2(board):
    tempboard = generateoldboard(board[3])
    currentletter = 'a'
    for eachposition in board[0]:
        x = eachposition[1]
        y = eachposition[0]
        tempboard[x][y] = currentletter
        currentletter = chr(ord(currentletter) + 1)
    remaining = True
    while remaining:
        remaining = False
        checker = False
        for each in tempboard[0]:
            if each != ".":
                checker = True
        if checker == False:
            tempboard.pop(0)
            remaining = True
        checker = False
        for each in tempboard[-1]:
            if each != ".":
                checker = True
        if checker == False:
            tempboard.pop(-1)
            remaining = True
        checker = False
        for eachrow in tempboard:
            if eachrow[0] != ".":
                checker = True
        if checker == False:
            for eachrow in tempboard:
                eachrow.pop(0)
                remaining = True
        checker = False
        for eachrow in tempboard:
            if eachrow[-1] != ".":
                checker = True
        if checker == False:
            for eachrow in tempboard:
                eachrow.pop(-1)
                remaining = True

    return tempboard


def decodemove(movein, x, y):  # up, right first
    translation = [[x, y], [y, x], [y, -x], [x, -y], [-x, -y], [-y, -x], [-y, x], [-x, y]]
    return translation[movein]


def generatejumps(board):
    for each in board[4]:
        move = decodemove(int(each), board[2][0], board[2][1])
        suggestedx = board[1][0] + move[0]
        suggestedy = board[1][1] - move[1]
        if suggestedx > board[3] - 1 or suggestedx < 0 or suggestedy > board[3] - 1 or suggestedy < 0:
            return 0  # error, view too small
        for eachposition in board[0]:
            if eachposition[0] == suggestedx and eachposition[1] == suggestedy:
                return 0  # error, visited square
        board[0].append([suggestedx, suggestedy])
        board[1] = [suggestedx, suggestedy]


# fns that arent related to drawing:

def text_advanced(text, localfont, text_color, xpos, ypos):
    if text_color == "red":
        text_color = (255, 0, 0)
    textimage = localfont.render(text, True, text_color)
    textimagerect = textimage.get_rect()
    textimagerect.center = (xpos, ypos)
    canvas.blit(textimage, textimagerect)
    # no need to return value


def draw_text(text, localfont, text_color, xpos, ypos):
    textimage = localfont.render(text, True, text_color)
    canvas.blit(textimage, (xpos, ypos))
    # no need to return value


def closest_value(input_list, input_value):
    arr = np.asarray(input_list)
    i = (np.abs(arr - input_value)).argmin()
    return arr[i]


def findcursorpos():
    cursorx = cursorpos[0]
    pos = 0
    tempjumplist = copy.copy(visiblejumplist)
    tempjumplist.append(" ")
    candidatepositions = []
    for element in tempjumplist:
        textwidth = 20 + pygame.font.SysFont("Calibri", 20).render("".join(tempjumplist[0:pos]), 1,
                                                                   (0, 0, 0)).get_width()
        candidatepositions.append(textwidth)
        pos += 1
    mindist = 1000
    pos = 0
    for each in candidatepositions:
        if abs(int(each) - int(cursorx)) < mindist:
            mindist = abs(int(each) - int(cursorx))
        pos += 1

    pos = 0
    for each in candidatepositions:
        if abs(int(each) - int(cursorx)) == mindist:
            cursorx = each
            cursorposinlist = pos
        pos += 1
    return [cursorposinlist, cursorx]


# make board
def drawstring(jumpstring, jumpx, jumpy):
    bnum = len(jumpstring) + 1
    myboard = generatenewboard(2 * max(jumpx, jumpy) * (bnum + 1) + 1, [jumpx, jumpy])
    mid = int((2 * max(jumpx, jumpy) * (bnum + 1) + 1 + 1) / 2) - 1
    myboard[4] = str(jumpstring)
    generatejumps(myboard)
    myboard[2] = [mid, mid]
    myboard = displayboard2(myboard)

    shapesize = [len(myboard), len(myboard[0])]
    blockwidth = min(float((width - 100)) / float(shapesize[1]), float((width - 100)) / float(shapesize[0]))
    blockwidth = abs(math.floor(blockwidth))
    leftmargin = (width - (blockwidth * shapesize[1])) / 2
    return [myboard, shapesize, blockwidth, leftmargin]


# initializing vars:
textboxopen = False
cursortimer = 0
cursorblinktimer = 13
visiblejumplist = [char for char in jumpstring]
cursorposinlist = 0
timesinceclick = 0
highlightarea = [0, 0]
highlighting = False
highlightpos = [0, 0]
lastmousestate = False
lastjumplist = []
keypresstimers = [0, 0, 0, 0]  # backspace, delete, left, right
keysdown = [False, False, False, False, False]  # bspace, del, left, right, SHIFT
waitkeypress = 13

# GAME LOOP
while True:
    ignore = False
    values = drawstring("".join(visiblejumplist), jumpx, jumpy)
    myboard = values[0]
    shapesize = values[1]
    blockwidth = values[2]
    leftmargin = values[3]
    pos = 0
    for el in keypresstimers:
        keypresstimers[pos] = keypresstimers[pos] + 1
        pos += 1

    canvas.fill((255, 255, 255))
    text_advanced("Shape Drawing Program", font1, (0, 0, 0), width // 2, 20)
    tempjumplist = copy.copy(visiblejumplist)
    tempjumplist.append(" ")
    keytoadd = ""
    if cursorposinlist > len(visiblejumplist):
        cursorposinlist = len(visiblejumplist)
    for event in pygame.event.get():
        cursorpos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_BACKSPACE:
                keysdown[0] = False
            if event.key == pygame.K_DELETE:
                keysdown[1] = False
            if event.key == pygame.K_LEFT:
                keysdown[2] = False
            if event.key == pygame.K_RIGHT:
                keysdown[3] = False
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                keysdown[4] = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_CTRL:
                if textboxopen and highlightpos[0] != highlightpos[1]:
                    if highlightpos[0] < highlightpos[1]:
                        pos = 0
                        highlightedstring = ""
                        for element in visiblejumplist:
                            if pos >= highlightpos[0] and pos < highlightpos[1]:
                                highlightedstring = highlightedstring + str(visiblejumplist[pos])
                            pos = pos + 1
                        pyperclip.copy(highlightedstring)
                    else:
                        pos = 0
                        highlightedstring = ""
                        for element in visiblejumplist:
                            if pos >= highlightpos[1] and pos < highlightpos[0]:
                                highlightedstring = highlightedstring + str(visiblejumplist[pos])
                            pos = pos + 1
                        pyperclip.copy(highlightedstring)

            if event.key == pygame.K_x and pygame.key.get_mods() & pygame.KMOD_CTRL:
                lastjumplist = copy.copy(visiblejumplist)
                ignore = True
                if textboxopen and highlightpos[0] != highlightpos[1]:
                    if highlightpos[0] < highlightpos[1]:
                        cursorposinlist = highlightpos[0]
                        pos = 0
                        highlightedstring = ""
                        for element in visiblejumplist:
                            if pos >= highlightpos[0] and pos < highlightpos[1]:
                                highlightedstring = highlightedstring + str(visiblejumplist[pos])
                            pos = pos + 1
                        pyperclip.copy(highlightedstring)
                        highlighting = False
                        if highlightpos[0] < highlightpos[1]:
                            visiblejumplist[highlightpos[0]:highlightpos[1]] = []
                        else:
                            visiblejumplist[highlightpos[1]:highlightpos[0]] = []
                        textwidth = 20 + pygame.font.SysFont("Calibri", 20).render(
                            "".join(tempjumplist[0:cursorposinlist]), 1, (0, 0, 0)).get_width()
                        cursorx = textwidth
                        highlightpos = [0, 0]
                        highlightarea = [0, 0]
                    else:
                        cursorposinlist = highlightpos[1]
                        pos = 0
                        highlightedstring = ""
                        for element in visiblejumplist:
                            if pos >= highlightpos[1] and pos < highlightpos[0]:
                                highlightedstring = highlightedstring + str(visiblejumplist[pos])
                            pos = pos + 1
                        pyperclip.copy(highlightedstring)
                        highlighting = False
                        if highlightpos[1] < highlightpos[0]:
                            visiblejumplist[highlightpos[1]:highlightpos[0]] = []
                        else:
                            visiblejumplist[highlightpos[0]:highlightpos[1]] = []
                        textwidth = 20 + pygame.font.SysFont("Calibri", 20).render(
                            "".join(tempjumplist[0:cursorposinlist]), 1, (0, 0, 0)).get_width()
                        cursorx = textwidth
                        highlightpos = [0, 0]
                        highlightarea = [0, 0]

            if event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_CTRL:
                lastjumplist = copy.copy(visiblejumplist)
                stringtoadd = pyperclip.paste()
                validstring = True
                for eachchar in stringtoadd:
                    if eachchar not in ["0", "1", "2", "3", "4", "5", "6", "7"]:
                        validstring = False
                if highlightpos[0] == highlightpos[1] and validstring:
                    keytoadd = stringtoadd
                if highlightpos[1] != highlightpos[0] and validstring:
                    keytoadd = stringtoadd
                    ignore = True
                    highlighting = False
                    if highlightpos[0] < highlightpos[1]:
                        visiblejumplist[highlightpos[0]:highlightpos[1]] = []
                    else:
                        visiblejumplist[highlightpos[1]:highlightpos[0]] = []
                    if highlightpos[1] > highlightpos[0]:
                        cursorposinlist = cursorposinlist - (highlightpos[1] - highlightpos[0])
                    highlightpos = [0, 0]
                    highlightarea = [0, 0]
                    for eachchar in keytoadd:
                        visiblejumplist.insert(cursorposinlist, eachchar)
                        cursorposinlist = cursorposinlist + 1
                        keytoadd = ""
                highlightpos = [0, 0]
                highlightarea = [0, 0]

            if event.key == pygame.K_a and pygame.key.get_mods() & pygame.KMOD_CTRL:
                if textboxopen:
                    textwidth = 20 + pygame.font.SysFont("Calibri", 20).render(
                        "".join(tempjumplist[0:len(visiblejumplist)]), 1, (0, 0, 0)).get_width()
                    cursorx = textwidth

                    highlightpos = [0, len(visiblejumplist)]
                    highlightarea = [20, textwidth]
                    cursorx = textwidth
            if event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:
                if textboxopen:
                    difference = len(visiblejumplist) - len(lastjumplist)
                    cursorposinlist = cursorposinlist - difference
                    visiblejumplist = copy.copy(lastjumplist)
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

            if event.key == pygame.K_BACKSPACE:
                if keysdown[0] == False:
                    keypresstimers[0] = 0
                keysdown[0] = True
                lastjumplist = copy.copy(visiblejumplist)
                if textboxopen and cursorposinlist > 0 and highlightpos[0] - highlightpos[1] == 0:
                    visiblejumplist.pop(cursorposinlist - 1)
                    cursorposinlist = cursorposinlist - 1
                    templist = copy.copy(visiblejumplist)
                    if cursorposinlist < 0: cursorposinlist = 0
                    textwidth = 20 + pygame.font.SysFont("Calibri", 20).render("".join(tempjumplist[0:cursorposinlist]),
                                                                               1, (0, 0, 0)).get_width()
                    cursorx = textwidth
                if highlightpos[0] - highlightpos[1] != 0:
                    highlighting = False
                    if highlightpos[0] < highlightpos[1]:
                        visiblejumplist[highlightpos[0]:highlightpos[1]] = []
                    else:
                        visiblejumplist[highlightpos[1]:highlightpos[0]] = []
                    if highlightpos[1] > highlightpos[0]:
                        cursorposinlist = cursorposinlist - (highlightpos[1] - highlightpos[0])
                    if cursorposinlist < 0: cursorposinlist = 0
                    textwidth = 20 + pygame.font.SysFont("Calibri", 20).render("".join(tempjumplist[0:cursorposinlist]),
                                                                               1, (0, 0, 0)).get_width()
                    cursorx = textwidth

                    highlightpos = [0, 0]
                    highlightarea = [0, 0]

            if event.key == pygame.K_DELETE:
                if keysdown[1] == False:
                    keypresstimers[1] = 0
                keysdown[1] = True
                lastjumplist = copy.copy(visiblejumplist)
                if textboxopen and cursorposinlist < len(tempjumplist) - 1 and highlightpos[0] - highlightpos[1] == 0:
                    visiblejumplist.pop(cursorposinlist)
                if highlightpos[0] - highlightpos[1] != 0:
                    highlighting = False
                    if highlightpos[0] < highlightpos[1]:
                        visiblejumplist[highlightpos[0]:highlightpos[1]] = []
                    else:
                        visiblejumplist[highlightpos[1]:highlightpos[0]] = []
                    if highlightpos[1] > highlightpos[0]:
                        cursorposinlist = cursorposinlist - (highlightpos[1] - highlightpos[0])
                    if cursorposinlist < 0: cursorposinlist = 0
                    textwidth = 20 + pygame.font.SysFont("Calibri", 20).render(
                        "".join(tempjumplist[0:len(visiblejumplist)]), 1, (0, 0, 0)).get_width()
                    cursorx = textwidth

                    highlightpos = [0, 0]
                    highlightarea = [0, 0]
                highlighting = False

            if event.key == pygame.K_RIGHT and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                if keysdown[3] == False:
                    keypresstimers[3] = 0
                keysdown[3] = True
                keysdown[4] = True
                if textboxopen and cursorposinlist < len(tempjumplist) - 1:
                    if highlightpos == [0, 0]:
                        highlightpos = [cursorposinlist, cursorposinlist]

                    cursorposinlist += 1
                    textwidth = 20 + pygame.font.SysFont("Calibri", 20).render(
                        "".join(tempjumplist[0: cursorposinlist]), 1, (0, 0, 0)).get_width()
                    cursorx = textwidth
                    highlightpos[1] += 1
                    highlightarea = [
                        20 + pygame.font.SysFont("Calibri", 20).render("".join(tempjumplist[0: highlightpos[0]]), 1,
                                                                       (0, 0, 0)).get_width(),
                        20 + pygame.font.SysFont("Calibri", 20).render("".join(tempjumplist[0: highlightpos[1]]), 1,
                                                                       (0, 0, 0)).get_width()]


            elif event.key == pygame.K_RIGHT:
                if keysdown[3] == False:
                    keypresstimers[3] = 0
                keysdown[3] = True
                if textboxopen and cursorposinlist < len(tempjumplist) - 1 and highlightpos[0] == highlightpos[1]:
                    cursorposinlist = cursorposinlist + 1
                    highlightpos = [cursorposinlist, cursorposinlist]
                if textboxopen and highlightpos[0] != highlightpos[1]:
                    highlightpos = [max(highlightpos), max(highlightpos)]
                    highlightarea = [max(highlightarea), max(highlightarea)]
                    cursorposinlist = max(highlightpos)

            if event.key == pygame.K_LEFT and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                if keysdown[2] == False:
                    keypresstimers[2] = 0
                keysdown[2] = True
                keysdown[4] = True
                if textboxopen and cursorposinlist > 0:
                    if highlightpos == [0, 0]:
                        highlightpos = [cursorposinlist, cursorposinlist]

                    cursorposinlist = cursorposinlist - 1
                    textwidth = 20 + pygame.font.SysFont("Calibri", 20).render(
                        "".join(tempjumplist[0: cursorposinlist]), 1, (0, 0, 0)).get_width()
                    cursorx = textwidth
                    highlightpos[1] = highlightpos[1] - 1
                    highlightarea = [
                        20 + pygame.font.SysFont("Calibri", 20).render("".join(tempjumplist[0: highlightpos[0]]), 1,
                                                                       (0, 0, 0)).get_width(),
                        20 + pygame.font.SysFont("Calibri", 20).render("".join(tempjumplist[0: highlightpos[1]]), 1,
                                                                       (0, 0, 0)).get_width()]

            elif event.key == pygame.K_LEFT:
                if keysdown[2] == False:
                    keypresstimers[2] = 0
                keysdown[2] = True
                if textboxopen and cursorposinlist > 0 and highlightpos[0] == highlightpos[1]:
                    cursorposinlist = cursorposinlist - 1
                    highlightpos = [cursorposinlist, cursorposinlist]
                if textboxopen and highlightpos[0] != highlightpos[1]:
                    highlightpos = [min(highlightpos), min(highlightpos)]
                    highlightarea = [min(highlightarea), min(highlightarea)]
                    cursorposinlist = min(highlightpos)

            if event.key == pygame.K_UP and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                if textboxopen:
                    if highlightpos == [0, 0]:
                        highlightpos = [cursorposinlist, cursorposinlist]

                    cursorposinlist = 0
                    cursorx = 20

                    highlightpos[1] = 0

                    highlightarea = [
                        20 + pygame.font.SysFont("Calibri", 20).render("".join(tempjumplist[0: highlightpos[0]]), 1,
                                                                       (0, 0, 0)).get_width(),
                        20 + pygame.font.SysFont("Calibri", 20).render("".join(tempjumplist[0: highlightpos[1]]), 1,
                                                                       (0, 0, 0)).get_width()]

            elif event.key == pygame.K_UP:
                if textboxopen and highlightpos[0] == highlightpos[1]:
                    cursorposinlist = 0
                    cursorx = 20
                    highlightpos = [cursorposinlist, cursorposinlist]
                if textboxopen and highlightpos[0] != highlightpos[1]:
                    highlightpos = [0, 0]
                    highlightarea = [0, 0]
                    cursorposinlist = 0

            if event.key == pygame.K_DOWN and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                if textboxopen:
                    ignore = True
                    if highlightpos == [0, 0]:
                        highlightpos = [cursorposinlist, cursorposinlist]

                    cursorposinlist = len(tempjumplist) - 1
                    cursorx = 20 + pygame.font.SysFont("Calibri", 20).render("".join(tempjumplist[0: cursorposinlist]),
                                                                             1, (0, 0, 0)).get_width()

                    highlightpos[1] = len(tempjumplist) - 1

                    highlightarea = [
                        20 + pygame.font.SysFont("Calibri", 20).render("".join(tempjumplist[0: highlightpos[0]]), 1,
                                                                       (0, 0, 0)).get_width(),
                        20 + pygame.font.SysFont("Calibri", 20).render("".join(tempjumplist[0: highlightpos[1]]), 1,
                                                                       (0, 0, 0)).get_width()]

            elif event.key == pygame.K_DOWN:
                if textboxopen and highlightpos[0] == highlightpos[1]:
                    cursorposinlist = len(tempjumplist) - 1
                    highlightpos = [cursorposinlist, cursorposinlist]
                if textboxopen and highlightpos[0] != highlightpos[1]:
                    highlightpos = [0, 0]
                    highlightarea = [0, 0]
                    cursorposinlist = len(visiblejumplist)

            if len(visiblejumplist) < 40 and textboxopen:
                if event.key == pygame.K_0 or event.key == pygame.K_KP0: keytoadd = ["0"]
                if event.key == pygame.K_1 or event.key == pygame.K_KP1: keytoadd = ["1"]
                if event.key == pygame.K_2 or event.key == pygame.K_KP2: keytoadd = ["2"]
                if event.key == pygame.K_3 or event.key == pygame.K_KP3: keytoadd = ["3"]
                if event.key == pygame.K_4 or event.key == pygame.K_KP4: keytoadd = ["4"]
                if event.key == pygame.K_5 or event.key == pygame.K_KP5: keytoadd = ["5"]
                if event.key == pygame.K_6 or event.key == pygame.K_KP6: keytoadd = ["6"]
                if event.key == pygame.K_7 or event.key == pygame.K_KP7: keytoadd = ["7"]

        mousestate = pygame.mouse.get_pressed()
    if keysdown[0] or keysdown[1] or keysdown[2] or keysdown[3]:
        cursortimer = 13
    if keytoadd != "":
        lastjumplist = copy.copy(visiblejumplist)
        for eachchar in keytoadd:
            visiblejumplist.insert(cursorposinlist, eachchar)
            cursorposinlist = cursorposinlist + 1
    if textboxopen and highlightpos[1] != highlightpos[0] + len(visiblejumplist) and ignore == False:
        textwidth = 20 + pygame.font.SysFont("Calibri", 20).render("".join(tempjumplist[0:cursorposinlist]), 1,
                                                                   (0, 0, 0)).get_width()
        cursorx = textwidth
    timesinceclick += 1
    if highlighting and mousestate[0] == False:
        highlighting = False

    # holding key code \/
    if keypresstimers[0] > waitkeypress and keypresstimers[0] % 2 == 0 and keysdown[0] and textboxopen and keysdown[
        1] == False and keysdown[2] == False and keysdown[3] == False:
        lastjumplist = copy.copy(visiblejumplist)
        if textboxopen and cursorposinlist > 0 and highlightpos[0] - highlightpos[1] == 0:
            visiblejumplist.pop(cursorposinlist - 1)
            cursorposinlist = cursorposinlist - 1
            templist = copy.copy(visiblejumplist)
            if cursorposinlist < 0: cursorposinlist = 0
            textwidth = 20 + pygame.font.SysFont("Calibri", 20).render("".join(tempjumplist[0:cursorposinlist]), 1,
                                                                       (0, 0, 0)).get_width()
            cursorx = textwidth
            if highlightpos[0] - highlightpos[1] != 0:
                highlighting = False
                if highlightpos[0] < highlightpos[1]:
                    visiblejumplist[highlightpos[0]:highlightpos[1]] = []
                else:
                    visiblejumplist[highlightpos[1]:highlightpos[0]] = []
                if highlightpos[1] > highlightpos[0]:
                    cursorposinlist = cursorposinlist - (highlightpos[1] - highlightpos[0])
                if cursorposinlist < 0: cursorposinlist = 0
                textwidth = 20 + pygame.font.SysFont("Calibri", 20).render("".join(tempjumplist[0:cursorposinlist]), 1,
                                                                           (0, 0, 0)).get_width()
                cursorx = textwidth
                highlightpos = [0, 0]
                highlightarea = [0, 0]

    if keypresstimers[1] > waitkeypress and keypresstimers[1] % 2 == 0 and keysdown[1] and textboxopen and keysdown[
        0] == False and keysdown[2] == False and keysdown[3] == False:
        lastjumplist = copy.copy(visiblejumplist)
        if textboxopen and cursorposinlist < len(tempjumplist) - 1 and highlightpos[0] - highlightpos[1] == 0:
            visiblejumplist.pop(cursorposinlist)
            if highlightpos[0] - highlightpos[1] != 0:
                highlighting = False
                if highlightpos[0] < highlightpos[1]:
                    visiblejumplist[highlightpos[0]:highlightpos[1]] = []
                else:
                    visiblejumplist[highlightpos[1]:highlightpos[0]] = []
                if highlightpos[1] > highlightpos[0]:
                    cursorposinlist = cursorposinlist - (highlightpos[1] - highlightpos[0])
                if cursorposinlist < 0: cursorposinlist = 0
                textwidth = 20 + pygame.font.SysFont("Calibri", 20).render(
                    "".join(tempjumplist[0:len(visiblejumplist)]), 1, (0, 0, 0)).get_width()
                cursorx = textwidth

                highlightpos = [0, 0]
                highlightarea = [0, 0]
        highlighting = False

    if keypresstimers[2] > waitkeypress and keypresstimers[2] % 2 == 0 and keysdown[2] and textboxopen and keysdown[
        4] == False and keysdown[0] == False and keysdown[1] == False and keysdown[3] == False:
        if textboxopen and cursorposinlist > 0 and highlightpos[0] == highlightpos[1]:
            cursorposinlist = cursorposinlist - 1
            highlightpos = [cursorposinlist, cursorposinlist]
        if textboxopen and highlightpos[0] != highlightpos[1]:
            highlightpos = [min(highlightpos), min(highlightpos)]
            highlightarea = [min(highlightarea), min(highlightarea)]
            cursorposinlist = min(highlightpos)

    if keypresstimers[3] > waitkeypress and keypresstimers[3] % 2 == 0 and keysdown[3] and textboxopen and keysdown[
        4] == False and keysdown[0] == False and keysdown[1] == False and keysdown[2] == False:
        if textboxopen and cursorposinlist < len(tempjumplist) - 1 and highlightpos[0] == highlightpos[1]:
            cursorposinlist = cursorposinlist + 1
            highlightpos = [cursorposinlist, cursorposinlist]
        if textboxopen and highlightpos[0] != highlightpos[1]:
            highlightpos = [max(highlightpos), max(highlightpos)]
            highlightarea = [max(highlightarea), max(highlightarea)]
            cursorposinlist = max(highlightpos)

    if keypresstimers[2] > waitkeypress and keypresstimers[2] % 2 == 0 and keysdown[2] and textboxopen and keysdown[
        4] and keysdown[0] == False and keysdown[1] == False and keysdown[3] == False:
        if textboxopen and cursorposinlist > 0:
            if highlightpos == [0, 0]:
                highlightpos = [cursorposinlist, cursorposinlist]

            cursorposinlist = cursorposinlist - 1
            textwidth = 20 + pygame.font.SysFont("Calibri", 20).render("".join(tempjumplist[0: cursorposinlist]), 1,
                                                                       (0, 0, 0)).get_width()
            cursorx = textwidth
            highlightpos[1] = highlightpos[1] - 1
            highlightarea = [
                20 + pygame.font.SysFont("Calibri", 20).render("".join(tempjumplist[0: highlightpos[0]]), 1,
                                                               (0, 0, 0)).get_width(),
                20 + pygame.font.SysFont("Calibri", 20).render("".join(tempjumplist[0: highlightpos[1]]), 1,
                                                               (0, 0, 0)).get_width()]
    if keypresstimers[3] > waitkeypress and keypresstimers[3] % 2 == 0 and keysdown[3] and textboxopen and keysdown[
        4] and keysdown[0] == False and keysdown[1] == False and keysdown[2] == False:
        if textboxopen and cursorposinlist < len(tempjumplist) - 1:
            if highlightpos == [0, 0]:
                highlightpos = [cursorposinlist, cursorposinlist]

            cursorposinlist += 1
            textwidth = 20 + pygame.font.SysFont("Calibri", 20).render("".join(tempjumplist[0: cursorposinlist]), 1,
                                                                       (0, 0, 0)).get_width()
            cursorx = textwidth
            highlightpos[1] += 1
            highlightarea = [
                20 + pygame.font.SysFont("Calibri", 20).render("".join(tempjumplist[0: highlightpos[0]]), 1,
                                                               (0, 0, 0)).get_width(),
                20 + pygame.font.SysFont("Calibri", 20).render("".join(tempjumplist[0: highlightpos[1]]), 1,
                                                               (0, 0, 0)).get_width()]

    # draw blocks
    currentpos = [leftmargin, 50]
    for eachrow in myboard:
        for eachblock in eachrow:
            if eachblock != ".":
                pygame.draw.rect(canvas, (120, 120, 120), (currentpos[0], currentpos[1], blockwidth, blockwidth))
                if blockwidth > 12:
                    text_advanced(eachblock, pygame.font.SysFont('Nunito', min(blockwidth // 2, blockwidth - 2)),
                                  (255, 255, 255), currentpos[0] + blockwidth / 2, currentpos[1] + blockwidth / 2)
            currentpos[0] += blockwidth
        currentpos[1] += blockwidth
        currentpos[0] = leftmargin
    currentpos = [leftmargin, 50]
    bottomright = [width - leftmargin, 50 + len(myboard) * blockwidth]
    while currentpos[1] < bottomright[1] + 0.1:
        pygame.draw.line(canvas, (0, 0, 0), (currentpos[0], currentpos[1]), (bottomright[0], currentpos[1]), 1)
        currentpos[1] += blockwidth
    currentpos[1] = 50

    while currentpos[0] < bottomright[0] + 0.1:
        pygame.draw.line(canvas, (0, 0, 0), (currentpos[0], currentpos[1]), (currentpos[0], bottomright[1]), 1)
        currentpos[0] += blockwidth

    # Textbox for jumpstring input
    if len(visiblejumplist) >= 39:
        text_advanced("Max string length reached.", pygame.font.SysFont("Calibri", 20), (255, 1, 1), 225, 480)
        visiblejumplist = visiblejumplist[0:39]
    text_advanced("Jump String:", pygame.font.SysFont("Calibri", 20), (0, 0, 0), 65, 480)
    if cursorpos[0] > 12 and cursorpos[0] < width - 13 and cursorpos[1] > 492 and cursorpos[1] < 522:  # switch
        mousetype = "IBEAM"

        if mousestate[0]:
            textboxopen = True
            cursortimer = cursorblinktimer * 1
            cursorposcurrent = findcursorpos()
            cursorposinlist = cursorposcurrent[0]
            cursorx = cursorposcurrent[1]
            if highlighting == False:
                highlighting = True
                highlightarea[0] = cursorx
                highlightpos[0] = cursorposinlist



    else:
        mousetype = "POINTER"
        if mousestate[0]:
            textboxopen = False

    if highlighting:
        cursorposcurrent = findcursorpos()
        cursorx = cursorposcurrent[1]
        if highlightarea != [0, 0]:
            highlightarea[1] = cursorx
        highlightpos[1] = cursorposinlist

    if textboxopen == False:
        pygame.draw.rect(canvas, (0, 0, 0), (13, 492, width - 26, 30), 1)
    else:
        pygame.draw.rect(canvas, (10, 30, 250), (13, 492, width - 26, 30), 2)

    # text stuff in textbox

    if textboxopen:
        cursortimer += 1
    if highlightarea != [0, 0]:
        pygame.draw.rect(canvas, (100, 100, 255), (highlightarea[0], 496, highlightarea[1] - highlightarea[0], 22))
        pygame.draw.rect(canvas, (100, 100, 255), (highlightarea[1], 496, highlightarea[0] - highlightarea[1], 22))

    textwidth = 21 + pygame.font.SysFont("Calibri", 20).render("".join(visiblejumplist), 1,
                                                               (0, 0, 0)).get_width()  # total text width
    if cursortimer > cursorblinktimer and cursortimer < 2.5 * cursorblinktimer and textboxopen:
        pygame.draw.line(canvas, (0, 0, 0), (cursorx, 498), (cursorx, 516))
    if cursortimer > 2.5 * cursorblinktimer:
        cursortimer = 0
    if textboxopen == False:
        pygame.draw.rect(canvas, (255, 255, 255), (15, 494, width - 119 - 4, 30 - 4))

    draw_text("".join(visiblejumplist), pygame.font.SysFont("Calibri", 20), (0, 0, 0), 20, 499)

    onbutton = False
    # \/ x and y jump stuff
    text_advanced("Jump X:", pygame.font.SysFont("Calibri", 20), (0, 0, 0), 47, 547)
    pygame.draw.rect(canvas, (0, 0, 0), (105, 531, 40, 30), 1)
    text_advanced(str(jumpx), pygame.font.SysFont("Calibri", 20), (0, 0, 0), 125, 547)
    pygame.draw.rect(canvas, (0, 0, 0), (90, 536, 16, 20), 1)
    pygame.draw.rect(canvas, (0, 0, 0), (144, 536, 16, 20), 1)
    pygame.draw.line(canvas, (0, 0, 0), (96, 546), (100, 542))
    pygame.draw.line(canvas, (0, 0, 0), (96, 546), (100, 550))
    pygame.draw.line(canvas, (0, 0, 0), (100, 542), (100, 550))
    pygame.draw.line(canvas, (0, 0, 0), (154, 546), (150, 542))
    pygame.draw.line(canvas, (0, 0, 0), (154, 546), (150, 550))
    pygame.draw.line(canvas, (0, 0, 0), (150, 542), (150, 550))

    text_advanced("Jump Y:", pygame.font.SysFont("Calibri", 20), (0, 0, 0), 47 + width // 2, 547)
    pygame.draw.rect(canvas, (0, 0, 0), (width // 2 + 105, 531, 40, 30), 1)
    text_advanced(str(jumpy), pygame.font.SysFont("Calibri", 20), (0, 0, 0), width // 2 + 125, 547)
    pygame.draw.rect(canvas, (0, 0, 0), (width // 2 + 90, 536, 16, 20), 1)
    pygame.draw.rect(canvas, (0, 0, 0), (width // 2 + 144, 536, 16, 20), 1)
    pygame.draw.line(canvas, (0, 0, 0), (width // 2 + 96, 546), (width // 2 + 100, 542))
    pygame.draw.line(canvas, (0, 0, 0), (width // 2 + 96, 546), (width // 2 + 100, 550))
    pygame.draw.line(canvas, (0, 0, 0), (width // 2 + 100, 542), (width // 2 + 100, 550))
    pygame.draw.line(canvas, (0, 0, 0), (width // 2 + 154, 546), (width // 2 + 150, 542))
    pygame.draw.line(canvas, (0, 0, 0), (width // 2 + 154, 546), (width // 2 + 150, 550))
    pygame.draw.line(canvas, (0, 0, 0), (width // 2 + 150, 542), (width // 2 + 150, 550))

    if cursorpos[0] > 90 and cursorpos[0] < 106 and cursorpos[1] > 536 and cursorpos[1] < 556:
        mousetype = "HAND"
        if mousestate[0] and jumpx > 0 and lastmousestate == False:
            jumpx = jumpx - 1
        if mousestate[0] and jumpx == 0 and lastmousestate == False:
            jumpx = maxjumplength
    elif cursorpos[0] > 144 and cursorpos[0] < 166 and cursorpos[1] > 536 and cursorpos[1] < 556:
        mousetype = "HAND"
        if mousestate[0] and jumpx < maxjumplength and lastmousestate == False:
            jumpx = jumpx + 1
        if mousestate[0] and jumpx == maxjumplength and lastmousestate == False:
            jumpx = 0
    elif cursorpos[0] > width // 2 + 90 and cursorpos[0] < width // 2 + 106 and cursorpos[1] > 536 and cursorpos[
        1] < 556:
        mousetype = "HAND"
        if mousestate[0] and jumpy > 0 and lastmousestate == False:
            jumpy = jumpy - 1
        if mousestate[0] and jumpy == 0 and lastmousestate == False:
            jumpy = maxjumplength
    elif cursorpos[0] > width // 2 + 144 and cursorpos[0] < width // 2 + 166 and cursorpos[1] > 536 and cursorpos[
        1] < 556:
        mousetype = "HAND"
        if mousestate[0] and jumpy < maxjumplength and lastmousestate == False:
            jumpy = jumpy + 1
        if mousestate[0] and jumpy == maxjumplength and lastmousestate == False:
            jumpy = 0

    if mousetype == "IBEAM":
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)
    elif mousetype == "HAND":
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    # \/ borders
    pygame.draw.line(canvas, (0, 0, 0), (width, 0), (width, height))
    pygame.draw.line(canvas, (0, 0, 0), (0, 0), (realwidth, 0))
    pygame.draw.line(canvas, (0, 0, 0), (0, 37), (width, 37))
    pygame.draw.line(canvas, (0, 0, 0), (0, 463), (width, 463))
    pygame.draw.line(canvas, (0, 0, 0), (0, height), (realwidth, height))
    pygame.draw.line(canvas, (0, 0, 0), (0, 0), (0, height))
    pygame.draw.line(canvas, (0, 0, 0), (realwidth, 0), (realwidth, height))

    # Framework
    lastmousestate = mousestate[0]
    pygame.display.update()
    FramePerSec.tick(30)
# end of gameloop


input("Done!")
