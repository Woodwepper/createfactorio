from enum import Enum


class ConstructionType(Enum):
    FACTORY = "factory"
    MODULE = "module"
    RESOURCE_NODE = "resource_node"
    SU_PRODUCER = "su_producer"
