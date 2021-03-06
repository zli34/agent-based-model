from Base.agent_cma_zl import Agent
import random
from Examples.BWT.Building import Building, CommercialBuilding
from Examples.BWT.MapGenerator import Road
import math
from Base.behavior import Behavior as b
from scipy.spatial import distance
import math
import logging
import functools as functools
from numba import *

class Criminal(Agent):

    """
    A subclass of Agent for Criminal types.

    """


    def __init__(self, pos, model, resources, uid, network=None, hierarchy=None, history_self=[],
                 history_others=[], policy=None, allies=[], competitors=[], utility = [], crime_propensity=None,
                 residence=None, kind=1, workplace=None):
        """
        :param pos: The position tuple of the agent.
        :param model: The environment the agent is in.
        :param resources: The amount of each asset the agent has.
        :param uid: The unique ID for the agent.
        :param network: The original network id where the agent is nested in.
        :param hierarchy: The level in organization (low, medium, high, etc).
        :param history_self: The agents' memory of history of itself.
        :param history_others: The agents' memory of history of others.
        :param policy: The agent's policy.
        :param residence: The living places of the agent.
        :param competitors: The list of agents who are the competitors of the agent.
        :param utility: The history of the utility of the agent.
        :param crime_propensity: The crime propensity of the agent.
        :param kind: Type of crime the criminal commits. 1: damage a building. 2: rob a civilian. 3: commit a violent crime.
        :param workplace: An instance of the class CommercialBuilding.
        """
        super().__init__(self, pos, model, resources, uid, network, hierarchy, policy)
        self.pos = pos
        self.environment = model
        self.resources = resources
        self.uid = uid
        self.history_self = history_self
        self.history_others = history_others
        self.allies = allies
        self.competitors = competitors
        self.crime_propensity = crime_propensity
        self.vision = random.randint(1, model.config['agent_vision_limit'])
        self.recidivism = 1
        self.is_incarcerated = False
        self.permanent_criminal = False
        self.convert_to_civilian = False
        self.remaining_sentence = 0
        self.network = network
        self.hierarchy = hierarchy
        self.policy = policy
        self.residence = residence
        self.utility = utility
        self.workplace = workplace

        # Attractiveness for each building
        self.building_memory = list()

        # Type of crime the criminal commits. 1: damage a building. 2: rob a civilian. 3: commit a violent crime
        self.kind = kind

        # Whether he can walk across buildings or not
        self.walk_across_buildings = 'Criminal' in model.config['walk_across_buildings']
        
        # Whether he commits a crime successfully in the current step
        self.do_crime = False

    def __str__(self):
        return "Criminal " + str(self.uid)

    def __repr__(self):
        return str(self)

    def step(self):
        """Complete one time step."""
        self.do_crime = False
        # If criminal is incarcerated, wait out sentence. On last step of sentence, may leave the police department.
        
<<<<<<< HEAD
=======
        personal_crime_threshold = random.randrange(0,1)
>>>>>>> 5f75cb2d4d25500bd8bfa1c37c1ee7455eb1e12b
            
        if self.is_incarcerated:
            self.remaining_sentence -= 1
            logging.info("Criminal has %s steps left in prison sentence" % str(self.remaining_sentence))
            if self.remaining_sentence <= 0:
                self.is_incarcerated = False
                logging.info("Criminal is free!")
            else:
                # Another step in prison
                return

        # Check if we need to search for other coalitions or to split
        #self.update_coalition_status()

        # Look for victims if we have enough propensity
        if self.recidivism <.5:
            
            self._convert_to_civilian()
<<<<<<< HEAD
            self.random_move_and_avoid_role([Building])
            return
            
=======
            return
        
        if personal_crime_threshold < self.environment.config['gamma']:
            
            self._convert_to_civilian()
            return
>>>>>>> 5f75cb2d4d25500bd8bfa1c37c1ee7455eb1e12b
        
        if self.environment.has_sufficient_propensity(self):

            possible_victim = self.look_for_victim(radius=1, include_center=True)


            if possible_victim and not self.check_for_police():

                unfiltered_neighbors =  self.environment.grid.get_neighbors(self.pos, True,  radius=1, include_center=False)
                neighbors = list(filter(lambda agent: not(type(agent) is Road), unfiltered_neighbors))
