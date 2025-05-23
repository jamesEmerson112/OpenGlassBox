import pytest

class Resource:
    MAX_CAPACITY = 2**32 - 1

    def __init__(self, resource_type, amount=0, capacity=None):
        self._type = resource_type
        self.m_type = resource_type
        self.m_amount = amount
        self.m_capacity = capacity if capacity is not None else Resource.MAX_CAPACITY

    def type(self):
        return self._type

class Resources:
    def __init__(self):
        self.m_bin = []

    def isEmpty(self):
        return all(r.m_amount == 0 for r in self.m_bin)

    def findResource(self, name):
        for r in self.m_bin:
            if r.type() == name:
                return r
        return None

    def hasResource(self, name):
        return self.findResource(name) is not None

    def addResource(self, name, amount):
        r = self.findResource(name)
        if r is None:
            r = Resource(name, amount)
            self.m_bin.append(r)
        else:
            r.m_amount += amount
        return r

    def removeResource(self, name, amount):
        r = self.findResource(name)
        if r is None:
            return False
        if r.m_amount < amount:
            r.m_amount = 0
        else:
            r.m_amount -= amount
        return True

    def getAmount(self, name):
        r = self.findResource(name)
        return r.m_amount if r else 0

    def getCapacity(self, name):
        r = self.findResource(name)
        return r.m_capacity if r else 0

    def setCapacity(self, name, capacity):
        r = self.findResource(name)
        if r is None:
            r = Resource(name, 0, capacity)
            self.m_bin.append(r)
        else:
            r.m_capacity = capacity
            if r.m_amount > r.m_capacity:
                r.m_amount = r.m_capacity

    def setCapacities(self, other):
        for r in other.m_bin:
            self.setCapacity(r.type(), r.m_capacity)

    def addResources(self, other):
        if self is other:
            return
        for r in other.m_bin:
            self.addResource(r.type(), r.m_amount)

    def removeResources(self, other):
        if self is other:
            return
        for r in other.m_bin:
            self.removeResource(r.type(), r.m_amount)

    def canAddSomeResources(self, other):
        if self is other:
            return False
        for r in other.m_bin:
            mine = self.findResource(r.type())
            if mine and mine.m_amount < mine.m_capacity:
                return True
        return False

    def transferResourcesTo(self, other):
        for r in self.m_bin:
            other_r = other.findResource(r.type())
            if other_r is None:
                other_r = Resource(r.type(), 0)
                other.m_bin.append(other_r)
            transfer_amount = min(r.m_amount, other_r.m_capacity - other_r.m_amount)
            other_r.m_amount += transfer_amount
            r.m_amount -= transfer_amount

def test_constructor():
    house = Resources()
    assert len(house.m_bin) == 0
    assert house.isEmpty() is True

def test_empty_collection():
    house = Resources()
    assert house.findResource("people") is None
    assert house.hasResource("people") is False

    house.removeResource("people", 10)
    assert len(house.m_bin) == 0
    assert house.isEmpty() is True

    assert house.canAddSomeResources(house) is False
    assert house.getAmount("people") == 0
    assert house.getCapacity("people") == 0

    house.removeResources(house)
    assert house.getAmount("people") == 0
    assert house.getCapacity("people") == 0

def test_nominal():
    house = Resources()
    r1 = house.addResource("people", 0)
    assert len(house.m_bin) == 1
    assert r1.type() == "people"
    assert house.m_bin[0].type() == "people"
    assert house.getAmount("people") == 0
    assert house.getCapacity("people") == Resource.MAX_CAPACITY
    assert house.isEmpty() is True
    assert house.canAddSomeResources(house) is False

    r2 = house.addResource("car", 2)
    assert len(house.m_bin) == 2
    assert r2.type() == "car"
    assert house.m_bin[0].type() == "people"
    assert house.m_bin[1].type() == "car"
    assert house.getAmount("people") == 0
    assert house.getAmount("car") == 2
    assert house.getCapacity("people") == Resource.MAX_CAPACITY
    assert house.getCapacity("car") == Resource.MAX_CAPACITY
    assert house.isEmpty() is False
    assert house.canAddSomeResources(house) is False

    house.removeResources(house)
    assert house.getAmount("people") == 0
    assert house.getAmount("car") == 2
    house.addResources(house)
    assert house.getAmount("people") == 0
    assert house.getAmount("car") == 2

    r3 = house.addResource("car", 8)
    assert len(house.m_bin) == 2
    assert r3.type() == "car"
    assert house.m_bin[0].type() == "people"
    assert house.m_bin[1].type() == "car"
    assert house.getAmount("people") == 0
    assert house.getAmount("car") == 10
    assert house.getCapacity("people") == Resource.MAX_CAPACITY
    assert house.getCapacity("car") == Resource.MAX_CAPACITY
    assert house.isEmpty() is False

    res = house.removeResource("car", 5)
    assert res is True
    assert len(house.m_bin) == 2
    assert house.m_bin[0].type() == "people"
    assert house.m_bin[1].type() == "car"
    assert house.getAmount("people") == 0
    assert house.getAmount("car") == 5
    assert house.getCapacity("people") == Resource.MAX_CAPACITY
    assert house.getCapacity("car") == Resource.MAX_CAPACITY
    assert house.isEmpty() is False

    assert house.getCapacity("car") == Resource.MAX_CAPACITY
    house.setCapacity("car", 2)
    assert house.getCapacity("car") == 2
    assert house.getAmount("car") == 2

    caps = Resources()
    caps.setCapacity("car", 20)
    caps.setCapacity("people", 10)
    caps.setCapacity("trash", 10)
    assert len(caps.m_bin) == 3
    assert caps.m_bin[0].type() == "car"
    assert caps.m_bin[1].type() == "people"
    assert caps.m_bin[2].type() == "trash"
    assert caps.getCapacity("car") == 20
    assert caps.getCapacity("people") == 10
    assert caps.getCapacity("trash") == 10

    assert len(house.m_bin) == 2
    assert house.getCapacity("car") == 2
    assert house.getCapacity("people") == Resource.MAX_CAPACITY
    house.setCapacities(caps)
    assert len(house.m_bin) == 3
    assert house.getCapacity("car") == 20
    assert house.getCapacity("people") == 10
    assert house.getCapacity("trash") == 10

    toAdd = Resources()
    toAdd.addResource("car", 5)
    toAdd.addResource("people", 2)
    toAdd.addResource("trash", 10)
    assert toAdd.getAmount("car") == 5
    assert toAdd.getAmount("people") == 2
    assert toAdd.getAmount("trash") == 10

    assert house.getAmount("car") == 2
    assert house.getAmount("people") == 0
    house.addResources(toAdd)
    assert house.getAmount("car") == 7
    assert house.getAmount("people") == 2
    assert house.getAmount("trash") == 10
    house.removeResources(toAdd)
    assert house.getAmount("car") == 2
    assert house.getAmount("people") == 0
    assert house.getAmount("trash") == 0

# TODO: Port and implement the more complex tests (canAddSomeResources, transferResourcesTo)
