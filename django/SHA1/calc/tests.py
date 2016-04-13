import datetime

from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse

from .models import File

class FileMethodTests(TestCase):

    def test_was_uploaded_recently_with_future_file(self):
        """
        was_uploaded_recently() should return False for questions whose
        upl_date is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_file = File(upl_date=time)
        self.assertEqual(future_file.was_uploaded_recently(), False)
        
    def test_was_uploaded_recently_with_old_file(self):
        """
        was_uploaded_recently() should return False for files whose
        upl_date is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=30)
        old_file = File(upl_date=time)
        self.assertEqual(old_file.was_uploaded_recently(), False)

    def test_was_uploaded_recently_with_recent_file(self):
        """
        was_uploaded_recently() should return True for files whose
        upl_date is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=1)
        recent_file = Question(upl_date=time)
        self.assertEqual(recent_file.was_uploaded_recently(), True)

def create_file(title, days):
    """
    Creates a file with the given `title` uploaded the given
    number of `days` offset to now (negative for files uploaded
    in the past, positive for files that have yet to be uploaded).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return File.objects.create(title=title,
                                   upl_date=time)

class FileViewTests(TestCase):
    def test_index_view_with_no_files(self):
        """
        If no files exist, an appropriate message should be displayed.
        """
        response = self.client.get(reverse('calc:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No files are available.")
        self.assertQuerysetEqual(response.context['latest_file_list'], [])

    def test_index_view_with_a_past_file(self):
        """
        File with a upl_date in the past should be displayed on the
        index page.
        """
        create_file(title="Past file.", days=-30)
        response = self.client.get(reverse('calc:index'))
        self.assertQuerysetEqual(
            response.context['latest_file_list'],
            ['<File: Past file.>']
        )

    def test_index_view_with_a_future_file(self):
        """
        File with a upl_date in the future should not be displayed on
        the index page.
        """
        create_file(title="Future file.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No files are available.",
                            status_code=200)
        self.assertQuerysetEqual(response.context['latest_file_list'], [])

    def test_index_view_with_future_file_and_past_file(self):
        """
        Even if both past and future questions exist, only past files
        should be displayed.
        """
        create_file(title="Past file.", days=-30)
        create_file(title="Future file.", days=30)
        response = self.client.get(reverse('calc:index'))
        self.assertQuerysetEqual(
            response.context['latest_file_list'],
            ['<File: Past file.>']
        )

    def test_index_view_with_two_past_files(self):
        """
        The files index page may display multiple files.
        """
        create_file(title="Past file 1.", days=-30)
        create_file(title="Past file 2.", days=-5)
        response = self.client.get(reverse('calc:index'))
        self.assertQuerysetEqual(
            response.context['latest_file_list'],
            ['<File: Past file 2.>', '<File: Past file 1.>']
        )

class FileIndexDetailTests(TestCase):
    def test_detail_view_with_a_future_file(self):
        """
        The detail view of a file with a upl_date in the future should
        return a 404 not found.
        """
        future_file = create_file(title='Future file.',
                                          days=5)
        response = self.client.get(reverse('calc:detail',
                                   args=(future_file.id,)))
        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_a_past_file(self):
        """
        The detail view of a file with a upl_date in the past should
        display the file's title.
        """
        past_file = create_file(title='Past file.',
                                        days=-5)
        response = self.client.get(reverse('calc:detail',
                                   args=(past_file.id,)))
        self.assertContains(response, past_file.title,
                            status_code=200)
