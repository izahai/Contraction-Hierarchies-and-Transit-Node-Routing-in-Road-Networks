class Vertex:
    def __init__(self):
        self.idx : int = None
        
        self.importance : int = None
        self.contractionOrder : int = None
        self.contracted = False
        
        self.isTransitNode = False
