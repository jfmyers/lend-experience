# Summary: Search & Manage Redis Sets
import redis
from tags.models import Tags

class SearchTags:
    def __init__(self, searchStr):
        self.searchStr = searchStr.lower()
        # Rather than search all tags, Redis sets are created for letters A-Z. 
        # Tags are placed into sets based on their first letter.
        # So we need the first letter of the search query to search the right Redis Set.
        self.fLetter = self.searchStr[0]
        self.r = redis.StrictRedis(host = 'REDIS HOST', port = 6376, db = 0)
        # The name of the Redis Set:
        self.set = "lxp_tags_"+self.fLetter
        # Does this Redis Set exist? If not create it from disk.
        if self.r.scard(self.set) == 0:
            self.compile()
    
    def compile(self):
        # Get all of the tags from Disk.
        groups = Tags.objects.all()
        for group in groups:
            name_lower = group.name.lower()
            # Find the tags that begin with the same letter as the input search query and create a Redis Set.
            if name_lower[0] == self.fLetter and name_lower is not None:
                self.r.sadd(self.set, name_lower)
        
    def search(self):
        results = {}
        redisSet = self.r.smembers(self.set)
        for name in redisSet:
            if self.searchStr in name:
                results[name] = name
        
        return results

# Use ManageTags to add new Tags to Redis Set/See if a tag exists already in a Redis Set.
class ManageTags:
    def __init__(self, tag):
        self.tag = tag.lower()
        self.fLetter = self.tag[0]
        self.r = redis.StrictRedis(host = 'REDIS HOST', port = 6376, db = 0)
        self.set = "lxp_tags_"+self.fLetter
        
    def add(self):
        # Add a new tag to Redis Set.
        self.r.sadd(self.set, self.tag)
    
    def exists(self):
        # Does this tag already exist in Redis Set?
        self.r.sismember(self.set, self.tag)
    
        
        
        
        
        