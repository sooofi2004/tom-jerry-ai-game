from node import Node
from time import process_time

class StarAlgorithm:
    def __init__(self, world):
        self.emptyNode = Node(None, None, "first father", -1, 0, 0, 0)
        self.firstNode = Node(world, self.emptyNode, " ", 0, 0, 0, 0)
        self.tomPos = self.firstNode.searchForTom()
        self.jerryPos = self.searchForJerry(world)
        self.stack = [self.firstNode]
        self.visited = set()  # Visited set to keep track of explored states
        self.computingTime = ""
        self.length_world = world.shape[1]
        self.height_world = world.shape[0]

    def getNodeMinSumCostHeuristic(self, stack):
       
        return min(range(len(stack)), key=lambda i: stack[i].getSumCostHeuristic())

    def getComputingTime(self):
        return self.computingTime

    def setComputingTime(self, computingTime):
        self.computingTime = computingTime

    def searchForJerry(self, world):
        jerryPos = []
        for i in range(world.shape[0]):
            for j in range(world.shape[1]):
                if world[i, j] == self.firstNode.PRINCESS:
                    jerryPos = [i, j]
        return jerryPos

    def start(self):
        startTime = process_time()
        expandedNodes = 0
        depth = 0

        while self.stack:
            
            minIndex = self.getNodeMinSumCostHeuristic(self.stack)
            currentNode = self.stack.pop(minIndex)

           
            currentState = str(currentNode.getTomPos())

           
            if currentState in self.visited:
                continue

           
            self.visited.add(currentState)

            
            if currentNode.getTomPos() == self.jerryPos:
                elapsedTime = process_time() - startTime
                elapsedTimeFormatted = "%.10f s." % elapsedTime
                self.setComputingTime(elapsedTimeFormatted)

                solution = currentNode.recreateSolutionWorld()
                solutionWorld = solution[::-1]

                print("Jerry found! Expanded nodes: ", expandedNodes + 1)
                print("Depth: ", depth)
                print("The final cost of the solution is: " + str(currentNode.getCost()))
                print(currentNode.recreateSolution())
                return [solutionWorld, expandedNodes + 1, depth]

            tomPos = currentNode.getTomPos()
            expandedNodes += 1

           
            possible_moves = [
                ("right", [tomPos[0], tomPos[1] + 1]),
                ("left", [tomPos[0], tomPos[1] - 1]),
                ("down", [tomPos[0] + 1, tomPos[1]]),
                ("up", [tomPos[0] - 1, tomPos[1]])
            ]

            for move, newPos in possible_moves:
                if 0 <= newPos[0] < self.height_world and 0 <= newPos[1] < self.length_world:
                    
                    if currentNode.getState()[newPos[0], newPos[1]] != 1:
                        
                        newState = currentNode.getState().copy() 
                      
                        newState[tomPos[0], tomPos[1]] = 0  
                        newState[newPos[0], newPos[1]] = 2  

                        son = Node(newState, currentNode, move, 
                                   currentNode.getDepth() + 1, currentNode.getCost() + 1, 
                                   currentNode.getStar(), currentNode.getFlower())

                        
                        son.setTomPos(newPos)

                       
                        manhattanDistance = abs(self.jerryPos[0] - newPos[0]) + abs(self.jerryPos[1] - newPos[1])
                        son.setHeuristic(manhattanDistance)

                        
                        son.setSumCostHeuristic(son.getCost() + son.getHeuristic())

                        
                        newStateStr = str(son.getTomPos())

                       
                        if newStateStr not in self.visited:
                            self.stack.append(son)
                            if son.getDepth() > depth:
                                depth = son.getDepth()

        print("No solution found.")
        return None
