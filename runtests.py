import sys

try:
    from django.conf import settings

    settings.configure(
        DEBUG=True,
        USE_TZ=True,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
            }
        },
        ROOT_URLCONF="permatrix.urls",
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sites",
            "permatrix",
        ],
        SITE_ID=1,
        NOSE_ARGS=['-s'],
        MIDDLEWARE_CLASSES=(),
    )

    try:
        import django
        setup = django.setup
    except AttributeError:
        pass
    else:
        setup()

    from django_nose import NoseTestSuiteRunner
except ImportError:
    import traceback
    traceback.print_exc()
    raise ImportError("To fix this error, run: pip install -r requirements-test.txt")


def run_tests(*test_args):
    if not test_args:
        test_args = ['tests']

    # We don't want to run any tests against Django 1.4 on python 3.3
    # As this combination is not supported by django, so will fail
    import django
    if sys.version_info.major < 3 and django.VERSION[:2] == (1, 4):
        python_version = ".".join([str(i) for i in (sys.version_info.major, sys.version_info.minor, sys.version_info.micro)])
        django_version = ".".join([str(i) for i in django.VERSION[:3]])
        print("This combination of python (%s) and django (%s) is not supported" % (python_version, django_version))
        sys.exit(0)

    # Run tests
    test_runner = NoseTestSuiteRunner(verbosity=1)

    failures = test_runner.run_tests(test_args)

    if failures:
        sys.exit(failures)


if __name__ == '__main__':
    run_tests(*sys.argv[1:])
