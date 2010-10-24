class ResourceCache:
    '''class to load resources and keep references to all of them.'''

    def __init__(self):
        # create empty image cache
        self._resourceDict = {}

    def createResource(self, resourcePath):
        '''Abstract.  Returns the newly created resource, ready to be put in the
        cache.'''
        return None

    def _fetchResource(self, resourcePath):
        '''private method'''
        if resourcePath in self._resourceDict:
            return self._resourceDict[resourcePath]
        resource = self.createResource(resourcePath)
        self._resourceDict[resourcePath] = resource
        return resource