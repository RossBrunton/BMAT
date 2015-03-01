from django.test import TestCase, Client
from django.contrib.auth.models import User

from .models import Bookmark, HTMLTitleReader
import json

class BookmarkModelTestCase(TestCase):
    """ Test that bookmarks work as expected """
    def setUp(self):
        self.user = User.objects.create(username="John", password="smith")
        self.user.save()
        self.bm = Bookmark(owner=self.user, title="Test Bookmark", url="http://localhost/")
        self.bm.save()

    def test_to_dict(self):
        bm_dict = self.bm.to_dir()
        self.assertEquals(bm_dict["title"], "Test Bookmark")
        self.assertEquals(bm_dict["url"], "http://localhost/")
        self.assertEquals(bm_dict["tags"], [])
    
    def test_to_json(self):
        self.assertEquals(self.bm.to_dir(), json.loads(self.bm.to_json()))
    
    def test_by_user(self):
        user2 = User.objects.create(username="Not John", password="smith")
        user2.save()
        
        bm2 = Bookmark(owner=user2, title="Other Bookmark", url="http://example.com")
        bm2.save()
        
        self.assertIn(self.bm, Bookmark.by_user(self.user))
        self.assertNotIn(self.bm, Bookmark.by_user(user2))
        
        self.assertIn(bm2, Bookmark.by_user(user2))
        self.assertNotIn(bm2, Bookmark.by_user(self.user))


class HTMLTitleReaderTestCase(TestCase):
    """ Tests the HTML title reader """
    
    def setUp(self):
        self.reader = HTMLTitleReader()
        
    def test_basic(self):
        self.reader.feed("<html><head><title>Test Title</title></head><body>Hello</body></html>")
        self.assertEqual(self.reader.title, "Test Title")
    
    def test_absent(self):
        self.reader.feed("<html><head></head><body>Hello</body></html>")
        self.assertFalse(self.reader.title)
    
    def test_nested_tags(self):
        self.reader.feed("<html><head><title>My <b>cool</b> website</title></head><body>Hello</body></html>")
        self.assertEquals(self.reader.title, "My cool website")
    
    def test_in_body(self):
        self.reader.feed("<html><head></head><body><title>Some Title</title>Hello</body></html>")
        self.assertFalse(self.reader.title)
    
    def test_multiple_tags(self):
        self.reader.feed("<html><head><title>Title 1</title><title>Title 2</title></head><body>Hello</body></html>")
        self.assertEquals(self.reader.title, "Title 1")
    
    def test_unicode(self):
        title = u"\xe2\xa0\xa0\xe2\xa0\x83\xe2\xa0\x87\xe2\xa0\x8a\xe2\xa0\x9d\xe2\xa0\x99\xe2\xa0\x80\xe2\xa0\xa0\xe2"\
            + u"\xa0\xba\xe2\xa0\x91\xe2\xa0\x83\xe2\xa0\x8e\xe2\xa0\x8a\xe2\xa0\x9e\xe2\xa0\x91"
        
        self.reader.feed(u"<html><head><title>{}</title></head><body>Hello</body></html>".format(title))
        self.assertEquals(self.reader.title, title)
    
    def test_unclosed(self):
        self.reader.feed("<html><head><title>Title</head><body>Hello</body></html>")
        self.assertFalse(self.reader.title)