#                print(len(neighbors))
#                for neigh in neighbors:
#                    if type(neigh) is Building:
#                        print("Building! " + str(neigh.attractiveness))
#                    if type(neigh) is CommercialBuilding:
#                        print("CommercialBuilding! " + str(neigh.attractiveness))
#
                if not neighbors:
                    # FIXME Penalize utility
                    if self.walk_across_buildings:
                        self.random_move_and_avoid_role([Police])
                    else:
                        self.random_move_and_avoid_role([Police, Building])
                else:
                    # TODO clean up

                    calculate_utility = lambda self, agent: b.utility_function(self, agent) - b.cost_function(agent=self, target=agent)
                    #dist = [distance.euclidean(self.pos, neighbor.pos) for neighbor in neighbors]
                    #print("Distance: " + str(dist))



                    current_utility = [calculate_utility(self, neighbor) for neighbor in neighbors]
                    #print("current utility: " + str(current_utility))

                    if(max(current_utility) > 0):
                        victim_index = current_utility.index(max(current_utility))
                        immediate_victim = neighbors[victim_index]
                        # print("victim index: " + str(victim_index))

                    # There is a potential victim in the neighbourhood, and no police around - try to rob them
                    #    print("Attempting crime at {0} against {1}.".format(self.pos, immediate_victim))

                        if isinstance(immediate_victim, Police) or isinstance(immediate_victim, Civilian) or isinstance(immediate_victim, Criminal):
                        #neighbors = self.environment.grid.get_neighbors(self.pos, True,  radius=1, include_center=True)
                        #immediate_victim = max(b.computeUtility(neighbors))
                            self.walk_to(immediate_victim.pos)
                            self.commit_violent_crime(immediate_victim)
                            self.utility.append(immediate_victim.resources[-1])

                        elif isinstance(immediate_victim, Building) or isinstance(immediate_victim, CommercialBuilding):
                            self.walk_to(immediate_victim.pos)
                            self.commit_nonviolent_crime(immediate_victim)
                            self.utility.append(immediate_victim.attractiveness)
                    else:
                        if self.walk_across_buildings:
                            self.random_move_and_avoid_role([Police])
                        else:
                            self.random_move_and_avoid_role([Police, Building])


            else:  # Look further away for victims if there are none in the neighbourhood
                potential_victim = self.look_for_victim(radius=self.vision, include_center=False)
                if isinstance(potential_victim, Police) or isinstance(potential_victim, Criminal) or isinstance(potential_victim, Civilian):
                    # print("Possible victim at %s" % str(potential_victim.pos))
                    # Found a victim -- if more than one, choose to pursue
                    # utility maximizing victim

                    unfiltered_neighbors =  self.environment.grid.get_neighbors(self.pos, True,  radius=self.vision, include_center=False)
                    neighbors =  [agent for agent in unfiltered_neighbors if not isinstance(agent, Road)]
                    if neighbors:
                        calculate_utility = lambda self, agent: b.utility_function(self, agent) - b.cost_function(agent=self, target=agent)
                        utility_list = [calculate_utility(self, neighbor) for neighbor in neighbors]

                        next_victim = b.get_victim_location(utility_list, neighbors)

                        #TODO Check that this works right
                        # just avoid police
                        if self.walk_across_buildings:
                            self.walk_to_avoid(next_victim.pos, [Police])
                        # avoid both police and buildings
                        else:
                            self.walk_to_avoid(next_victim.pos, [Police, Building, CommercialBuilding])
                        self.utility.append(-b.cost_function(self, next_victim))
                    return

        # Couldn't find victim, or insufficient propensity
        # FIXME decrement utility
        # TODO Check that criminals utility cost is relative to their home base and the potential victims
        else:
            if self.walk_across_buildings:
                self.random_move_and_avoid_role([Police])
            else:
                self.random_move_and_avoid_role([Police, Building])

        # add the buildings in the neighbourhood to the criminal's memory
        neighborhood = self.environment.grid.get_neighborhood(self.pos, moore=False, include_center=True)

        for cell in neighborhood:
            for agent_building in self.environment.grid.get_cell_list_contents(cell):
                if type(agent_building) is Building or type(agent_building) is CommercialBuilding:
                    self.add_to_building_memory(agent_building)
        return
    
    def _convert_to_civilian(self):
        
        self.convert_to_civilian = True
        
        

    def random_move_and_avoid_role(self, role_to_avoid):
        """Randomly walk around, but not into cells with an agent of the specified role.
        :param role_to_avoid: A list of types of classes the agent will avoid."""
        possible_moves = self.environment.grid.get_neighborhood(self.pos, moore=False, include_center=True)
        next_moves = []

        # add the cells without roles to avoid to next_moves
        for cell in possible_moves:
            contents = self.environment.grid.get_cell_list_contents(cell)
            if sum([type(agent) in role_to_avoid for agent in contents]) == 0:
                next_moves.append(cell)

        random.shuffle(next_moves)
        self.environment.grid.move_agent(self, next_moves[0])


    def add_to_building_memory(self, building):
        """Add a building to the civilian's momory.
        :param building: An instance of the class Building the agent will memorize.
        """
        self.building_memory.append(building)
        self.building_memory = list(set(self.building_memory)) # remove repeats

    def commit_nonviolent_crime(self, victim):
        """Commit a crime against a building in the vicinity.

         :param victim: An instance of the class Building.
         """
        # FIXME criminals seem to be very stupid
        # Rob half of their resources if model deems the crime successful
        # This call to the model is an attempt to keep the environment in charge of interaction rules

        if self.pos == victim.pos:
            self.attempt_nonviolent_crime(victim)

    def commit_violent_crime(self, victim):
        """Commit a crime against an agent in the vicinity.
        :param victim: An instance of the class Agent."""
        self.attempt_violent_crime(victim)


    def crime_wrapper(crime_function):
        """Controls whether a crime is successful."""

        @functools.wraps(crime_function)
        def inner_wrapper(self, *args, **kwargs):
           #print(crime_function)
           if random.random() < self.environment.config['crime_success_probability']:
               self.environment.total_crimes += 1
               crime_function(self, *args, **kwargs)

        return inner_wrapper

    @crime_wrapper
    def attempt_violent_crime(self, victim):
        """Commit a crime against an agent in the vicinity.
        :param victim: An instance of the class Agent."""
        # Add criminal to victim's memory

        #FIXME getting 'AttributeError: 'Criminal' object has no attribute 'add_to_memory'
        #FIXME every time this is called.

        assert(isinstance(self, Criminal))
        victim.add_to_memory(self)
        self.do_crime = True

        # Probability of success - replace with any equation, e.g. including crime propensity
        self.increase_propensity()
        #print(str(self) + " successfully robbed " + str(victim) + " at %s." % str(victim.pos))

        if self.network:
            # Distribute resources across coalition
            split = (victim.resources[0]/2)/len(self.network.members)

            for member in self.network.members:
                member.resources[0] += split
        else:
            # Criminal get's 100% of the stolen goods
            self.resources[0] += victim.resources[0]/2

        # Victim loses money
        victim.resources[0] /= 2

    @crime_wrapper
    def attempt_nonviolent_crime(self, victim):
        """Commit a crime against a building in the vicinity.

         :param victim: An instance of the class Building.
         """
        self.do_crime = True
        if isinstance(victim, Building) or isinstance(victim, CommercialBuilding):
            self.environment.decrement_building_attractiveness(victim, 1)
            #print(str(self) + " successfully robbed " + str(victim) + " at %s." % str(victim.pos))


            neighbor_buildings = list(
                filter(
                    lambda x: isinstance(x, Building),
                    self.environment.grid.get_neighbors(victim.pos, moore=True, include_center=False, radius=1)))

            for building in neighbor_buildings:
                self.environment.decrement_building_attractiveness(building, 0.5)


            # Give Criminal resources for crime
            self.resources[0] += 5


    def look_for_victim(self, radius, include_center):
        """Look in the neighborhood for a potential victim to rob.

        :return: An agent object.
                 False, if no victims in sight.
        """
        neighbors = self.environment.grid.get_neighbors(self.pos, True,  radius=radius, include_center=include_center)
        random.shuffle(neighbors)
        for agent in neighbors:
            #print("\n{0} is a Building: {1}\nis a Civilian {2}".format(type(agent), type(agent) == Building.Building, type(agent) == Civilian))
            if type(agent) == Civilian or type(agent) == Building or type(agent) == CommercialBuilding:
                # Pick out this agent to be victimized

                return agent

        return False

    def check_for_police(self):
        """Check for police around a position, but only in cells the criminal can currently see in their neighborhood.

        :return: True if there are police in proximity to pos that the Criminal can see in their neighborhood.
        """
        #print("Are there any police around?")
        neighbors = self.environment.grid.get_neighbors(self.pos, moore=True, include_center=True, radius=self.vision)

        for neighbor in neighbors:
            if type(neighbor) is Police:
                # There are Police
                #print("Police are present, abort crime.")
                return True
        # No police
        return False

    def increase_propensity(self):
        """Increase the propensity of the criminal. Can be simple or maybe more complicated."""
        self.crime_propensity += 1
        return

    def join_agents_coalition(self, agent):
        """If not in coalition join it. If in one, merge them. Assumes authority to do so in latter case.
        :param agent: Another agent who will join the agent's coalition.

        :return: True, if successfully joins/merges coalition.
        """

        if self.network is not None:
            # In a coalition already, try to merge the other coalition into ours
            if agent.network is None:
                # Let the solo agent join our coalition
                return self.network.add_member(agent)
            elif self.network is not agent.network:
                # Merge the two DIFFERENT coalitions
                return self.network.merge(agent.network)
        elif agent.network is None:
            # Other agent is also not in a coalition, create a new one.
            coalition = self.environment.new_coalition()
            coalition.add_member(self)
            coalition.add_member(agent)
            return True
        else:
            # Not currently in a network, try to join the coalition
            return agent.network.add_member(self)

    def leave_coalition(self):
        """Let an agent leave their coalition.

        FIXME Should probably live in Agent
        """
        if self.network is None:
            logging.info("\nError: Criminal tried to leave coalition when not in one.\n")
            return

        # Leave coalition
        self.network.remove_member(self)

    def try_to_join_nearby_coalitions(self):
        """Look for criminals around to coerce into joining forces."""
        # Can only join forces at a maximum specified distance
        radius = self.environment.config['coalition_merge_distance']

        potential_partners = self.environment.grid.get_neighbors(pos=self.pos, radius=radius,
                                                           moore=True, include_center=True)
        if potential_partners:
            random.shuffle(potential_partners)  # randomize
            for agent in potential_partners:
                if type(agent) is Criminal and agent is not self:
                    # Agent is a criminal - join forces
                    if self.join_agents_coalition(agent):
                        return


    def update_coalition_status(self):
        """General workhorse for coalition stuff.
.
        Check if personal propensity is greater than required threshold. If not, try to join nearby coalitions. If it \
        is, split from any coalitions this criminal is in.
        """

        if not self.environment.has_sufficient_propensity(self):
            # Propensity too low, look for others to join coalition with
            self.try_to_join_nearby_coalitions()
        elif self.environment.can_be_solo(self):
            # Propensity is high enough to go solo, split from current coalition
            if self.network is not None:
                self.leave_coalition()
        return

    def walk_to_avoid(self, coordinates, role_to_avoid):
        """Walk one cell towards a set of coordinates, using only cardinal directions (North/South or West/East).
           Avoid specified roles.
           :param coordinates: The coordinate tuple the agent will move towards.
           :param role_to_avoid: A list of types of classes the agent will avoid.
        """
        possible_moves = self.environment.grid.get_neighborhood(self.pos, moore=False, include_center=True)
        next_moves = []

        # add the cells without roles to avoid to next_moves
        for cell in possible_moves:
            contents = self.environment.grid.get_cell_list_contents(cell)
            if sum([type(agent) in role_to_avoid for agent in contents]) == 0:
                next_moves.append(cell)

        random.shuffle(next_moves)

        best_distance = 0
        best_cell = (0, 0)

        # get the best utility based on larger distance from cell to criminals and shorter distance from cell to goal
        for cell in next_moves:
            # choose the shortest distance
            dist = distance.euclidean(cell, coordinates)
            if dist < best_distance:
                best_distance = dist
                best_cell = cell
                
        self.environment.grid.move_agent(self, best_cell)



    def target_building(self):
        target = self.environment.agents['buildings'][0]
        risk = target.attractiveness + math.sqrt((self.pos[0]-target.pos[0])**2 + (self.pos[1]-target.pos[1])**2)
        for i in range(len(self.environment.buildings)):
            dist = math.sqrt((self.pos[0]-self.environment.agents['buildings'].pos[0])**2 + (self.pos[1]-self.environment.agents['buildings'][i].pos[1])**2)
            if(risk > self.environment.agents['buildings'].attractiveness + dist):
                risk = self.environment.agents['buildings'].attractiveness + dist
                target = self.environment.agents['buildings'][i]
        return target

    def update_attractiveness(self):
        neighbor_buildings = list(
                filter(
                    lambda x: isinstance(x, Building),
                    self.grid.get_neighbors(self.pos, moore=True, include_center=True, radius=1)))
        for building in neighbor_buildings:
            self.building_memory[building.uid] = building.attractiveness



