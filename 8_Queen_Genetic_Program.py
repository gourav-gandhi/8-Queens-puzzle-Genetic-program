import random
import numpy as np
from numpy.random import choice
import pandas as pd
import math
import time

class GeneticCompute:
    # Initialing variables for Genetic programming for N Queens problem
    def __init__(self, i_target_Seq):
        self.populationData=[]
        self.fitnessData=[]
        self.probabilityDist = []
        self.probDataFrame=()
        self.mutationRate = .03
        self.initialPopulation = 100
        self.MaxGenerations=2000
        self.crossOver = 0.5
        # Possible numbers list 
        self.num_list = [x for x in range(len(i_target_Seq))] 
        self.target_seq=i_target_Seq
        print("Inital Random Polulation : ", self.initialPopulation)  
        print("")
        print("Crossover : ", self.crossOver)
        print("")
        print("Mutation : ", self.mutationRate*100,"%")
        print("")
        print("Maximum generation set for this program : ",self.MaxGenerations)
        print("")
        print("")
        print("Computing Genetic Algorithm for 8 Queens problem. Please wait...")
        print("")
        time.sleep(3)
    
    # Function to calculate Fitness Score
    def getFitnessScore(self,data):    
        fitnessScore = 0
        for inloop in range(len(self.target_seq)):
            if (data[inloop] == self.target_seq[inloop]):
                fitnessScore = fitnessScore + 1
        return fitnessScore
    
    
    # Initialing Population with Randon Sequence
    def initializing_population(self):        
        get_random = random.SystemRandom()
        
        for outloop in range(self.initialPopulation):
            randomData = []
            fitnessScore = 0
            for inloop in range(len(self.target_seq)):
                randomData.append(get_random.choice(self.num_list))
            fitnessScore=self.getFitnessScore(randomData)
            self.populationData.append(randomData) 
            self.fitnessData.append(fitnessScore)
        #print(self.populationData)
        self.Calc_Probability()
        self.update_problemDF()
        
    #Creating and updating DataFrame based on the Population set
    def update_problemDF(self):
        self.probDataFrame = pd.DataFrame({'Queens':self.populationData,'FitnessScore':self.fitnessData,'Probability':self.probabilityDist})
        self.probDataFrame = self.probDataFrame.sort_values(['Probability'],ascending=False)
        self.probDataFrame = self.probDataFrame.reset_index(drop=True)
        
    # Function to calulate Probability of each dataset in poplulation    
    def Calc_Probability(self):
        self.probabilityDist.clear()
        #print("prob" , len(self.probabilityDist))
        for i in range(len(self.populationData)):
            self.probabilityDist.append(self.fitnessData[i]/len(self.target_seq))
        
        #print(self.probDataFrame)
    
    # This function will generate childs and validate them with solution
    def Generate_childs(self):
        crossOverPoint = int(self.crossOver*len(self.target_seq))  
        #print(self.probDataFrame)
        for loop in range(self.MaxGenerations):
            Parents=[]
            #Take first 2 parents with high Probability
            Parents.append(self.probDataFrame[0:1]["Queens"].values[0])
            Parents.append(self.probDataFrame[1:2]["Queens"].values[0])
            #Generate new child with both parent using crossover
            child = Parents[0][0:crossOverPoint]+Parents[1][crossOverPoint:]
            #Adding Mutation
            child=self.mutate_child(child)            
            # Appending Population list with new child
            self.populationData.append(child)
            if(self.match(child)):
                print("***** Solution Found *****")
                print("Solution generated by Genetic Programming is ", child)
                print("And Exactly matched with the random picked solution from 8 Queens Problem(Non-Genetic method)")
                print("")
                print("Below are some other facts --")
                print("")
                print("Total Generations spent :" , loop+1, " Avg Fitness Score : ", self.probDataFrame["FitnessScore"].mean())                                
                break                
            #Updating Population dataset with updated fitness score & probability             
            self.update_polulation()
            if(loop==self.MaxGenerations-1):
                print("Sorry, No solution found. Please try adjusting variables configured in class Initialization")
            
     
    def mutate_child(self,child):
            for i in range(len(child)):
                if(random.randint(1,100)<=int(self.mutationRate*100)):            
                    child[i] = random.randint(0,len(self.target_seq)-1)
            return child
    
        
    # Function to update population dataset & Problem DataFrame        
    def update_polulation(self):
         self.fitnessData.clear()
         #print(len(self.populationData))
         for items in self.populationData:
             self.fitnessData.append(self.getFitnessScore(items))
             #print(items)
         self.Calc_Probability()
         self.update_problemDF()
    
        
    # Function to match solution generated from Genetic programming with one right answer of 8 Queens puzzle
    def match(self,child):
        if(self.getFitnessScore(child)==len(self.target_seq)):
            return True
        return False
            
