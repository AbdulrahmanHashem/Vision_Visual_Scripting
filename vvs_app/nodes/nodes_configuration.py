LISTBOX_MIMETYPE = "application/x-item"


# Logic = {}
# Math = {}
# Process = {}

FUNCTIONS = {}
VARIABLES = {}
EVENTS = {}


######################


class ConfException(Exception):
    pass


class InvalidNodeRegistration(ConfException):
    pass


class NodeTypeNotRegistered(ConfException):
    pass


######################


def regester_Node(Node_Class):
    Node_Type = len({**FUNCTIONS, **VARIABLES, **EVENTS})
    Node_Class.node_type = Node_Type

    if Node_Class.category == "FUNCTION":
        FUNCTIONS[Node_Type] = Node_Class
    elif Node_Class.category == "EVENT":
        EVENTS[Node_Type] = Node_Class
    elif Node_Class.category == "VARIABLE":
        VARIABLES[Node_Type] = Node_Class


######################

def get_node_by_type(node_type):
    NODES = {**FUNCTIONS, **VARIABLES, **EVENTS}
    if node_type not in NODES:
        raise NodeTypeNotRegistered("node_type '%d' is not registered" % node_type)
    else:
        return NODES[node_type]

######################


##############################################################################################################
##############################################################################################################

# User Variables setup


######################

# User Events setup


##############################################################################################################
##############################################################################################################


# This comment was originally here before it was removed for better init performance and moved
# import all nodes and register them
# from vvs_app.nodes import *