class Civilian(Agent):


    """
    A subclass of Agent for Civilian types.

    """
    def __init__(self, pos, model, resources, uid, utility = [], residence=None, workplace=None):
        """
        :param pos: The position tuple of the agent.
        :param model: The environment the agent is in.
        :param resources: The amount of each asset the agent has.
        :param uid: The unique ID for the agent.
        :param residence: The living places of the agent.
        :param utility: The history of the utility of the agent.
        :param workplace: An instance of the class CommercialBuilding.
        """
        super().__init__(self, pos, model, resources, uid, residence)
        self.pos = pos
        self.environment = model
        self.resources = resources
        self.uid = uid
        self.history_self = None
        self.history_others = None
        self.allies = None
        self.competitors = None
        self.memory = list()
        self.mental_map = dict()
        self.vision = random.randint(1, model.config['agent_vision_limit'])
        self.workplace = workplace
        self.utility = utility
        self.residence = residence
        self.route = (self.residence.pos, self.workplace.pos)
        # Individuals who have tried to rob this civilian
        self.criminal_memory = list()
        self.routes_completed = 0
        self.recidivism = 0
        # Attractiveness for each building
        self.building_memory = list()
        self.walk_across_buildings = 'Civilian' in model.config['walk_across_buildings']
        self.last_pos = pos
        return


    def __str__(self):
        return "Civilian " + str(self.uid)
    
    def step(self):
        # FIXME do routes even after being robbed
        # TODO USe Zhen's walk_to_avoid function
        #if len(self.memory) > 0:
        #    print("walk_and_avoid")
        #    self.walk_and_avoid()
        #else:
        #    #self.random_move()
        #    print("walk_route")
        #    self.walk_route()

        # Have cleaned up the code (have considered the two cases above)
        # Avoid criminals in memory and avoid buildings
        self.walk_and_avoid()

        # add the buildings in the neighbourhood to the civilian's memory
        neighborhood = self.environment.grid.get_neighborhood(self.pos, moore=False, include_center=True)

        for cell in neighborhood:
            for agent_building in self.environment.grid.get_cell_list_contents(cell):
                if type(agent_building) is Building or type(agent_building) is CommercialBuilding:
                    self.add_to_building_memory(agent_building)

        if(self.routes_completed % 2 == 0):
            if(self.pos == self.workplace.pos):
                print("Arrive at workplace!")
                self.routes_completed += 1
                self.utility.append(b.utility_function(self, self))

        else:
            if(self.pos == self.residence.pos):
                print("Arrive at home!")
                self.routes_completed += 1
                self.utility.append(b.utility_function(self, self))

        return

    #def walk_route(self):
    #    # TODO Descriptive comment
    #    if(self.routes_completed % 2 == 0):
    #        self.walk_to(self.workplace.pos)
    #    else:
    #        self.walk_to(self.residence.pos)
    #
    #    return
    def current_route_goal(self):
        """
        :return: The goal of the current route of the civilian.
        """
        if(self.routes_completed % 2 == 0):
            goal = self.workplace.pos
        else:
            goal = self.residence.pos

        return goal

    def walk_and_avoid(self):
        """Avoid criminals in his memory and buildings and go towards to his goal.

        :return: True if successfully moved. False if couldn't move anywhere.
        """

        # FIXME CIVILIAN move choosing does not consider criminals they can see more than one space away
        # doesn't consider moving towards a criminal they can see

        goal = self.current_route_goal()
        #print("goal: " + str(goal))
        neighbourhoods = self.environment.grid.get_neighborhood(self.pos, moore=False, include_center=False, radius = 1)
        neighbors = self.environment.grid.get_neighbors(self.pos, moore=True, radius=self.vision, include_center=True)

        #Find nearby criminals for current location in the civilian's memory
        criminals_nearby = [crim for crim in filter(lambda agent: agent in self.memory, neighbors)]
        # if (len(criminals_nearby)):
        #     print("criminals_nearby: " + str(criminals_nearby))

        # The civilian should avoid buildings but should not avoid his home or workplace
        if len(criminals_nearby) == 0:
            #print("No criminals nearby!")
            if not self.walk_across_buildings:
                next_moves = [cell for cell in filter(lambda x: (self.environment.can_agent_occupy_cell(x) or x == goal) and x != self.last_pos, neighbourhoods)]
            else:
                next_moves = [cell for cell in filter(lambda x: x != self.last_pos, neighbourhoods)]
        else:
            if not self.walk_across_buildings:
                next_moves = [cell for cell in filter(lambda x: self.environment.can_agent_occupy_cell(x) or x == goal, neighbourhoods)]
            else:
                next_moves = neighbourhoods

        if  len(next_moves) == 0:
            next_moves.append(self.last_pos)

        random.shuffle(next_moves)

        # print("last_pos: " + str(self.last_pos))
        self.last_pos = (self.pos[0], self.pos[1])



        # print("next_moves: " + str(next_moves))



        #Make list of points nearby, calculate triangle inequality for ways to maximize min distance
        #from a criminal while walking route

        #if not criminals_nearby:
            #If not criminals nearby, then civilian walks to goal as usual
        #    self.walk_route()
        #    return True
        #else:
        #Calculate distance between nearby cells and the goal of the civilians route, choose the one that
        #maximizes distance from criminal and minimizes distance to goal

        #distance_from_cells_to_goal = [distance.euclidean(self.current_route_goal(), cell) for cell in next_moves]
        ###distance_from_self_to_criminal = [distance.euclidean(self.pos, criminal) for criminal in criminals_nearby]
        ###closest_criminal = next_moves[distance_from_self_to_criminal.index(min(distance_from_self_to_criminal))]
        #points_away_from_criminal = [distance.euclidean(cell, closest_criminal) for cell in next_moves]

        ###dist_between_criminal_and_goal = [distance.euclidean(distance.euclidean(cell, closest_criminal), distance.euclidean(cell, self.current_route_goal()))
        ###for cell in next_moves]
        ###cell_to_walk_to = next_moves[next_moves.index(max(dist_between_criminal_and_goal))]
        ###print("debug: " + next_moves.index(max(dist_between_criminal_and_goal)))
        ###print("cell_to_walk_to: " + str(cell_to_walk_to))

        ###self._walk_to(cell_to_walk_to)


        best_utility = -math.inf
        best_cell = (0, 0)

        # get the best utility based on larger distance from cell to criminals and shorter distance from cell to goal
        for cell in next_moves:
            utility = 0
            dist_to_criminals = 0

            # calculate total distance from cell to criminals
            for criminal in criminals_nearby:
                dist_to_criminals += distance.euclidean(cell, criminal.pos)

            # calculate utility
            # set 0.5 since to avoid criminals is more important
            utility = dist_to_criminals - 0.5 * distance.euclidean(cell, goal)
            if utility > best_utility:
                best_utility = utility
                best_cell = cell

        #print("best_cell: " + str(best_cell))

        if best_cell != self.pos:
            self.environment.grid.move_agent(self, best_cell)
            # print("pos: " + str(self.pos))
            return True
        else:
            return False


            #take the cell that minimizes the distance to my goal but that maxmizes my min distance from criminal




        #random.shuffle(next_moves)
        #for cell in next_moves:
         #   if sum(agent in self.memory for agent in self.environment.grid.get_cell_list_contents(cell)):
          #      continue

           # else:
                # Move to this cell where there is nobody we remember
            #    self.walk_to(self, cell)
             #   return True




    def add_to_memory(self, agent):
        """Add a criminal to the civilian's memory, no repeats.

        :param agent: An agent that will be avoided in the future.
        """
        #assert(isinstance(agent, Criminal))
        self.memory.append(agent)
        self.memory = list(set(self.memory))  # remove repeats

        # Call police through the environment
        self.environment.call_police(self, agent)
        return

    def add_to_building_memory(self, building):
        """Add a building to the civilian's momory.
        :param building: An instance of the class Building that the agent will memorize.
        """
        #assert(isinstance(building, Building))
        self.building_memory.append(building)
        self.building_memory = list(set(self.building_memory)) # remove repeats


    def walk_to_avoid(self, coordinates, role_to_avoid):
        """Walk one cell towards a set of coordinates, using only cardinal directions (North/South or West/East).
           Avoid specified roles.
           :param coordinates: The coordinate tuple the agent will move towards.
           :param role_to_avoid: A list of types of classes the agent will avoid.
        """
        possible_moves = self.environment.grid.get_neighborhood(self.pos, moore=False, include_center=True)
        next_moves = []

        # add the cells without roles to avoid to next_moves
        for cell in possible_moves:
            contents = self.environment.grid.get_cell_list_contents(cell)
            if sum([type(agent) in role_to_avoid for agent in contents]) == 0:
                next_moves.append(cell)

        random.shuffle(next_moves)

        best_distance = 0
        best_cell = (0, 0)

        # get the best utility based on larger distance from cell to criminals and shorter distance from cell to goal
        for cell in next_moves:
            # choose the shortest distance
            dist = distance.euclidean(cell, coordinates)
            if dist < best_distance:
                best_distance = dist
                best_cell = cell

        self.environment.grid.move_agent(self, best_cell)


