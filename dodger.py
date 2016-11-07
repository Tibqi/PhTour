import pygame, random, sys, json
from pygame.locals import *
from settings import * # import constant variables from separate settings file

def terminate(topScore, musicPlaying):
    topScoreJs = json.dumps(topScore)
    musicPlayingJs = json.dumps(musicPlaying)
    with open('savegame.txt', 'w') as saveFile:
        saveFile.write(topScoreJs + '\n')
        saveFile.write(musicPlayingJs)
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey(topScore, musicPlaying):
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate(topScore, musicPlaying)
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate(topScore, musicPlaying)
                return

def playerHasHitBaddie(playerRect, baddies):
    for b in baddies:
        if playerRect.colliderect(b['rect']):
            return True
    return False

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def loadSavedSetting():
    savedVariables = []
    try:
        with open('savegame.txt', 'r') as saveFile:
            for line in saveFile:
                savedVariables.append(line)
        topScore = json.loads(savedVariables[0])
        musicPlaying = json.loads(savedVariables[1])
        error = 0 # will be used later to show error message in the menu
    except (FileNotFoundError, IndexError):
        topScore = 0
        musicPlaying = True
        error = 1
    return topScore, musicPlaying, error

# set up pygame, the window, and the mouse cursor
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Dodger')
pygame.mouse.set_visible(True)

# set up fonts
font = pygame.font.SysFont(None, 48)

# set up sounds
gameOverSound = pygame.mixer.Sound('gameover.wav')
pygame.mixer.music.load('background.ogg')

# set up images
playerImage = pygame.image.load('player.png').convert()
playerRect = playerImage.get_rect()
baddieImage = pygame.image.load('baddie.png').convert()
soundIcon = pygame.Rect((WINDOWWIDTH - 44), 20, 24, 24)
soundIconImageOn = pygame.image.load('LoudL_24px.png')
soundIconImageOff = pygame.image.load('MuteL_24px.png')

# set up the start menu
# show title
drawText('Dodger', font, windowSurface, (WINDOWWIDTH / 2) - 50, (WINDOWHEIGHT / 4))
drawText('Press the button to start', font, windowSurface, (WINDOWWIDTH / 4) - 40, (WINDOWHEIGHT / 4) + 50)

# show start game button
menuFont = pygame.font.SysFont(None, 20)
menuText = menuFont.render('Start game', 1, BACKGROUNDCOLOR, TEXTCOLOR)
menuRect = menuText.get_rect()
menuRect.centerx = windowSurface.get_rect().centerx
menuRect.centery = windowSurface.get_rect().centery
button = pygame.Rect(menuRect.left - 5, menuRect.top - 5, menuRect.width + 10, menuRect.height + 10)
pygame.draw.rect(windowSurface, TEXTCOLOR, button) # maybe with freetype.font padding?
windowSurface.blit(menuText, menuRect)

# update display
pygame.display.update()

# load saved scores and sound setting
topScore, musicPlaying, error = loadSavedSetting()

# set up variables for the menu
startGame = 0 # set to 1 when clicking on the start menu button
menuActive = False
# menu loop
while 1:
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate(topScore, musicPlaying)
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                terminate(topScore, musicPlaying)
        if event.type == MOUSEBUTTONUP:
            if button.collidepoint(event.pos[0], event.pos[1]):
                startGame = 1
                # ide jön még valami button push effect pl. deflate with 1 pixel, esetleg szín váltás?

    if button.collidepoint(pygame.mouse.get_pos()) and not menuActive:
        menuActive = True
        activeMenu = pygame.Surface((button.width, button.height))
        activeMenu.fill((251,51,0))
        activeMenu.set_alpha(50)
        windowSurface.blit(activeMenu, button)
    elif not button.collidepoint(pygame.mouse.get_pos()):
        menuActive = False
        pygame.draw.rect(windowSurface, TEXTCOLOR, button) # maybe with freetype.font padding?
        windowSurface.blit(menuText, menuRect)

    if startGame:
        break

    pygame.display.update(button)
    mainClock.tick(FPS)

