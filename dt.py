from typing import List

class DecisionTreeClassifier:
    max_depth = 0
    tree = None 
    
    def __init__(self, max_depth: int):
        self.max_depth = max_depth
        self.tree = BinaryTree()
        
    def fit(self, X: List[List[float]], y: List[int]):
        self.fitRecursive(X,y,self.tree.root)      
        
    def fitRecursive(self,X: List[List[float]], y: List[int], node):       
        gini = self.calculatedGini(y)
        maxInformationGain = 0
        left = list()
        right = list()
        leftAtt = list(list())
        rightAtt = list(list())
        split = 0
        atts_index = 0
        #calculate info gain for attributes
        for i in range(0,len(X)):
            for j in range(0,len(X[0])):
                leftTarget = list()
                rightTarget = list()
                leftAttribute = list(list())
                rightAttribute = list(list()) 
                for k in range(0,len(y)):
                    if(X[i][j] > X[k][j]):
                        leftTarget.append(y[k])
                        leftAttribute.append(X[k][:])
                    else:
                        rightTarget.append(y[k])
                        rightAttribute.append(X[k][:])
                      
                if(len(rightTarget)>0 and len(leftTarget)>0):
                    averageGini = ( len(leftTarget)/len(y) * self.calculatedGini(leftTarget) + len(rightTarget)/len(y) * self.calculatedGini(rightTarget) )
                    informationGain = gini - averageGini
                    if(informationGain >= maxInformationGain):
                        maxInformationGain = informationGain
                        left = leftTarget
                        right = rightTarget
                        split = X[i][j]
                        leftAtt = leftAttribute
                        rightAtt = rightAttribute
                        atts_index = j
        #root
        if(self.tree.root == None):
            
            self.tree.addRoot(BinaryTree.Node(split,atts_index))
            node = self.tree.root
            node.setDepth(0)
            #Check leaf node 
            if(left.count(left[0]) == len(left)):
                node.setLeft(BinaryTree.Node(None,atts_index))
                node.left.setDepth(node.depth + 1)
                node.left.target = left[0]
            #Check leaf node 
            if(right.count(right[0]) == len(right)):
                node.setRight(BinaryTree.Node(None,atts_index))
                node.right.setDepth(node.depth + 1)
                node.right.target = right[0]
            
            if(left.count(left[0]) != len(left)):
                node.setLeft(BinaryTree.Node(split,atts_index))
                node.left.setDepth(node.depth + 1)
                self.fitRecursive(leftAtt,left,node.left)
                
            if(right.count(right[0]) != len(right)):
                node.setRight(BinaryTree.Node(split,atts_index))
                node.right.setDepth(node.depth + 1)
                self.fitRecursive(rightAtt,right,node.right)   

        else:
            #check for max depth
            if(node.depth != self.max_depth):
                node.setSplit(split)
                node.setAtt(atts_index)
                #Check leaf node
                if(left.count(left[0]) == len(left) and len(left)>0 ):
                    node.setLeft(BinaryTree.Node(None,atts_index))
                    node.left.setDepth(node.depth + 1)
                    node.left.target = left[0]
                #Check leaf node    
                if(right.count(right[0]) == len(right) and len(right)>0 ):
                    node.setRight(BinaryTree.Node(None,atts_index))
                    node.right.setDepth(node.depth + 1)
                    node.right.target = right[0]
                    
                if(left.count(left[0]) != len(left) and len(left)>0 ):
                    node.setLeft(BinaryTree.Node(split,atts_index))
                    node.left.setDepth(node.depth + 1)
                    frequent_target = left[0]
                    for i in left:
                        curr = left.count(i)
                        if(curr > left.count(frequent_target)):
                            frequent_target = curr

                    node.target = frequent_target
                    if(len(left)>1):
                        self.fitRecursive(leftAtt,left,node.left)
                    
                if(right.count(right[0]) != len(right) and len(right)>0 ):
                    node.setRight(BinaryTree.Node(split,atts_index))
                    node.right.setDepth(node.depth + 1)
                    frequent_target = right[0]
                    for i in right:
                        curr = right.count(i)
                        if(curr > right.count(frequent_target)):
                            frequent_target = curr

                    node.target = frequent_target
                    if(len(right)>1):
                        self.fitRecursive(rightAtt,right,node.right)
    
        
    def predict(self, X: List[List[float]]):
        classifications = list()
        for c in X:
            node = self.tree.root
            while(node.value != None): #leaf node values are None
                #left
                if(c[node.attribute] < node.value):
                    node = node.left
                #right
                else:
                    node = node.right
            classifications.append(node.target)     
        return classifications
    
    def calculatedGini(self, y: List[int]):
        p = 0
        for i in range(0,3):
            p += ( y.count(i) / len(y) )**2 
        return 1 - ( p )
    
    
class BinaryTree:
    root = None
    height = 0

      
    def addRoot(self, root):
        self.root = root
        
    class Node:
        left = None
        right = None
        attribute = -1
        target = -1
        value = None #leaf node values are None
        depth = 0
        
        def __init__(self, val, att):
            self.value = val
            self.attribute = att
        
        def setSplit(self, s: int):
            self.value = s
        
        def setDepth(self, d: int):
            self.depth = d
        
        def setLeft(self, l):
            self.left = l
        
        def setRight(self, r):
            self.right = r
        
        def setAtt(self, a):
            self.attribute = a