class Police(Agent):
    """
    A subclass of Agent for Police types. 

    """

    def __init__(self, pos, model, resources=[], uid=None, network=None, hierarchy=None, history_self=[],
                 history_others=[], policy=None, allies=[], utility = [], competitors=[], residence=None):
        """
        :param pos: The position tuple of the agent.
        :param model: The environment the agent is in.
        :param resources: The amount of each asset the agent has.
        :param uid: The unique ID for the agent.
        :param network: The original network id where the agent is nested in.
        :param hierarchy: The level in organization (low, medium, high, etc).
        :param history_self: The agents' memory of history of itself.
        :param history_others: The agents' memory of history of others.
        :param policy: The agent's policy.
        :param residence: The living places of the agent.
        :param allies: The list of agents who are the allies of the agent.
        :param utility: The history of the utility of the agent.
        :param competitors: The list of agents who are the competitors of the agent.
        """
        super().__init__(self, pos, model, resources, uid, network, hierarchy, policy, residence=None)
        self.pos = pos
        self.environment = model
        self.resources = resources
        self.uid = uid
        self.history_self = history_self
        self.history_others = history_others
        self.allies = allies
        self.competitors = competitors
        self.dispatch_coordinates = None
        self.target = None
        self.vision = random.randint(1, model.config['agent_vision_limit'])
        self.pd = None
        self.arrest_radius = model.config['police_arrest_radius']
        self.utility = utility

    def __str__(self):
        return "Police " + str(self.uid)

    def step(self):
        """One time unit in the simulation, decide what actions to take."""

        # Check if this Police has an assignment
        if self.dispatch_coordinates is not None:
            criminal_in_sight = self.scan_for_target()  # update dispatch coordinates if this police can see their target
            at_dispatch_coordinates = self.walk_to(self.dispatch_coordinates) # walk towards the dispatch_coordinates

            # if target is within the police's arrest radius, the police will capture him
            if self.target.pos in self.environment.grid.get_neighborhood(self.pos, moore=True, include_center=True, radius=self.arrest_radius):
                print("Attempting arrest at {0} for criminal at {1}".format(self.pos, self.target.pos))
                self.environment.attempt_arrest(criminal=self.target, police=self)
                return

            if at_dispatch_coordinates:
                # Arrived at crime scene / target coordinates
                self.initiate_investigation()

            elif not criminal_in_sight:
                # Did not arrive at crime scene, search for target again on the way there.
                self.scan_for_target()
        else:
            # No dispatch assignment, patrol randomly
            # TODO Patrol neighborhood, not randomly
            self.random_move()

    def initiate_investigation(self):
        """
        The police will start his investigation when he arrives at the crime scene.
        """
        #Check if target is in same cell - which should be the dispatch coordinates.
        print("Officer arrived at the crime scene")
