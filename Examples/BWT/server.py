"""The server.py controls macro parameters for simulations. Including data collection for each episode, etc."""
# import os 
# os.chdir("C:\\Users\\Administrator.SKY-20991225ONL\\Desktop\\ABM-example-BWT")
from Base.batch import batchManager
import logging
from timeit import default_timer as timer

logging.basicConfig(level=logging.INFO, filename='ABM.log')



num_steps = 5000
num_episodes = 50



data_to_collect = {
    # Individual, Role, and Custom Group Data Collecting
    # Each should be a list of specifications
    "individuals": [
        # Add a dictionary for each individual/attribute to monitor
        {
            "uid": None,         # None defaults to UID 0
            "role": "civilians",          # civilians/police/criminals
            "attribute": "resources",   # MUST BE SPECIFIED
            "frequency": "step",  # step/episodic
        }
    ],

    "roles": [
        # Collect the attributes for all agents within the specified role
        # Add more dictionaries to collect other agent roles or attributes
        {
            "role": "civilians",
            "attribute": "pos",
            "frequency": "step"
        },
        {
            "role": "criminals",     # Role, as a string
            "attribute": "do_crime",  # Attribute, as a string
            "frequency": "step"  # "step" or "episodic"
        },
#        {
#            "role": "residences",     # Role, as a string
#            "attribute": "attractiveness",  # Attribute, as a string
#            "frequency": "step"  # "step" or "episodic"
#        }
        {
                "role": "police",
                "attribute": "pos",
                "frequency": "step"},
        
        {
                "role": "criminals",
                "attribute": "pos",
                "frequency": "step"},
        
        {
                "role": "criminals",
                "attribute": "crime_propensity",
                "frequency": "step"}
    ],

    "groups": [
        # Only agents matching these qualifiers, in this order, will have the specified attribute recorded
        # Leave as None to NOT exclude agents based on that criteria
        {
            "role_qualifier_list": ["criminals"],  # List of roles as strings, None = ALL roles
            "uid_qualifier_list": None,  # List of uid's as integers, None = ALL agents
            "attribute_qualifier_list": None,
#                [a
#                # Add as many qualifiers as desired!
#                # None = No attribute qualifiers
#                {
#                    "attribute": "network",    # Attribute to look for as string
#                    "value_list": [0]  # Values the attribute can take on
#                }
#            ],
            "attribute": "utility",  # attribute to be collected
            "frequency": "step"  # step or episodic
        }
    ]
}

print("Starting server.")

bm = batchManager(num_episodes=num_episodes,
                  num_steps=num_steps,
                  data_to_collect=data_to_collect)

start_time = timer()
bm.start()

bm.dm.data_in_sim[0].data_to_collect['individuals'][0]['data']
bm.dm.data_in_sim[1].data_to_collect['individuals'][0]['data']

<<<<<<< HEAD
df = bm.dm.data_in_sim[0].data_to_collect['roles'][0]['data']

=======
>>>>>>> 5f75cb2d4d25500bd8bfa1c37c1ee7455eb1e12b

#For recording simulation run time
#dt = timer()-start_time

#print(dt) #19.35 is the time to beat
# All Data lies in  a list of [data_lists['individuals'/'groups'/'types'][specification_index]['data']]



