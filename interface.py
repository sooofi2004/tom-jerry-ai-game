import pygame
from algorithms.dfsAlgorithm import DepthAlgorithm
from algorithms.bfsAlgorithm import AmplitudeAlgorithm
from algorithms.costAlgorithm import CostAlgorithm
from algorithms.greedyAlgorithm import GreedyAlgorithm
from algorithms.AstarAlgorithm import StarAlgorithm
import sys

BLACK = (0, 0, 0)
YELLOW = (255, 205, 104)
WHITE = (255, 255, 255)  # FREE 0
BROWN = (139, 69, 19)  # BLOCK 1

algorithm = None


class Interface:

    def __init__(self, initWorld):
        self.__initWorld = initWorld
        self.__solutionWorlds = None
        self.__imgTom = None
        self.__imgJerry = None
        self.__imgTomAndJerry = None
        self.__width = initWorld.shape[0]
        self.__height = initWorld.shape[1]
        self.__margin = 510 / (10 * self.__width + 1)
        self.__lengthcell = self.__margin * 9
        self.__heightcell = self.__margin * 9

    def setSolutionWorld(self, newSolutionWorlds):
        self.__solutionWorlds = newSolutionWorlds

    def loadImages(self):
        self.__imgTom = pygame.image.load("images/Tom.png").convert()
        self.__imgJerry = pygame.image.load(
            "images/Jerry.png").convert()
        self.__imgTomAndJerry = pygame.image.load(
            "images/Tom&Jerry.jpg").convert()

    def showText(self, pantalla, fuente, texto, color, dimensiones, x, y):
        tipo_letra = pygame.font.Font(fuente, dimensiones)
        superficie = tipo_letra.render(texto, True, color)
        rectangulo = superficie.get_rect()
        rectangulo.center = (x, y)
        pantalla.blit(superficie, rectangulo)

    def showComputingTime(self, screen, algorithm):
        computingTime = algorithm.getComputingTime()
        self.showText(screen, pygame.font.match_font(
            'arial'), computingTime, WHITE, 35, 655, 230)

    def interfaceSolution(self, press, grid, i, screen, clock):
        while not press:
            # prueba para boton
            pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # draw the grid
            for row in range(self.__width):
                for column in range(self.__height):
                    if (grid[row, column] != 1 and grid[row, column] != 2 ):
                        color = WHITE
                        pygame.draw.rect(screen,
                                         color,
                                         [(self.__margin+self.__lengthcell) * column + self.__margin,
                                          (self.__margin+self.__heightcell) *
                                          row + self.__margin,
                                          self.__lengthcell,
                                          self.__heightcell])
                    if grid[row, column] == 1:
                        color = BROWN
                        pygame.draw.rect(screen,
                                         color,
                                         [(self.__margin+self.__lengthcell) * column + self.__margin,
                                          (self.__margin+self.__heightcell) *
                                          row + self.__margin,
                                          self.__lengthcell,
                                          self.__heightcell])

                    if grid[row, column] == 2:
                        imagen_redimensionada = pygame.transform.scale(
                            self.__imgTom, (self.__lengthcell, self.__heightcell))
                        screen.blit(imagen_redimensionada, [(self.__margin+self.__lengthcell) * column + self.__margin,
                                                            (self.__margin+self.__heightcell) *
                                                            row + self.__margin,
                                                            self.__lengthcell,
                                                            self.__heightcell])

                    if grid[row, column] == 6:
                        imagen_redimensionada = pygame.transform.scale(
                            self.__imgJerry, (self.__lengthcell, self.__heightcell))
                        screen.blit(imagen_redimensionada, [(self.__margin+self.__lengthcell) * column + self.__margin,
                                                            (self.__margin+self.__heightcell) *
                                                            row + self.__margin,
                                                            self.__lengthcell,
                                                            self.__heightcell])
                    if grid[row, column] == 8:
                        imagen_redimensionada = pygame.transform.scale(
                            self.__imgTomAndJerry, (self.__lengthcell, self.__heightcell))
                        screen.blit(imagen_redimensionada, [(self.__margin+self.__lengthcell) * column + self.__margin,
                                                            (self.__margin+self.__heightcell) *
                                                            row + self.__margin,
                                                            self.__lengthcell,
                                                            self.__heightcell])

         # limit to 1 frames per second.
            clock.tick(5)

        # check that the length is not exceeded
            if (not (i >= len(self.__solutionWorlds))):
                # update world
                grid = self.__solutionWorlds[i]
                i += 1
            elif (i == len(self.__solutionWorlds)):
                sonido_fondo = pygame.mixer.Sound("music/fondo.wav")
                pygame.mixer.Sound.play(sonido_fondo)
                i += 1
                press = True

        # advance and update the screen with what we have drawn.
            pygame.display.flip()

        # Close
        # pygame.quit()

    def showInterface(self):
        # Initialize pygame
        pygame.init()

        # music
        pygame.mixer.init()

        # Set the length and width of the screen
        WINDOW_DIMENSION = [800, 510]  # 510,510
        screen = pygame.display.set_mode(WINDOW_DIMENSION)

        # iterate until the user presses the exit button.
        press = False

        # use it to set how fast the screen refreshes.
        clock = pygame.time.Clock()

        i = 1
        self.loadImages()
        grid = self.__initWorld

        # Set the screen background.
        screen.fill(BLACK)

        pygame.display.set_caption("Tom & Jerry")

        self.showCaptions(screen)

        for row in range(self.__width):
            for column in range(self.__height):
                if (grid[row, column] != 1 and grid[row, column] != 2 and grid[row, column] != 6):
                    color = WHITE
                    pygame.draw.rect(screen,
                                     color,
                                     [(self.__margin+self.__lengthcell) * column + self.__margin,
                                      (self.__margin+self.__heightcell) * row + self.__margin,
                                      self.__lengthcell,
                                      self.__heightcell])
                if grid[row, column] == 1:
                    color = BROWN
                    pygame.draw.rect(screen,
                                     color,
                                     [(self.__margin+self.__lengthcell) * column + self.__margin,
                                      (self.__margin+self.__heightcell) * row + self.__margin,
                                      self.__lengthcell,
                                      self.__heightcell])
                if grid[row, column] == 2:

                    imagen_redimensionada = pygame.transform.scale(
                        self.__imgTom, (self.__lengthcell, self.__heightcell))
                    screen.blit(imagen_redimensionada, [(self.__margin+self.__lengthcell) * column + self.__margin,
                                                        (self.__margin+self.__heightcell) *
                                                        row + self.__margin,
                                                        self.__lengthcell,
                                                        self.__heightcell])


                if grid[row, column] == 6:
                    imagen_redimensionada = pygame.transform.scale(
                        self.__imgJerry, (self.__lengthcell, self.__heightcell))
                    screen.blit(imagen_redimensionada, [(self.__margin+self.__lengthcell) * column + self.__margin,
                                                        (self.__margin+self.__heightcell) *
                                                        row + self.__margin,
                                                        self.__lengthcell,
                                                        self.__heightcell])

                if grid[row, column] == 8:
                    imagen_redimensionada = pygame.transform.scale(
                        self.__imgTomAndJerry, (self.__lengthcell, self.__heightcell))
                    screen.blit(imagen_redimensionada, [(self.__margin+self.__lengthcell) * column + self.__margin,
                                                        (self.__margin+self.__heightcell) *
                                                        row + self.__margin,
                                                        self.__lengthcell,
                                                        self.__heightcell])

        pygame.display.flip()
        # --------Main Program Loop-----------
        while not press:
            # prueba para boton
            pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pos[0] > 598 and pos[0] < 713 and pos[1] > 8 and pos[1] < 29:
                        print("BFS")
                        screen.fill(BLACK)
                        self.showCaptions(screen)
                        # Set the title of the screen.
                        pygame.display.set_caption("Tom using BFS algorithm")
                        self.showText(screen, pygame.font.match_font(
                            'arial'), "BFS", YELLOW, 35, 655, 20)
                        algorithm = AmplitudeAlgorithm(self.__initWorld)
                        solution = algorithm.start()
                        solutionWorld = solution[0]
                        nodeExpanded = solution[1]
                        depth = solution[2]
                        self.showComputingTime(screen, algorithm)
                        self.showText(screen, pygame.font.match_font(
                            'arial'), str(nodeExpanded), WHITE, 35, 655, 295)
                        self.setSolutionWorld(solutionWorld)
                        self.showText(screen, pygame.font.match_font(
                            'arial'), str(depth), WHITE, 35, 655, 355)
                        self.setSolutionWorld(solutionWorld)
                        self.interfaceSolution(press, grid, i, screen, clock)
                    elif pos[0] > 581 and pos[0] < 732 and pos[1] > 42 and pos[1] < 62:
                        print("DFS")
                        screen.fill(BLACK)
                        self.showCaptions(screen)
                        # Set the title of the screen.
                        pygame.display.set_caption("Tom using DFS")
                        self.showText(screen, pygame.font.match_font(
                            'arial'), "DFS", YELLOW, 35, 655, 50)
                        algorithm = DepthAlgorithm(self.__initWorld)
                        solution = algorithm.start()
                        solutionWorld = solution[0]
                        nodeExpanded = solution[1]
                        depth = solution[2]
                        self.showComputingTime(screen, algorithm)
                        self.showText(screen, pygame.font.match_font(
                            'arial'), str(nodeExpanded), WHITE, 35, 655, 295)
                        self.showText(screen, pygame.font.match_font(
                            'arial'), str(depth), WHITE, 35, 655, 355)
                        self.setSolutionWorld(solutionWorld)
                        self.interfaceSolution(press, grid, i, screen, clock)
                    elif pos[0] > 618 and pos[0] < 692 and pos[1] > 70 and pos[1] < 90:
                        print("UCS")
                        screen.fill(BLACK)
                        self.showCaptions(screen)
                        # Set the title of the screen.
                        pygame.display.set_caption("Tom using UCS")
                        self.showText(screen, pygame.font.match_font(
                            'arial'), "UCS", YELLOW, 35, 655, 80)
                        algorithm = CostAlgorithm(self.__initWorld)
                        solution = algorithm.start()
                        solutionWorld = solution[0]
                        nodeExpanded = solution[1]
                        depth = solution[2]
                        self.showComputingTime(screen, algorithm)
                        self.showText(screen, pygame.font.match_font(
                            'arial'), str(nodeExpanded), WHITE, 35, 655, 295)
                        self.showText(screen, pygame.font.match_font(
                            'arial'), str(depth), WHITE, 35, 655, 355)
                        self.setSolutionWorld(solutionWorld)
                        self.interfaceSolution(press, grid, i, screen, clock)
                    elif pos[0] > 619 and pos[0] < 692 and pos[1] > 101 and pos[1] < 123:
                        print("Greedy")
                        screen.fill(BLACK)
                        self.showCaptions(screen)
                        # Set the title of the screen.
                        pygame.display.set_caption("Tom using Greedy")
                        self.showText(screen, pygame.font.match_font(
                            'arial'), "Greedy", YELLOW, 35, 655, 110)
                        algorithm = GreedyAlgorithm(self.__initWorld)
                        solution = algorithm.start()
                        solutionWorld = solution[0]
                        nodeExpanded = solution[1]
                        depth = solution[2]
                        self.showComputingTime(screen, algorithm)
                        self.showText(screen, pygame.font.match_font(
                            'arial'), str(nodeExpanded), WHITE, 35, 655, 295)
                        self.showText(screen, pygame.font.match_font(
                            'arial'), str(depth), WHITE, 35, 655, 355)
                        self.setSolutionWorld(solutionWorld)
                        self.interfaceSolution(press, grid, i, screen, clock)
                    elif pos[0] > 641 and pos[0] < 692 and pos[1] > 130 and pos[1] < 153:
                        print("A*")
                        screen.fill(BLACK)
                        self.showCaptions(screen)
                        # Set the title of the screen.
                        pygame.display.set_caption("Tom using A*")
                        self.showText(screen, pygame.font.match_font(
                            'arial'), "A*", YELLOW, 35, 655, 140)
                        algorithm = StarAlgorithm(self.__initWorld)
                        solution = algorithm.start()
                        solutionWorld = solution[0]
                        nodeExpanded = solution[1]
                        depth = solution[2]
                        self.showComputingTime(screen, algorithm)
                        self.showText(screen, pygame.font.match_font(
                            'arial'), str(nodeExpanded), WHITE, 35, 655, 295)
                        self.showText(screen, pygame.font.match_font(
                            'arial'), str(depth), WHITE, 35, 655, 355)
                        self.setSolutionWorld(solutionWorld)
                        self.interfaceSolution(press, grid, i, screen, clock)
                    # print(pos[0])
                    # print(pos[1])

    def showCaptions(self, screen):
        self.showText(screen, pygame.font.match_font(
            'arial'), "BFS", WHITE, 35, 655, 20)

        self.showText(screen, pygame.font.match_font(
            'arial'), "DFS", WHITE, 35, 655, 50)

        self.showText(screen, pygame.font.match_font(
            'arial'), "UCS", WHITE, 35, 655, 80)

        self.showText(screen, pygame.font.match_font(
            'arial'), "Greedy", WHITE, 35, 655, 110)

        self.showText(screen, pygame.font.match_font(
            'arial'), "A*", WHITE, 35, 655, 140)

        self.showText(screen, pygame.font.match_font(
            'arial'), "Computing time: ", WHITE, 35, 655, 200)

        self.showText(screen, pygame.font.match_font(
            'arial'), "#Expanded nodes: ", WHITE, 35, 655, 265)

        self.showText(screen, pygame.font.match_font(
            'arial'), "Depth: ", WHITE, 35, 655, 325)