#        unfiltered_neighbors = self.environment.grid.get_neighbors(self.pos, moore=True, include_center=True, radius=self.arrest_radius)
#        neighbors = list(filter(lambda agent: type(agent) is Criminal, unfiltered_neighbors))
#        if self.target in neighbors:
#            # Target is within the police's arrest radius
#            # if self.arrest_radius is 0, then the police and the target is in the same cell
#
#            #TODO :
#            #Choose utility-maximizing arrest:
#
#            calculate_utility = lambda self, agent: b.utility_function(self, agent) - b.cost_function(agent=self, target=agent)
#            possible_utility = [calculate_utility(self, neighbor) for neighbor in neighbors]
#
#            criminal_target = neighbors[possible_utility.index(max(possible_utility))]
#            potential_cost = b.cost_function(self, criminal_target)
#            potential_utility= b.utility_function(self, criminal_target)
#
#            print("Attempting arrest at {0} for criminal at {1}".format(self.pos, criminal_target.pos))
#
#
#            if self.environment.attempt_arrest(criminal=criminal_target, police=self):
#                #Update utility and pass;
#                self.utility.append(potential_utility - potential_cost)
#                pass
        if self.target.pos in self.environment.grid.get_neighborhood(self.pos, moore=True, include_center=True, radius=self.arrest_radius):
            print("Attempting arrest at {0} for criminal at {1}".format(self.pos, self.target.pos))
            self.environment.attempt_arrest(criminal=self.target, police=self)

        elif not self.scan_for_target():
            # Drop Investigation
            # TODO A timer for patience? i.e. moving randomly until patience runs out.
            print("Officer could not find Criminal %s, they give up!" % self.target.uid)
            # Update utility and cost of not making arrest
            # self.utility.append(-potential_cost)
            self.drop_investigation()


    def drop_investigation(self):
        """Remove from other police officer's who are chasing the same target."""
        self.environment.grid.move_agent(self, self.pd.pos)  # police goes to the station with criminal, for processing



    def scan_for_target(self):
        """Check around officer if the target is in sight.
        :return: True if target is in the vision of the police. False otherwise."""
        # FIXME Scanning is broken!
        # FIXME Maybe use the model to determine distance instead of scanning - this includes opportunity for police to miss \
        # FIXME the target or something - gives control to the model?
        agents = self.environment.grid.get_neighbors(self.pos, moore=True, include_center=True, radius=self.vision)
        for agent in agents:
            if agent is self.target:
                #print("Spotted target!")
                self.dispatch_coordinates = agent.pos
                return True
        # Target not spotted, fail
        return False