# Class to find and store possible solutions for N Queens puzzle
class NQueens:
    """Generate all valid solutions for the N queens puzzle"""
    def __init__(self, size):
        # Store the puzzle (problem) size and the number of valid solutions
        self.size = size
        self.solutions = 0
        self.unique_comb=[]
             

    def solve(self):
        """Solve the N queens puzzle and print the number of solutions"""
        positions = [-1] * self.size
        #print(positions)
        self.put_queen(positions, 0)
        #print("Found", self.solutions, "solutions.")

    def put_queen(self, positions, target_col):
        """
        This is a recursive function and will check all posible case to place 
        in the queen in right place
        """
        # Base (stop) case - all N rows are occupied
        if target_col == self.size:
            self.Add_queen_postions(positions)            
            self.solutions += 1
        else:
            # For all N rows positions try to place a queen
            for row in range(self.size):
                # Reject all invalid positions
                if self.check_place(positions, target_col, row):
                    positions[target_col] = row
                    self.put_queen(positions, target_col + 1)


    def check_place(self, positions, ocuppied_col, row):
        """
        Checking row and diagonal positions to find if position is in under attack from any of
        the previously placed queens
        """
        #print(ocuppied_rows)
        for i in range(ocuppied_col):
            if positions[i] == row or \
                positions[i] - i == row - ocuppied_col or \
                positions[i] + i == row + ocuppied_col:

                return False
        return True
    
    #This function will store the all the posible solutions in a list
    def Add_queen_postions(self, positions):
        """Show the full NxN board"""
        queen_pos=[]
        #self.unique_comb.append(positions)
        for row in range(self.size):
            queen_pos.append(positions[row])            
        self.unique_comb.append(queen_pos)

    

def main():
    """Initialize and solve the n Queens puzzle"""       
    print("*****************************************************************************")
    print("Genetic Programming for N Queens Puzzle")
    print("*****************************************************************************")
    print("Welcome!!!")
    print(" ")
    print("**8 QUEENS PROBLEM** Generating all possible solutions(Non-Genetic method). Please wait..." )
    print(" ")
    
    chess_queen = NQueens(8)
    chess_queen.solve()
    total_unique_seq=chess_queen.unique_comb    
    print("Total possible solutions are ",len(total_unique_seq))
    print(" ")    
    print("Picking up one random solution out of ", len(total_unique_seq), "Please wait...")
    secure_random = random.SystemRandom()
    random_seq=secure_random.choice(total_unique_seq)
    time.sleep(2)
    print(" ") 
    print("Random Solution is ",random_seq)
    print("")
    print("********************************************************************************")
    print("**COMPUTING GENETIC ALGORITHM**")
    print("")
    print("Now generating 8 Queens puzzle solution using genetic programming approach")
    print("And then verify this with the conventional 8 queen puzzle random picked solution")
    print("Initializing.....")    
    print("")
    time.sleep(3)
    gc= GeneticCompute(random_seq)
    gc.initializing_population()
    #GC.Calc_Probability()
    gc.Generate_childs()
    print("")
    print("***************************************************************************************")    
    
if __name__ == "__main__":
    # execute only if run as a script
    main()