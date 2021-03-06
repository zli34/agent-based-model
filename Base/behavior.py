# -*- coding: utf-8 -*-
"""

@author: conar
"""
from Examples.BWT import bwt_agents as bwt
from Examples.BWT.Building import Building, CommercialBuilding
from Examples.BWT.config.environ_config import environ as env
from scipy.spatial.distance import euclidean
from Examples.BWT.MapGenerator import Road
import logging

class Behavior(object):
    
     """ A class for behavior modification in agents
    
    Attributes:
        uid: unique ID for agent
        network: The original network id where the agent is nested in 
        resources: The amount of each asset the agent has
        hierarchy: The level in organization (low, medium, high, etc)
        history_self, history_others: The agents' memory of history of itself and others
        policy: The agent's policy
        
    """
    
     def __init__(self, resources = [], states = [], policy=None):
        """
         :param resources: A list of resources.
         :param states: A list of states.
         :param policy: The policy an agent follows.
        """
        
       
        self.resources = resources
        self.states = states
        self.policy = policy
    

     def getUtility(self):
        """Function for retrieving utility.
        :return: The utility of an agent."""
        
        
        return self.utility
    
     def getPolicy(self, history):
        """Function here for retrieving policies.
        :return: The policy of an agent."""
        
        return self.policy
        
     def getState(self):
        """Function here for retrieving states.
        :return: The state."""
        
        return self.state
        
     def getHistory(self, agentList):
         #...
         
         """:return: The history of particular agent(s) in the form of a list of lists."""
         return history
     
     def utility_function(agent, target):
        """Calculate the utility for an agent.
        :param agent: The agent whose utility is calculated.
        :param target: A target the agent will act towards.
        :return: The utility of the agent who act towards the target."""
        logging.info(target)
        logging.info(isinstance(target, Road))
        if(isinstance(agent, bwt.Criminal)):
            if(isinstance(target, bwt.Civilian)):
                U = target.resources[-1]**(env['alpha']) #+ (1-env.config['alpha'])*y
                # print("resource: " + str(target.resources[-1]))
                return U
            if(isinstance(target, Building) or isinstance(target, CommercialBuilding)):
                # U = target.attractiveness**(-env['alpha'])
                if target.attractiveness >= 0.2:
                    U = target.attractiveness**(-env['alpha'])
                    # print("attract: " + str(target.attractiveness))
                else:
                    U = 0
                return U
        if(isinstance(agent, bwt.Police)):
            U = target.crime_propensity**(env['alpha'])
            return U
        elif(isinstance(agent, bwt.Civilian)):
            U = agent.routes_completed**(env['alpha'])
            return U

        else:
            return 0
                
            
        return 0
    
     def cost_function(agent, target):
         """Calculate the cost of an agent.
        :param agent: The agent whose cost is calculated.
        :param target: A target the agent will act towards.
        :return: The cost of the agent who act towards the target."""
         
         if(isinstance(agent, bwt.Criminal)):
             dist = euclidean(agent.pos, target.pos)
             C =  (1/(env['gamma']))*dist
             return C
                
         if(isinstance(agent, bwt.Police)):
             dist = euclidean(agent.pos, target.pos)
             C = dist
             return C
            
         elif(isinstance(agent, bwt.Civilian)):
             dist = euclidean(agent.pos, target.pos)
             C = dist
             return C
         else:
             return 0
         
         return 
 
     def computeUtility(self, agents, pos):
         
         """Compute utility for a given agent after passing a list of buildings, police
         and civilians to it after looking within an agent's vision limit"""
         
         #FIXME Is this function even necessary?
          
         #TODO Different types of agents shouldn't necessarily have the same 
         # utility function
         #TODO Make a static method for computing utility for different agents.
         #TODO Agents should not be able to perfectly see all resources.
         #TODO There should be some risk probability for being arrested
             
         dist = [euclidean(pos, agent) for agent in agents]
         value = []
             
         for agent in agents:
             if isinstance(agent, bwt.Civilian):
                 value.append(self.utility_function(agent.resources[-1]))
             elif isinstance(agent, Building): 
                 value.append(self.utility_function(agent.attractiveness[-1]))
                     
         criminal_utility = value - dist
             
         #TODO compute and add in cost of travel to get to agents and buildings 
         # along with the chance of being caught
             
            
         return criminal_utility
         
#         If the agent is a civilian:
#          if isinstance(self, Civilian):
#             
#             Civilians get utility from completing their routes and going to work
#             coming back home in as little time as possible. (This means they evaluate
#             the minimum distance between their endpoints under the constraint that they 
#             want to avoid 'bad areas' and criminals as they go.)
#             
#             They get disutility from being robbed or attacked, and
#             from incurring risks by walking through 'bad areas'.
#             
#             x = [civilian.resources[-1] for civilian in civilians]
#             
#             civilian_utility = U(x,y) 
#             
#             return civilian_utility
#
#         If the agent is police:
#         if isinstance(self, Police):
#             
#             Police get utility from stopping crimes, catching criminals, and pursuing
#             criminals. They get disutility from failing to catch criminals, failing 
#             to stop crimes, or getting killed by criminals. 
#             
#             x = [civilian.resources[-1] for civilian in civilians]
#             
#             police_utility = U(x,y) 
#             
#             return police_utility
         
        
        #return the instant or long-term reward if the initial state and the current action of the agent are given
     def get_victim_location(criminal_utility_list, agents):

        """:return: Position of the agent the criminal will pursue. """
        criminal_utility_max = max(criminal_utility_list)
        victim_index = criminal_utility_list.index(criminal_utility_max)
        
        victim_position = agents[victim_index].pos
        return agents[victim_index]  # Chris: I changed to give agent not position, sorry
        
     def computeTotalUtility(self, agent):
         
         """This computes total utility up until present time-step for the agent."""
         
         #TODO Ideally agents should saved their most recently computed expected utility
         #     and then update that previous estimate in a sequential average 
         
         utility_list = [agent.utility[i]*(kappa)^i for i in len(agent.utility)]
         total_discounted_utility = sum(utility_list)
         
         return NotImplementedError
        
     def computeCost(self, agent):
         
         """Compute a cost function for criminals."""
         
         #TODO Generalize to other agent types
    
         
         return NotImplementedError
        
    
     def updatePolicy(self):
        #...
        """update the agent's policy based on some optimization criteria, history and so on."""
        return self.policy

