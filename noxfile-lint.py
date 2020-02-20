from vox import FlagsBuilder, Manager, get_options, linty, mutations
from vox.linters import python

options = get_options()
if options.posargs:
    files = options.posargs
else:
    files = "src"

manager = Manager(files=files)
manager.lint(python.RadonCC)
manager.lint(python.RadonMI)
# manager.lint(python.Pyroma, FlagsBuilder().build(files='.'))
manager.lint(python.DetectSecrets)
manager.lint(python.Pydiatra)
manager.lint(python.Pylama)
manager.lint(python.Prospector)
manager.lint(python.Bandit)
# manager.lint(python.Frosted)
manager.lint(python.Vulture)
manager.lint(python.Pydocstyle)
manager.lint(python.Pylint)
manager.lint(python.Mypy)
manager.lint(python.PyCodeStyle)
manager.lint(python.Pyflakes)
# manager.lint(python.Jedi)  # slow + buggy
manager.lint(python.Flake8)


@manager.display(
    [
        mutations.sort_location,
        mutations.clean_extensions,
        mutations.merge_duplicates,
        mutations.remove_mam,
        mutations.remove_nosa,
    ]
)
def display(messages):
    linty.display.default(messages)