while True:
    # set up the start of the game
    pygame.mouse.set_visible(False)
    baddies = []
    score = 0
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    baddieAddCounter = 0
    if musicPlaying:
        pygame.mixer.music.play(-1, 0.0)

    while True: # the game loop runs while the game part is playing
        score += 1 # increase score

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate(topScore, musicPlaying)

            if event.type == KEYDOWN:
                if event.key == ord('z'):
                    reverseCheat = True
                if event.key == ord('x'):
                    slowCheat = True
                if event.key == ord('p'):
                    drawText('PAUSED', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
                    drawText('Press a key to continue.', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3) + 50)
                    pygame.display.update()
                    waitForPlayerToPressKey(topScore, musicPlaying)
                if event.key == K_LEFT or event.key == ord('a'):
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveRight = True
                    moveLeft = False
                if event.key == K_UP or event.key == ord('w'):
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == ord('s'):
                    moveDown = True
                    moveUp = False
                if event.key == ord('m'):
                    if musicPlaying:
                        pygame.mixer.music.stop()
                    else:
                        pygame.mixer.music.play(-1, 0.0)
                    musicPlaying = not musicPlaying

            if event.type == KEYUP:
                if event.key == ord('z'):
                    reverseCheat = False
                    score = 0
                if event.key == ord('x'):
                    slowCheat = False
                    score = 0
                if event.key == K_ESCAPE:
                    terminate(topScore, musicPlaying)
                if event.key == K_LEFT or event.key == ord('a'):
                    moveLeft = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveRight = False
                if event.key == K_UP or event.key == ord('w'):
                    moveUp = False
                if event.key == K_DOWN or event.key == ord('s'):
                    moveDown = False

            if event.type == MOUSEMOTION:
                # If the mouse moves, move the player where the cursor is.
                playerRect.move_ip(event.pos[0] - playerRect.centerx, event.pos[1] - playerRect.centery)

        # Add new baddies at the top of the screen, if needed.
        if not reverseCheat and not slowCheat:
            baddieAddCounter += 1
        if baddieAddCounter == ADDNEWBADDIERATE:
            baddieAddCounter = 0
            baddieSize = random.randint(BADDIEMINSIZE, BADDIEMAXSIZE)
            newBaddie = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH-baddieSize), 0 - (baddieSize * 2), baddieSize, (baddieSize * 2)),
                         'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                         'surface':pygame.transform.scale(baddieImage, (baddieSize, (baddieSize * 2))),
                        }

            baddies.append(newBaddie)

        # Move the player around.
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1*PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE,0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0,-1*PLAYERMOVERATE)
        if moveDown and playerRect.bottom < WINDOWHEIGHT:
            playerRect.move_ip(0,PLAYERMOVERATE)

        # Move the mouse cursor to match the player.
        pygame.mouse.set_pos(playerRect.centerx, playerRect.centery)

        # Move the baddies down.
        for b in baddies:
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(0, b['speed'])
            elif reverseCheat:
                b['rect'].move_ip(0, -5)
            elif slowCheat:
                b['rect'].move_ip(0, 1)

        # Delete baddies that have fallen past the bottom.
        for b in baddies[:]:
            if b['rect'].top > WINDOWHEIGHT:
                baddies.remove(b)

        # Draw the game world on the window.
        windowSurface.fill(BACKGROUNDCOLOR)

        # Draw the score and top score.
        drawText('Score: %s' % (score), font, windowSurface, 10, 0)
        drawText('Top score: %s' % (topScore), font, windowSurface, 10, 40)

        # Draw the player's rectangle
        windowSurface.blit(playerImage, playerRect)

        # Draw each baddie
        for b in baddies:
            windowSurface.blit(b['surface'], b['rect'])

        # Draw sound icon
        if musicPlaying:
            windowSurface.blit(soundIconImageOn, soundIcon)
        else:
            windowSurface.blit(soundIconImageOff, soundIcon)

        pygame.display.update()

        # Check if any of the baddies have hit the player.
        if playerHasHitBaddie(playerRect, baddies):
            if score > topScore:
                topScore = score # set new top score
            break

        mainClock.tick(FPS)

    # Stop the game and show the "Game Over" screen.
    pygame.mixer.music.stop()
    if musicPlaying:
        gameOverSound.play()

    drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
    drawText('Press a key to play again.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)
    pygame.display.update()
    waitForPlayerToPressKey(topScore, musicPlaying)

    gameOverSound.stop()
