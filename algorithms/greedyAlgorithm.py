from node import Node
from time import process_time

class GreedyAlgorithm:
    def __init__(self, world):
        self.emptyNode = Node(None, None, "first father", -1, 0, 0, 0)
        self.firstNode = Node(world, self.emptyNode, " ", 0, 0, 0, 0)
        self.tomPos = self.firstNode.searchForTom()  
        self.jerryPos = self.searchForJerry(world)   
        self.stack = [self.firstNode]               
        self.computingTime = ""
        self.length_world = world.shape[0]           
        self.height_world = world.shape[1]          
        self.visited = set()                          

    def getNodeMinHeuristic(self, stack):
        
        return min(stack, key=lambda node: node.getHeuristic())

    def getComputingTime(self):
        return self.computingTime

    def setComputingTime(self, computingTime):
        self.computingTime = computingTime

    def searchForJerry(self, world):
       
        for i in range(world.shape[0]):
            for j in range(world.shape[1]):
                if world[i, j] == self.firstNode.PRINCESS:  
                    return (i, j)  
        return None  

    def start(self):
        startTime = process_time()  
        expandedNodes = 0  
        depth = 0  

        while self.stack:
            
            currentNode = self.getNodeMinHeuristic(self.stack)
            self.stack.remove(currentNode)  

            
            tomPos = currentNode.getTomPos()

            
            print(f"Current Node Position: {tomPos}")
            print(f"Current Node State:\n{currentNode.getState()}")

            
            if tomPos == self.jerryPos:
                elapsedTime = process_time() - startTime
                elapsedTimeFormatted = "%.10f s." % elapsedTime
                self.setComputingTime(elapsedTimeFormatted)

                solution = currentNode.recreateSolutionWorld()  
                solutionWorld = solution[::-1]  

                print("Jerry found! Expanded nodes: ", expandedNodes)
                print("Depth: ", depth)
                print("The final cost of the solution is: " + str(currentNode.getCost()))
                print(currentNode.recreateSolution())  
                return [solutionWorld, expandedNodes, depth]

            
            possible_moves = [
                ("right", (tomPos[0], tomPos[1] + 1)),
                ("left", (tomPos[0], tomPos[1] - 1)),
                ("down", (tomPos[0] + 1, tomPos[1])),
                ("up", (tomPos[0] - 1, tomPos[1]))
            ]

            for move, newPos in possible_moves:
            
                if 0 <= newPos[0] < self.length_world and 0 <= newPos[1] < self.height_world:
                    
                    if currentNode.getState()[newPos[0], newPos[1]] != 1:
                        
                        newState = currentNode.getState().copy()
                        newState[tomPos[0], tomPos[1]] = 0  
                        newState[newPos[0], newPos[1]] = 2  

                        
                        son = Node(newState, currentNode, move, currentNode.getDepth() + 1,
                                   currentNode.getCost(), currentNode.getStar(), currentNode.getFlower())
                        son.setTomPos(newPos)  

                        
                        heuristic = son.calculateManhattanDistance(self.jerryPos)
                        son.setHeuristic(heuristic)

                        
                        tom_position_tuple = tuple(newPos) 
                        if tom_position_tuple not in self.visited and son.avoidGoBack2(newPos):
                            print(f"Adding new node from {tomPos} to {newPos} with heuristic {heuristic}")
                            self.stack.append(son)  
                            self.visited.add(tom_position_tuple) 

                           
                            if son.getDepth() > depth:
                                depth = son.getDepth()

            expandedNodes += 1   
        
        print("No solution found.")

        return None
