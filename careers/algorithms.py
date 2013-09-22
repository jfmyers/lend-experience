# Summary: Organize experience posts into different career areas based on tags associated with each post.
from careers.models import Area, SubArea
from text_algorithms.word_similarity import Similarity

class CalculateCareer:
    def __init__(self, post):
        self.post = post
        self.tags = post.tags.all()
        # Threshold for similarity algorithm. Two words must be at least 65% similar.
        self.threshold = .65
        
        # Initiate Career calculations...
        self.get_career_areas()
        self.get_career_sub_areas()
        self.calculate()
        
    def get_career_areas(self):
        # Get all the career areas. There are 10 (Art, Business, Education, Energy, etc...)
        self.areas = Area.objects.all()

    def get_career_sub_areas(self):
        # Each carear area has subareas, (ex: Business: finance, economics, marketing, etc...), get each of these.
        self.sub_areas = {}
        for area in self.areas:
            self.sub_areas[area.url] = area.subarea.all()
        
    def calculate(self):
        # We want to compare each sub_area for text similarity with each tag a post has.
        # If the similarity is greater than .65 than the post is related to a specific career area.
        # There are typically less tags with a post than all sub_areas. So will we begin the loop with sub_areas.
        for key, value in self.sub_areas.iteritems():
            # Compare each sub_area to each tag.
             for sub_area in value:
                 for tag in self.tags:
                     sim = Similarity(tag.name,sub_area.name).get()
                     if sim > self.threshold:
                        if key == "ArtDesignFashion":
                            self.post.ArtDesignFashion = 1
                        elif key == "Business":
                            self.post.Business = 1
                        elif key == "Education":
                            self.post.Education = 1
                        elif key == "Energy":
                            self.post.Energy = 1
                        elif key == "Engineering":
                            self.post.Engineering = 1
                        elif key == "Entertainment":
                            self.post.Entertainment = 1
                        elif key == "GovernmentAndLaw":
                            self.post.GovernmentAndLaw = 1
                        elif key == "HealthAndMedicine":
                            self.post.HealthAndMedicine = 1
                        elif key == "NonProfits":
                            self.post.NonProfits = 1
                        elif key == "Technology":
                            self.post.Technology = 1
    
                        self.post.save()