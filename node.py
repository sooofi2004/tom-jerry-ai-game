class Node:

    EMPTY = 0
    BLOCK = 1
    MARIO = 2
    STAR = 3
    KOOPA = 5
    FLOWER = 4
    PRINCESS = 6
    RESCUED_PRINCESS = 8

    def __init__(self, state, father, operator, depth, cost, star, flower):
        self.__state = state
        self.__father = father
        self.__operator = operator
        self.__depth = depth
        self.__cost = cost
        self.__star = star  # It lasts 6 grids - cost 1/2 and they accumulate
        self.__flower = flower  # Cost to go through a koopa when having a flower comes down to 1
        self.__tomPos = []
        self.__heuristic = 0  # The correct value is given only when the greedy algorithm is used
        self.__sumCostHeuristic = 0
        self.__awaitingCharacter = 0

    def getRigthCount(self):
        count = 0
        currentNode = self
        operator = currentNode.getOperator()
        while operator != "first father":
            if operator =="right":
                count += 1
            currentNode = currentNode.getFather()
            operator = currentNode.getOperator()
        return count

    def getState(self):
        return self.__state

    def getFather(self):
        return self.__father

    def getOperator(self):
        return self.__operator

    def getDepth(self):
        return self.__depth

    def getCost(self):
        return self.__cost

    def getHeuristic(self):
        return self.__heuristic

    def getTomPos(self):
        return self.__tomPos

    def getStar(self):
        return self.__star

    def getFlower(self):
        return self.__flower

    def getState(self):
        return self.__state.copy()

    def getAwaitingCharacter(self):
        return self.__awaitingCharacter
    
    def getSumCostHeuristic(self):
        return self.__sumCostHeuristic

    def setState(self, newState):
        self.__state = newState

    def setFather(self, newFather):
        self.__father = newFather

    def setOperator(self, newOperator):
        self.__operator = newOperator

    def setDepth(self, newDepth):
        self.__depth = newDepth

    def setCost(self, newCost):
        self.__cost = newCost

    def setHeuristic(self, newHeuristic):
        self.__heuristic = newHeuristic

    def setTomPos(self, newTomPos):
        self.__tomPos = newTomPos

    def setStar(self, newStarValue):
        self.__star = newStarValue

    def setFlower(self, newFlowerValue):
        self.__flower = newFlowerValue

    def setAwaitingCharacter(self, awaitingCharacter):
        self.__awaitingCharacter = awaitingCharacter

    def setSumCostHeuristic(self, newValue):
        self.__sumCostHeuristic = newValue

    def calculateManhattanDistance(self, princessPos):
        iDistance = princessPos[0] - self.getTomPos()[0]
        jDistance = princessPos[1] - self.getTomPos()[1]
        manhattanDistance = abs(iDistance) + abs(jDistance)
        return manhattanDistance

    def calculateHeuristic(self, manhattanDistance):
        heuristic = 0
        # assuming Tom has both stars, only a max. of 12 squares would cost half as much.
        if (manhattanDistance > 12):
            heuristic = manhattanDistance - 6
        else:
            heuristic = manhattanDistance / 2
        return heuristic

    def rightMovement(self, tomPos):
        return [tomPos[0], tomPos[1] + 1 if tomPos[1] < self.__state.shape[0] - 1 else False]

    def leftMovement(self, tomPos):
        return [tomPos[0], tomPos[1] - 1 if tomPos[1] > 0 else False]

    def upMovement(self, tomPos):
        return [tomPos[0] - 1 if tomPos[0] > 0 else False, tomPos[1]]

    def downMovement(self, tomPos):
        return [tomPos[0] + 1 if tomPos[0] < self.__state.shape[1] - 1 else False, tomPos[1]]

    # True means that the node can expand their sons, false means it can't
    def avoidGoBack2(self, nextTomPos):
        currentNode = self
        fatherNode = self.getFather()
        grandFatherNode = fatherNode.getFather()
        nextNodePosition = nextTomPos
        if grandFatherNode.getOperator() != "first father":
            if (grandFatherNode.getTomPos() == nextNodePosition):
                # print("flowercant", grandFatherNode.getFlower(), currentNode.getFlower())
                if (grandFatherNode.getStar() != currentNode.getStar() or grandFatherNode.getFlower() != currentNode.getFlower() or (fatherNode.getFlower() == 1 and currentNode.getFlower() == 0)):
                    # print("flowercantIf", grandFatherNode.getFlower(), currentNode.getFlower())
                    return True
                else:
                    return False
        return True

    def compareCicles2(self, nextTomPos):
        currentNode = self
        fatherNode = self.getFather()
        grandFatherNode = fatherNode.getFather()
        nextNodePosition = nextTomPos
        while grandFatherNode.getOperator() != "first father":
            # print("father", grandFatherNode.getTomPos(),"mia", nextNodePosition)
            if (grandFatherNode.getTomPos() == nextNodePosition):
                # print("flowercant", grandFatherNode.getFlower(),currentNode.getFlower())
                if (grandFatherNode.getStar() != currentNode.getStar() or grandFatherNode.getFlower() != currentNode.getFlower() or (fatherNode.getFlower() == 1 and currentNode.getFlower() == 0)):
                    # print("flowercantIf", grandFatherNode.getFlower(),currentNode.getFlower())
                    grandFatherNode = grandFatherNode.getFather()
                else:
                    return False
            else:
                grandFatherNode = grandFatherNode.getFather()
        return True

    def moveRight(self, posTom):
        i = posTom[0]
        j = posTom[1]
        self.__state[i, j] = self.getFather().getAwaitingCharacter()
        self.takeDecision([i, j+1])
        return self

    def moveLeft(self, posTom):
        i = posTom[0]
        j = posTom[1]
        self.__state[i, j] = self.getFather().getAwaitingCharacter()
        self.takeDecision([i, j-1])
        return self

    def moveDown(self, posTom):
        i = posTom[0]
        j = posTom[1]
        self.__state[i, j] = self.getFather().getAwaitingCharacter()
        self.takeDecision([i+1, j])
        return self

    def moveUp(self, posTom):
        i = posTom[0]
        j = posTom[1]
        self.__state[i, j] = self.getFather().getAwaitingCharacter()
        self.takeDecision([i-1, j])
        return self

    def setNewCost(self, pos):
        i = pos[0]
        j = pos[1]
        state = self.getState()
        currentCost = self.getCost()  # Current cost is the one from the father
        # If the position where Tom will move into has a Koopa inside then:
        if state[i, j] == self.KOOPA:
            if self.getStar() > 0:  # If true, Koopa will not affect Tom
                self.setCost(currentCost + 0.5)
            elif self.getFlower() > 0:  # If true, Tom can use the flower to kill Koopa
                self.setCost(currentCost + 1)
            else:  # If all of the cases above did not meet, Tom is affected by Koopa
                self.setCost(currentCost + 6)
        elif state[i, j] == self.FLOWER:
            if self.getStar() > 0:
                self.setCost(currentCost + 0.5)
            else:
                self.setCost(currentCost + 1)
        # If it is not a Koopa, I still need to check whether Tom has a star or not,
        # if so Tom needs 0.5 of effort to move across the grid
        else:
            if self.getStar() > 0:
                self.setCost(currentCost + 0.5)
            else:
                self.setCost(currentCost + 1)

    # pos is the future position of Tom
    def takeDecision(self, pos):
        i = pos[0]
        j = pos[1]
        if self.__state[i, j] == self.PRINCESS:
            self.setAwaitingCharacter(self.EMPTY)
            self.setStar(self.getStar() - 1 if self.getStar() > 0 else 0)
            self.__state[i, j] = self.RESCUED_PRINCESS
        elif self.__state[i, j] == self.KOOPA:
            if self.getFlower() > 0 or self.getStar() > 0:
                self.setAwaitingCharacter(self.EMPTY)
                self.setFlower(self.getFlower() -
                               1 if self.getFlower() > 0 else 0)
                self.setStar(self.getStar() - 1 if self.getStar() > 0 else 0)
            else:
                self.setAwaitingCharacter(self.KOOPA)
        elif self.__state[i, j] == self.FLOWER:
            if self.getStar() == 0:  # Tom can get the flower
                self.setFlower(self.getFlower() + 1)
                # print("cantidad flowers", self.getFlower())
                self.setAwaitingCharacter(self.EMPTY)
            else:
                self.setStar(self.getStar() - 1 if self.getStar() > 0 else 0)
                self.setAwaitingCharacter(self.FLOWER)
        elif self.__state[i, j] == self.STAR:
            if self.getFlower() == 0:  # Tom can get the star
                self.setStar(self.getStar() - 1 if self.getStar() > 0 else 0)
                self.setStar(self.getStar() + 6)
                self.setAwaitingCharacter(self.EMPTY)
            else:
                self.setAwaitingCharacter(self.STAR)
        else:
            self.setStar(self.getStar() - 1 if self.getStar() > 0 else 0)
            self.setAwaitingCharacter(self.EMPTY)

        if self.__state[i, j] != self.RESCUED_PRINCESS:
            self.__state[i, j] = self.MARIO

    def recreateSolution(self):
        directions = []
        currentNode = self
        while currentNode.getOperator() != "first father":
            directions.append(
                str(currentNode.getOperator() + " " + str(currentNode.getCost()) + " Star: " + str(currentNode.getStar())))
            currentNode = currentNode.getFather()
        return directions

    def recreateSolutionWorld(self):
        directions = []
        currentNode = self
        while currentNode.getOperator() != "first father":
            directions.append(currentNode.getState())
            currentNode = currentNode.getFather()
        return directions

    def searchForTom(self):
        tomPos = [-1, -1]  # Tom position [x,y]
        state = self.__state
        for i in range(state.shape[0]):
            for j in range(state.shape[1]):
                if (state[i, j] == self.MARIO):
                    tomPos[0] = i
                    tomPos[1] = j

        self.setTomPos(tomPos)
        return tomPos

    def isGoal(self):
        state = self.__state
        for i in range(state.shape[0]):
            for j in range(state.shape[1]):
                if (state[i, j] == self.RESCUED_PRINCESS):
                    return True
        return False
