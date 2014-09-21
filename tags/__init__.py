_taggable = {}

def add_taggable(name, model):
    _taggable[name] = model

def lookup_taggable(name):
    return _taggable.get(name, None)


def taggable(name):
    def decorator(c):
        if not hasattr(c, "tags"):
            raise RuntimeError("Class {} does not have a tags property, but is taggable".format(c))
        
        def tag(self, tag):
            if isinstance(tag, (int, long)):
                try:
                    tag = Tag.objects.get(pk=tag, owner=self.owner)
                except ObjectDoesNotExist:
                    #Handle this better?
                    return
            
            if isinstance(tag, (str, unicode)):
                try:
                    tag = Tag.objects.get(slug=defaultfilters.slugify(tag), owner=self.owner)
                except ObjectDoesNotExist:
                    tag = Tag(owner=self.owner, name=tag)
                    tag.save()
            
            tag.owner = self.owner
            tag.save()
            self.tags.add(tag)
        c.tag = tag
        
        def untag(self, tag):
            if isinstance(tag, (int, long)):
                try:
                    tag = Tag.objects.get(pk=tag, owner=self.owner)
                except ObjectDoesNotExist:
                    return
            
            if type(tag) == str:
                try:
                    tag = Tag.objects.get(name__iexact=tag, owner=self.owner)
                except ObjectDoesNotExist:
                    return
            
            self.tags.remove(tag)
        c.untag = untag
        
        @staticmethod
        def get_by_tag(tag):
            out = []
            
            tags = models.Tag.expand_implied_by([tag])
            
            for t in tags:
                results = c.objects.filter(owner=tag.owner, tags=t)
                
                for b in results:
                    if b not in out:
                        out.append(b)
            
            return out
        c.get_by_tag = get_by_tag
        
        add_taggable(name, c)
        
        return c
    return decorator
