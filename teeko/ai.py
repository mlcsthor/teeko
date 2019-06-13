class MinMax:
    def __init__(self, tree):
        self.tree = tree

    def max_value(self, node):
        print("MinMax-->MAX: Visited Node :: " + node.name)

        if node.is_leaf:
            return node.value

        infinity = float('inf')
        max_value = -infinity

        for child in node.children:
            max_value = max(max_value, self.min_value(child))

        return max_value

    def min_value(self, node):
        print('MinMax-->MIN: Visited Node :: ' + node.name)

        if node.is_leaf:
            return node.value

        infinity = float('inf')
        min_value = infinity

        for child in node.children:
            min_value = min(min_value, self.max_value(child))

        return min_value