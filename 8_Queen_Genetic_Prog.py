# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 13:06:18 2020

@author: Gourav Gandhi
"""


import random
import numpy as np
from numpy.random import choice
import pandas as pd
import math
import time
from datetime import datetime
class GeneticCompute:
    # Initialing variables for Genetic programming for N Queens problem
    def __init__(self, i_total_queens):
        self.populationData=[]
        self.fitnessData=[]
        self.probabilityDist = []
        self.probDataFrame=()
        self.mutationRate = .07
        self.initialPopulation = 150
        self.MaxGenerations=10000
        self.crossOver = 0.5
        self.max_clashes=28
        # Possible numbers list 
        self.num_list = [x for x in range(i_total_queens)] 
        self.total_queens=i_total_queens        
        print("Inital Random Polulation : ", self.initialPopulation)  
        print("")
        print("Crossover : ", self.crossOver)
        # print("")
        # print("Mutation : ", self.mutationRate*100,"%")
        # print("")
        print("Maximum generation set for this program : ",self.MaxGenerations)
        print("")
        #print("")
        print("Computing Genetic Algorithm for 8 Queens problem. Please wait...")
        # print("")
        #time.sleep(3)
    
    def fitness(self, chromosome):
    # calculate row and column clashes
    # just subtract the unique length of array from total length of array
    # [1,1,1,2,2,2] - [1,2] => 4 clashes    
    # and evaluate chromosome against this score
        clashes = 0;
        row_col_clashes = abs(len(chromosome) - len(np.unique(chromosome)))
        clashes += row_col_clashes

    # calculate all the Diagonal Clashes
        for i in range(len(chromosome)):
            for j in range(i,len(chromosome)):
            
                if ( i != j):
                    dx = abs(i-j)
                    dy = abs(chromosome[i] - chromosome[j])
                    #print(dx,dy,(i-j),(chromosome[i] - chromosome[j]))
                    #time.sleep(.25)
                    if(dx == dy):                    
                        clashes += 1                        
        return self.max_clashes - clashes        
      
    
    # Initialing Population with Randon Sequence
    def initializing_population(self):        
        get_random = random.SystemRandom()        
        for outloop in range(self.initialPopulation):
            randomchromosome = []
            fitnessScore = 0
            for inloop in range(self.total_queens):
                randomchromosome.append(get_random.choice(self.num_list))
            fitnessScore=self.fitness(randomchromosome)
            self.populationData.append(randomchromosome) 
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
            #Taking 28 as full fitness score if there are no clashes
            self.probabilityDist.append(self.fitnessData[i]/self.max_clashes)
        
        
    
    # This function will generate childs and validate them with solution
    def Generate_childs(self):
        crossOverPoint = int(self.crossOver*self.total_queens)        
        for loop in range(self.MaxGenerations):            
            random_parents=[]
            #Take first 2 random parents with high Probability            
            rand_par_count=int(len(self.populationData)*.05)
            if(rand_par_count<5):
              rand_par_count=5
            #print("random count", rand_par_count, "total Pop" , len(self.populationData))
            for i in range(rand_par_count):
                random_parents.append(self.probDataFrame.loc[i:i+1,"Queens"].values[0])                
            while True:
                Parent1=random_parents[random.randint(0, rand_par_count-1)]
                Parent2=random_parents[random.randint(0, rand_par_count-1)]
                if Parent1!=Parent2:
                    break
                else:
                    continue
            child = Parent1[0:crossOverPoint]+Parent2[crossOverPoint:]
            #Adding Mutation
            child=self.mutate_child(child)            
            # Appending Population list with new child
            if child not in self.populationData:
                self.populationData.append(child)
            #print("Generation : ", loop+1, "Sequence : " ,child, self.fitness(child))
            if(self.fitness(child)==self.max_clashes):
                #print(child)                
                print("***** Solution Found *****")
                print("Solution generated by Genetic Programming is ", child)
                #print("And Exactly matched with the Target solution for 8 Queens Problem")
                #print("")
                #print("Below are some other facts --")
                print("")
                print("Total Generations spent :" , loop+1, " Avg Fitness Score : ", self.probDataFrame["FitnessScore"].mean())                                
                
                break                
            #Updating Population dataset with updated fitness score & probability             
            self.update_polulation()
            #print("Generation : ", loop+1, "Sequence : " ,child)
            if(loop==self.MaxGenerations-1):
                print("Sorry, No solution found. Please try adjusting variables configured in class Initialization")
            
     
    def mutate_child(self,child):
            for i in range(len(child)):
                if(random.randint(1,100)<=int(self.mutationRate*100)):            
                    child[i] = random.randint(0,self.total_queens-1)
            return child
    
        
    # Function to update population dataset & Problem DataFrame        
    def update_polulation(self):
         self.fitnessData.clear()
         #print(len(self.populationData))
         for items in self.populationData:
             self.fitnessData.append(self.fitness(items))
             #print(items)
         self.Calc_Probability()
         self.update_problemDF()
    
        
               
# Class to find and store possible solutions for N Queens puzzle
  

def main():
    for i in range(1):
        
    #Creating class object and passing parameter
        total_queens= 8      
        gc= GeneticCompute(total_queens)
        gc.initializing_population()    
        gc.Generate_childs()
    #print("")
        print("***************************************************************************************")    
    
if __name__ == "__main__":    
    main()
