# pylint: disable=W0212
from django.test.simple import DjangoTestSuiteRunner


class TestRunner(DjangoTestSuiteRunner):
    def build_suite(self, *args, **kwargs):
        suite = super(TestRunner, self).build_suite(*args, **kwargs)

        blacklist = (
            'django.contrib.auth.tests.models.test_site_profile_not_available',
            'registration.tests.test_get_version',
        )

        suite._tests = [test for test in suite._tests
            if '{0}.{1}'.format(test.__module__, test._testMethodName)
                not in blacklist]

        return suite
