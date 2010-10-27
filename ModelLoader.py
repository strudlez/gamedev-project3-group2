import os

class ModelLoader(object):
    def __init__(self, metadataCache):
        self._metadataCache = metadataCache

    def instanceModelTo(self, modelName, parentNode):
        '''loads a model, parents it to parentNode, and applies any metadata to
        it'''
        model = self._getModel(modelName)
        metadata = self._metadataCache.load(self._modelNameToMetadataName(modelName))
        if metadata != None:
            print 'applied to model'
            self.applyMetadataToNode(metadata, model)
        model.reparentTo(parentNode)
        return model

    def applyMetadataToNode(self, metadata, node):
        '''given a metadata object, sets it's data onto given pandanode'''
        x, y, z = metadata.getPos()
        h, p, r = metadata.getHpr()
        scale = metadata.getScale()
        node.setPosHpr(x, y, z, h, p, r)
        node.setScale(scale)

    def _modelNameToMetadataName(self, name):
        '''converts name of model to name of it's corresponding metadata file'''
        n, _ = os.path.splitext(name)
        return n + '.meta'

    def _getModel(self, name):
        return loader.loadModel(name)