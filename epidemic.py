
# models the spread of
# infection in a population
# Timesteps are in days
# Grey
# 14th April 2020

import random
import matplotlib.pyplot as plt
import math

TIMESTEPS=100 # 100 days
POPULATION=10000
VACCINATION_RATE=0.0 # Proportion of population that has been innoculated against the disease
TRANSMISSION_RATE=1.5 # Each person infects 2.5 others initially
CONTAGOUS_PERIOD=7 # The period in days over which an infectious person can infect others
DAILY_TRANSMISSION_RATE=TRANSMISSION_RATE/CONTAGOUS_PERIOD

class Person():
    
    def __init__(self, status=None, day=None):
        # Status
        # 0. No disease, no immunity
        # 1. Disease
        # 2. Immunity
        self.status = status
        # The number of days a person has been infectious
        self.day =  day


class Epidemiology():

    # Set up initial population.  Some may be innoculated against the disease,
    # others not
    
    def vaccinate(self):
        self.population=[]
        for i in range(POPULATION):
            if random.random() <=VACCINATION_RATE:
                self.population.append(Person(2,None))
            else:
                self.population.append(Person(0,None))

        return self.population

    def patient_zero(self):

        # First person to be infected with disease
        
        self.s=random.randint(0,POPULATION-1)
       
        while self.population[self.s].status != 0:
            self.s=random.randint(0,POPULATION-1)

        print("patient zero:",self.s)
        self.population[self.s].status=1
        self.population[self.s].day=0
        
        return self.population

    def spread(self):

        self.no_disease=[]
        self.disease=[]
        self.immune=[]

        print("Time step\tNo Disease\tDisease\t Immune")
        for i in range(TIMESTEPS):

            self.i=i
            self.calculate()

            for k in range(POPULATION):
                if  self.population[k].status == 1:
                    r_value=random.gauss(DAILY_TRANSMISSION_RATE, DAILY_TRANSMISSION_RATE/3)
                    if r_value > random.random():
                        r=random.randint(0,POPULATION-1)  
                        if   self.population[r].status == 0:
                            self.population[r].status=1
                            self.population[r].day=0

            for k in range(POPULATION):
                if   self.population[k].status == 1:
                    if self.population[k].day==CONTAGOUS_PERIOD:
                    # no longer infectious
                     self.population[k].status=2
                    else:
                    # still infectious
                     self.population[k].day+=1
                   
    def calculate(self):
        
            no_disease=0
            disease=0
            immune=0
    
            for j in range(POPULATION):
                if self.population[j].status==0:
                    no_disease=no_disease+1
                elif self.population[j].status==1:
                    disease=disease+1
                elif self.population[j].status==2:
                    immune=immune+1

            self.no_disease.append(no_disease)
            self.disease.append(disease)
            self.immune.append(immune)
  
            print(self.i,"\t",no_disease,"\t",disease,"\t",immune)


    def plot_simulation(self):
        
        plt.title("R0 is 1.5")
        plt.xlabel("Time") 
        plt.ylabel("Number of Infected") 
    #plt.xticks(rotation=90) 
        plt.plot(self.disease)
        
        plt.savefig("cases-v-time-1.5.png", format='png')
        plt.show()

class Main():

    def __init__(self):
        print("Running Pandemic Simulation")
        e=Epidemiology()
        e.vaccinate()
        e.patient_zero()
        e.spread()
        e.plot_simulation()

if __name__=="__main__":
    Main()