#    def walk_to_avoid(self, coordinates, role_to_avoid):
#        """Walk one cell towards a set of coordinates, using only cardinal directions (North/South or West/East"""
#        x, y = self.pos  # Current position
#        x_target, y_target = coordinates  # Target position
#        dx, dy = x_target - x, y_target - y  # Distance from target in terms of x/y
#        next_moves = self.environment.grid.get_neighborhood(self.pos, moore=False, include_center=True)
#        next_moves = [cell for cell in filter(lambda x: self.environment.grid.can_agent_occupy_cell(x), next_moves)]
#        random.shuffle(next_moves)
#
#        # Scale dx/dy to -1/1 for use as coordinate move
#        if dx != 0 and dy != 0:
#            # Agent needs to go vertical and horizontally, choose one randomly
#            if random.random() < 0.5:
#                # The agents or buildings in the next position
#                agents_buildings = self.environment.grid.get_cell_list_contents((dx / abs(dx) + x, y))
#                # Check if the next position is avoided
#                avoid = sum([type(agent) in role_to_avoid for agent in agents_buildings])
#                if not avoid:
#                    # Move horizontally
#                    dest_x = int(x + dx / abs(dx))
#                    dest_y = int(y)
#                else:
#                    # move randomly and avoid the specified roles
#                    dest_x, dest_y = self.random_move_and_avoid_role(role_to_avoid)
#
#            else:
#                agents_buildings = self.environment.grid.get_cell_list_contents((x, dy / abs(dy) + y))
#                avoid = sum([type(agent) in role_to_avoid for agent in agents_buildings])
#                if not avoid:
#                    # Move vertically
#                    dest_y = int(y + dy / abs(dy))
#                    dest_x = int(x)
#                else:
#                    dest_x, dest_y = self.random_move_and_avoid_role(role_to_avoid)
#
#        elif dx == 0 and dy == 0:
#            # Agent is at destination
#            return True
#        elif dx == 0:
#            agents_buildings = self.environment.grid.get_cell_list_contents((x, dy / abs(dy) + y))
#            avoid = sum([type(agent) in role_to_avoid for agent in agents_buildings])
#            if not avoid:
#                # Agent only needs to move vertically
#                dest_y = int(y + dy / abs(dy))
#                dest_x = int(x)
#            else:
#                dest_x, dest_y = self.random_move_and_avoid_role(role_to_avoid)
#
#        elif dy == 0:
#            agents_buildings = self.environment.grid.get_cell_list_contents((x, dy / abs(dy) + y))
#            avoid = sum([type(agent) in role_to_avoid for agent in agents_buildings])
#            if not avoid:
#                # Agent only needs to move horizontally
#                dest_x = int(x + dx / abs(dx))
#                dest_y = int(y)
#            else:
#                dest_x, dest_y = self.random_move_and_avoid_role(role_to_avoid)
#
#        self.environment.grid.move_agent(self, (dest_x, dest_y))
#        # FIXME Check if there?
#        return x_target == dest_x and y_target == dest_y
