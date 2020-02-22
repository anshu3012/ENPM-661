import numpy as np  # Used to store the digits in an array
import os  # Used to delete the file created by previous running of the program


class Node: 
    def __init__(self, node_no, data, parent, act, cost): # Node() will be the object of the class. Creating a linked list 
        self.data = data
        self.parent = parent
        self.act = act
        self.node_no = node_no
        self.cost = cost

def get_initial(): #getting data from user 
    print("Enter number from 0-8")
    initial_state = np.zeros(9)
    for i in range(9):
        states = int(input("Enter the " + str(i + 1) + " number: "))
        if states < 0 or states > 8:
            print("Enter states which are [0-8]")
            exit(0)
        else:
            initial_state[i] = np.array(states)
    return np.reshape(initial_state, (3, 3))


def find_index(puzzle): 
    i, j = np.where(puzzle == 0) # finding the position of 0
    i = int(i)
    j = int(j)
    return i, j


def move_left(data):
    i, j = find_index(data)
    if j == 0:
        return None
    else:
        temp_arr = np.copy(data)
        temp = temp_arr[i, j - 1] #since left 
        temp_arr[i, j] = temp
        temp_arr[i, j - 1] = 0 #interchanging of element and 0
        return temp_arr


def move_right(data):
    i, j = find_index(data)
    if j == 2:
        return None
    else:
        temp_arr = np.copy(data)
        temp = temp_arr[i, j + 1] #since right
        temp_arr[i, j] = temp
        temp_arr[i, j + 1] = 0
        return temp_arr


def move_up(data):
    i, j = find_index(data)
    if i == 0:
        return None
    else:
        temp_arr = np.copy(data)
        temp = temp_arr[i - 1, j] #since up
        temp_arr[i, j] = temp
        temp_arr[i - 1, j] = 0
        return temp_arr


def move_down(data):
    i, j = find_index(data)
    if i == 2:
        return None
    else:
        temp_arr = np.copy(data)
        temp = temp_arr[i + 1, j] #since down 
        temp_arr[i, j] = temp
        temp_arr[i + 1, j] = 0
        return temp_arr


def move_tile(action, data):
    if action == 'up':
        return move_up(data)
    if action == 'down':
        return move_down(data)
    if action == 'left':
        return move_left(data)
    if action == 'right':
        return move_right(data)
    else:
        return None


def print_states(list_final):  
    print("printing final solution")
    for l in list_final:
        print("Move : " + str(l.act) + "\n" + "Result : " + "\n" + str(l.data) + "\t" + "node number:" + str(l.node_no))
        """list_final is a list of objects that l iterates through and hence that's why l is able to access the values of class Node"""


def write_path(list_final):  # The nodes that were selected to arrive at goal 
    if os.path.exists("nodePath.txt"):
        os.remove("nodePath.txt")

    f = open("nodePath.txt", "a")
    for k in list_final:
        for g in range(len(k.data)):
            for h in range(len(k.data)):
                q=str(k.data[h][g])
                e=float(q)
                f.write(f'{int(e)} ')
        f.write("\n")       

    f.close()


def write_node_explored(explored):  # All the nodes explored
    if os.path.exists("Nodes.txt"):
        os.remove("Nodes.txt")

    f = open("Nodes.txt", "a")
    for element in explored:
        for i in range(len(element)):
            for j in range(len(element)):
                z=str(element[j][i])
                u=float(z)
                f.write(f'{int(u)} ')
        
        f.write("\n")
    f.close()


def write_node_info(visited):  #   First column: Node Index Second Column: Parent Node Index Third Coloumn :Cost (since given in template)
    if os.path.exists("NodesInfo.txt"):
        os.remove("NodesInfo.txt")

    f = open("NodesInfo.txt", "a")
    for n in visited:
        if n.parent is not None:
            f.write(str(n.node_no) + " " + str(n.parent.node_no) + "\t" + str(n.cost) + "\n")
    f.close()


def path(node):  # To find the path from the goal node to the starting node
    p = []  # Empty list
    p.append(node)
    parent_node = node.parent #node is child_node object which can access data of class Node
    while parent_node is not None:
        p.append(parent_node)
        parent_node = parent_node.parent # using the concept of linked lists, parent_node.parent points to the next node in the linked list
    return list(reversed(p))  
    """list() converts the the iterable passed to it to a list
    reversed() method returns an iterator that accesses the given sequence in the reverse order."""

def exploring_nodes(node):
    print("Exploring Nodes")
    actions = ["down", "up", "left", "right"]
    goal_node = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
    """Instance of a class (object) is being passed as a list. node_q is a list having only an object of class Node defined earlier.
     Since node_q[0] has only one elelmt in the list,which is the object of class Node, the object has be to accessed as node_q[0]"""
    node_q = [node]
    final_nodes = []
    visited = []
    final_nodes.append(node_q[0].data.tolist())  # Only writing data of nodes in seen
    node_counter = 0  # To define a unique ID to all the nodes formed

    while node_q:
        current_root = node_q.pop(0)  
        """ assigning the object in node_q to current_root.
 Now that the object has been assigned to current_root, current_root can be used to access the variales in class Node"""
        if current_root.data.tolist() == goal_node.tolist(): 
            """ This is the case when user input data is [1 2 3;4 5 6;7 8 0] """
            print("Goal reached")
            return current_root, final_nodes, visited

        for move in actions:
            temp_data = move_tile(move, current_root.data)
            if temp_data is not None:
                node_counter += 1
                child_node = Node(node_counter, np.array(temp_data), current_root, move, 0)  
                """Create a child node which again is an object since it's of the form  Node(). 
                Now since it also an object of the Node class, it can acess data in that class and manipulaye it"""

                if child_node.data.tolist() not in final_nodes:  # Add the child node data in final node list.
                 
                    node_q.append(child_node)
                    """ appending the child node to node_q list bc if we don't append the child node, the while loop will exit"""
                    final_nodes.append(child_node.data.tolist())
                    """appending child nodes as visual data"""
                    visited.append(child_node)
                    if child_node.data.tolist() == goal_node.tolist():
                        print("Goal_reached") 
                        """ This is the result when you input any solvable matrix except 1 2 3;4 5 6;7 8 0"""
                        return child_node, final_nodes, visited
    return None, None, None  # return statement if the goal node is not reached


def check_correct_input(l): #check if data input by the user is correct or not 
    array = np.reshape(l, 9)
    for i in range(9):
        counter_appear = 0
        f = array[i]
        for j in range(9):
            if f == array[j]:
                counter_appear += 1
        if counter_appear >= 2:
            print("invalid input, same number entered 2 times")
            exit(0)


def check_solvable(g): #check if it's solvable 
    arr = np.reshape(g, 9)
    counter_states = 0
    for i in range(9):
        if not arr[i] == 0:
            check_elem = arr[i]
            for x in range(i + 1, 9):
                if check_elem < arr[x] or arr[x] == 0:
                    continue
                else:
                    counter_states += 1
    if counter_states % 2 == 0:
        print("The puzzle is solvable, generating path")
    else:
        print("The puzzle is insolvable, still creating nodes")

k = get_initial()

check_correct_input(k)
check_solvable(k)

root = Node(0, k, None, None, 0)
goal, s, v = exploring_nodes(root)

if goal is None and s is None and v is None:
    print("Goal State could not be reached, Sorry")
else:
    print_states(path(goal))
    write_path(path(goal))
    write_node_explored(s)
    write_node_info(v)
