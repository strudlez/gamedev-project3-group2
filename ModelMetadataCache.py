from ModelMetadata import ModelMetadata
from ResourceCache import ResourceCache
import string

class ModelMetadataCache(ResourceCache):
    def createResource(self, resourcePath):
        try:
            file = open(resourcePath, 'r')
        except:
            return None # this metadata doesn't exist

        ret = ModelMetadata()
        x, y, z = ret.getPos()
        h, p, r = ret.getHpr()
        # load data from file
        for line in file:
            before, after = string.split(line, '=')
            before = string.upper(string.strip(before))
            string.after = string.upper(string.strip(after))

            num = float(after)
            print '%s, %s, %s' % (before, after, num)
            if before == 'X':
                x = num
            elif before == 'Y':
                y = num
            elif before == 'Z':
                z = num
            elif before == 'H':
                h = num
            elif before == 'P':
                p = num
            elif before == 'R':
                r = num
            elif before == 'SCALE':
                ret.setScale(num)

        file.close()
        ret.setPos((x, y, z))
        ret.setHpr((h, p, r))
        
        return ret

    def load(self, path):
        return self._fetchResource(path)