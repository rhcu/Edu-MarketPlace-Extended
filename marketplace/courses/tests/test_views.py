from courses.views import adjust_rating

class BasicTests(TestCase):
    def test_adjust_rating(self):
        self.assertEqual(adjust_rating(10), 1)
