from enum import Enum


class RoleType(Enum):
    approver = "approver"
    complainer = "complainer"
    admin = "admin"


class State(Enum):
    approved = "Approved"
    pending = "Pending"
    rejected = "Rejected"
