from node import Node
from time import process_time
from collections import deque

class AmplitudeAlgorithm:
    def __init__(self, world):
        self.emptyNode = Node(None, None, "first father", -1, 0, 0, 0)
        self.firstNode = Node(world, self.emptyNode, " ", 0, 0, 0, 0)
        self.tomPos = self.firstNode.searchForTom()  
        self.jerryPos = self.searchForJerry(world)  
        self.queue = deque([self.firstNode])  
        self.visited = set([tuple(self.tomPos)])  
        self.computingTime = ""
        self.length_world = world.shape[0]  
        self.height_world = world.shape[1]  

    def getComputingTime(self):
        return self.computingTime

    def setComputingTime(self, computingTime):
        self.computingTime = computingTime

    def searchForJerry(self, world):
    
        for i in range(world.shape[0]):
            for j in range(world.shape[1]):
                if world[i, j] == self.firstNode.PRINCESS:  
                    return [i, j]
        return None

    def start(self):
        
        startTime = process_time()
        expandedNodes = 0
        depth = 0

        while self.queue:
            currentNode = self.queue.popleft()  
            tomPos = currentNode.getTomPos()  

            print(f"Tom's current position: {tomPos}")  

           
            if tomPos == self.jerryPos:
                elapsedTime = process_time() - startTime
                elapsedTimeFormatted = "%.10f s." % elapsedTime
                self.setComputingTime(elapsedTimeFormatted)

                
                solution = currentNode.recreateSolutionWorld()
                solutionWorld = solution[::-1]  
                print(f"Jerry found! Expanded nodes: {expandedNodes + 1}")
                print(f"Depth: {depth}")
                print(f"Final cost of the solution is: {currentNode.getCost()}")
                print(currentNode.recreateSolution())
                return [solutionWorld, expandedNodes + 1, depth]

            
            possible_moves = [
                ("right", [tomPos[0], tomPos[1] + 1], ),
                ("left", [tomPos[0], tomPos[1] - 1]),
                ("down", [tomPos[0] + 1, tomPos[1]]),
                ("up", [tomPos[0] - 1, tomPos[1]])
            ]

            for move, newPos in possible_moves:
               
                if 0 <= newPos[0] < self.length_world and 0 <= newPos[1] < self.height_world:
                   
                    if currentNode.getState()[newPos[0], newPos[1]] != 1:
                        
                        if tuple(newPos) not in self.visited:#so that we dont explore the same position over and over again
                            self.visited.add(tuple(newPos))  
                            
                            newState = currentNode.getState().copy()
                            newState[tomPos[0], tomPos[1]] = 0  
                            newState[newPos[0], newPos[1]] = 2  
                            
                            son = Node(newState, currentNode, move, currentNode.getDepth() + 1,
                                       currentNode.getCost() + 1, currentNode.getStar(), currentNode.getFlower())
                            son.setTomPos(newPos)  
                            print(f"Tom moves {move} to position {newPos}")  

                            
                            self.queue.append(son)

                            
                            if son.getDepth() > depth:
                                depth = son.getDepth()

            expandedNodes += 1  
        
       
        print("No solution found.")
        return None
