# pytest-regtest2

*pytest-regtest2* is a fork of [pytest-regtest][pytest-regtest], a plugin for [pytest][pytest]. I forked this project to make it compatible with the latest versions of Python and pytest.

The main changes in this fork are:

- Support for **Python 3.12** (minimum 3.8)
- Update to **pytest 7.4.0** and higher
- Removal of **Python 2** support


*pytest-regtest2* is a *pytest*-plugin for implementing regression tests.
Compared to functional testing a regression test does not test if
software produces correct results, instead a regression test checks if
software behaves the same way as it did before introduced changes.

More about regression testing at
<https://en.wikipedia.org/wiki/Regression_testing>. Regression testing
is a common technique to get started when refactoring legacy code
lacking a test suite.

*pytest-regtest2* allows capturing selected output which then can be
compared to the captured output from former runs.

To install and activate this plugin execute:

    $ pip install pytest-regtest2

*pytest-regtest2* plugin provides a fixture named *regtest* which can be
used as a file handle for recording data:

```python
    def test_squares_up_to_ten(regtest):

        result = [i*i for i in range(10)]

        # one way to record output:
        print(result, file=regtest)

        # alternative method to record output:
        regtest.write("done")

        # or using a context manager:
        with regtest:
            print("this will be recorded")
```

If you run this test script with *pytest* the first time there is no
recorded output for this test function so far and thus the test will
fail with a message including a diff:

    $ py.test
    ...

    regression test output differences for test_demo.py::test_squares_up_to_ten:

    >   --- current
    >   +++ tobe
    >   @@ -1,2 +1 @@
    >   -[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
    >   -done
    >   +

The output tells us what the current output is, and that the "tobe" output
is still empty.

For accepting this output, we run *pytest* with the *--reset-regtest*
flag:

    $ py.test --regtest-reset

Now the next execution of *py.test* will succeed:

    $ py.test

Now we break the test by modifying the code under test to compute the first
eleven square numbers:

```python
    from __future__ import print_function

    def test_squares_up_to_ten(regtest):

        result = [i*i for i in range(11)]  # changed !

        # one way to record output:
        print(result, file=regtest)

        # alternative method to record output:
        regtest.write("done")
```

The next run of pytest delivers a nice diff of the current and expected output
from this test function:

    $ py.test

    ...
    >   --- current
    >   +++ tobe
    >   @@ -1,2 +1,2 @@
    >   -[0, 1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
    >   +[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
    >    done


The recorded output was written to files in the subfolder
`_regtest_outputs` next to your test script(s). You might keep this
folder under version control.


Other features
--------------

Another way to record output is to capture all output to `sys.stdout`:

```python
    def test_squares_up_to_ten(regtest):

        result = [i*i for i in range(10)]

        with regtest:
            print(result)
```

You can reset recorded output of files and functions individually as:

    $ py.test --regtest-reset tests/test_00.py
    $ py.test --regtest-reset tests/test_00.py::test_squares_up_to_ten

To supress the diff and only see the stats use:

    $ py.test --regtest-nodiff

To see recorded output during test execution run:

    $ py.test --regtest-tee -s

If you develop on mixed platforms it might be usefull to ignore white
spaces at the end of the lines when comparing output. This can be
achieved by specifying:

    $ py.test --regtest-ignore-line-endings


Fixing unavoidable changes in recorded  output
----------------------------------------------

The recorded output can contain data which is changing from test run to test
run, e.g. pathes created with the `tmpdir` fixture or hexadecimal object ids,
when objects are printed.

The plugin already replaces such changing data in the recorded output,
and one can register own converters in `conftest.py` in the tests
folder. For example:

```python
    import pytest_regtest2

    @pytest_regtest2.register_converter_pre
    def fix_before(txt):
        """modify recorded output before the default fixes
        like temp folders or hex object ids are applied"""

        # remove lines with passwords:
        lines = txt.split('\n')
        lines = [l for l in lines if "password is" not in l]
        return '\n'.join(lines)

    @pytest_regtest2.register_converter_post
    def after(txt):
        """modify recorded output after the default fixes
        like temp folders or hex object ids are applied"""

        # for demo only
        return txt.upper()
```

This can be used to fix substrings like "computation need 1.23 seconds"
to "computation needed <TIME> seconds" etc.

One can register multiple such converters which will be applied in
order of registration.


[pytest]: https://pytest.org/
[pytest-regtest]: https://gitlab.com/uweschmitt/pytest-regtest