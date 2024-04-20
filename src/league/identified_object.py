class IdentifiedObject:
    """an abstract class including the object id"""

    def __init__(self, oid):
        self._oid = oid

    @property
    def oid(self):
        return self._oid

    def __eq__(self, other):
        """two IdentifiedObjects are equal
        if they have the same type and the same oid"""
        if self is other:
            return True
        if type(self) == type(other):
            return self.oid == other.oid

    def __hash__(self):
        """return hash code based on object's oid"""
        return hash(self.oid)
