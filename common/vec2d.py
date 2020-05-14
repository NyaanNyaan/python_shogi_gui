class Vec(list):
    def __add__(self,other):
        if(type(other) in (Vec, list) and len(self) == len(other)):
            return Vec([ int(x + y) for x, y in zip(self, other)])
        else:
            raise ValueError
    __radd__ = __add__

    def __sub__(self,other):
        if(type(other) in (Vec, list) and len(self) == len(other)):
            return Vec([ int(x - y) for x, y in zip(self, other)])
        else:
            raise ValueError
    __rsub__ = __sub__
    
    def __mul__(self,other):
        if(type(other) in (int,float)):
            return Vec([ int(x * other) for x in self])
        elif(type(other) in (Vec, list) and len(self) == len(other)):
            return Vec([ int(x * y) for x, y in zip(self, other)])
        else:
            raise ValueError
    __rmul__ = __mul__