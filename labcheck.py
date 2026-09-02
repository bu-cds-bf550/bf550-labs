"""Self-checks for the lab notebooks.

Every check reports; nothing here ever raises, and nothing here grades.
Three states:

  #   not attempted yet — the name the task asks for does not exist
  X   not passing yet — what came back, what was expected, and a hint
  OK  passing

Run a check cell as often as you like. It only reads your work.
"""
import inspect


def _report(mark, text):
    print(f"{mark} {text}")


def check(name, expect, args=None, hint=""):
    """Report whether `name` — a variable, or a function called with `args` —
    equals `expect`. Looks the name up in the notebook the check runs in."""
    namespace = inspect.currentframe().f_back.f_globals
    if name not in namespace:
        _report("⬜", f"{name} — not defined yet. Write it in the cell above, "
                      "run that cell, then re-run this one.")
        return
    value = namespace[name]
    label = name
    if args is not None:
        # a repr carrying a memory address (e.g. a generator) reads as noise —
        # show the type's name instead
        shown = ", ".join(type(a).__name__ if " at 0x" in repr(a) else repr(a)
                          for a in args)
        label = f"{name}({shown})"
        try:
            value = value(*args)
        except Exception as error:  # a check never raises — it reports
            _report("⚠️", f"{label} raised {type(error).__name__}: {error}")
            print("   Read the error top to bottom, fix the cell above, and re-run.")
            return
    try:
        comparison = (value == expect)
        if hasattr(comparison, "__len__"):   # arrays compare element by element
            passed = bool(comparison.all()) and len(value) == len(expect)
        else:
            passed = bool(comparison)
    except Exception:               # shapes that cannot even be compared
        passed = False
    if passed:
        _report("✅", f"{label} — passing")
    else:
        _report("❌", f"{label} came back with {value!r}; expected {expect!r}.")
        if hint:
            print(f"   Hint: {hint}")
