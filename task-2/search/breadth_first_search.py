#
# This file is based on pyperplan
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
#

"""
Implements the breadth first search algorithm.
"""

from collections import deque
import logging

from . import searchspace


def breadth_first_search(planning_task):
    """
    Searches for a plan on the given task using breadth first search and
    duplicate detection.

    @param planning_task: The planning task to solve.
    @return: The solution as a list of Operators or None if the task is
    unsolvable.
    """
    # counts the number of loops (only for printing)
    iteration = 0

    # fifo-queue storing the nodes which are next to explore
    queue = deque()

    # Add to the queue the root node (i.e. the node that corresponds to the
    # initial state). The root node is a SearchNode instance with the following
    # attributes:
    # state: equals to the initial state of the planning_task
    # parent (node): None
    # action (that produced the initial state): None
    # g (The path length of the root node in the count of applied operators): 0
    # See searchspace.py for more details.
    queue.append(searchspace.make_root_node(planning_task.initial_state))

    # A set storing the explored nodes, used for duplicate detection
    # Initially, the set contains only the initial state
    closed = {planning_task.initial_state}

    # Iterate over the queue as long as the queue contains items to pop
    while queue:
        # Step 1
        # Increase the number of iterations
        iteration += 1

        logging.debug(
            "breadth_first_search: Iteration %d, #unexplored=%d"
            % (iteration, len(queue))
        )

        # Step 2
        # Get the next node that is stored in the queue, whose neighbor
        # nodes will be visited now
        node = None 
        node = queue.popleft()

        # Step 3
        # If the goal of the planning task has been reach in the state
        # of the node, then extract the solution and return it.
        # HINT 1: Access the state attribute of the node that represents 
        #         the state in the node
        # HINT 2: Use a Task method that you implemented to check if
        #         the goal of the planning task has been reached at the 
        #         the state in the node
        # HINT 3: Use the  SearchNode method extract_solution() to extract
        #         and return the solution to the task (in case the goal has
        #         been achieved)
        if planning_task.goal_reached(node.state):
            logging.info("Goal reached. Start extraction of solution.")
            logging.info("%d Nodes expanded" % iteration)
            return node.extract_solution()

        # Step 4 
        # Create and add each neighbor node of the node to the queue, if the 
        # neighbor node hasn't been visited yet.
        # HINT 1: You can create neighbor nodes, using the SearchNode method 
        #         make_child_node()
        # HINT 2: Use a Task method that you implemented to retrieve the 
        #         all the possible neighbor (next) states that can be reached
        #         after the state in the node. Information stored in the 
        #         retrieved neighbor states, can be used to create a neighbor 
        #         node with make_child_node()
        # HINT 3: Only add a newly created neighbor node to the queue, if the 
        #         state in the neighbor node has not been visited yet, i.e. 
        #         it is not the set "closed"
        # HINT 4: If a newly created neighbor node has been added to the queue,
        #         add its state to the set "closed", to avoid duplicate visits
        for operator, successor_state in planning_task.get_successor_states(node.state):
            # duplicate detection
            if successor_state not in closed:
                queue.append(
                    searchspace.make_child_node(node, operator, successor_state)
                )
                # remember the successor state
                closed.add(successor_state)
    
    # If no solution has been extracted and returned after iterating over the whole
    # queue, the function returns None, considering that the task is unsolvable
    logging.info("No operators left. Task unsolvable.")
    logging.info("%d Nodes expanded" % iteration)
    return None
