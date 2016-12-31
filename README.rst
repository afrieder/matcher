########
Matcher
########

This is a port of `Rematch <https://github.com/jiaweihli/rematch>`_, a Typescript pattern matching library.
Matcher allows for type-safe, functional pattern matching in Python.

===========
Basic usage
===========

---------------------
Without type-checking
---------------------

::

  from matcher import Matcher

  m = Matcher()

  def powerLevel(hero):
    return m.match(hero, [
      m.Type(Speedster, lambda hero: print('Speedsters are too fast!'), lambda hero: math.inf),
      m.Values(['Goku', 'Vegeta'], lambda hero: 9001),
      m.Value('Iron Man', lambda hero: 616)
    ])

  print(powerLevel('Goku'))  # 9001
  print(powerLevel(Speedster.Flash))  # Speedsters are too fast!  # inf
  print(powerLevel('Captain America'))  # matcher.MatchError: Captain America doesn't match any of the provided clauses

------------------
With type-checking
------------------

::

  from matcher import Matcher

  m = Matcher[int, str]()

  def wrongInput(s: str) -> str:
    return m.match(s, [
      m.Value(1, lambda s: s),
      m.Else(lambda s: s)
    ])

  # Argument 1 to "match" of "Matcher" has incompatible type "str"; expected "int"

  def wrongOutput(n: int) -> Any:
    return m.match(n, [
      m.Values((1, 2, 3), lambda n: n + "Hello World"),
      m.Else(lambda n: n**2)
    ])

  # Argument 2 to "Values" of "Matcher" has incompatible type Callable[[int], int]; expected Callable[[int], str]

The Matcher.match function takes in an argument and a group of cases to test the argument against.

There are 4 types of cases:

  - **Value** - argument matches single value
  - **Values** - argument matches one of multiple values
  - **Type** - argument matches a type
  - **Else** - argument does not match any previous cases

If no cases are valid, a MatchError is thrown. There are no 'fall-throughs' like in switch statements.

======================================
Why use pattern matching over if/else?
======================================
For the large majority of code that isn't performance-sensitive, there are a lot of great reasons why you'd want to use pattern matching over if/else:

 - it enforces a common return value and type for each of your branches (when using type definitions)
 - in languages with exhaustiveness checks, it forces you to explicitly consider all cases and noop the ones you don't need
 - it prevents early returns, which become harder to reason about if they cascade, grow in number, or the branches grow longer than the height of your screen (at which point they become invisible). Having an extra level of indentation goes a long way towards warning you you're inside a scope.
 - it can help you identify logic to pull out, rewriting it into a more DRY, debuggable, and testable form.

================
A longer example
================

Let's do an example! We're building a webapp, and we need to authenticate our users and update them on their status. Here's a straightforward solution:

::

  if isinstance(user, BlacklistedUser):
    warnBlacklistMonitor()

    return
  elif user.password == enteredPassword:
    login()

    print("You're logged in!")
  else:
    onUserFailedLogin()

    print("Mistyped your password?  Try again or do a password reset.")

This code works. Let's see how a pattern matching solution stacks up:

::

  from matcher import Matcher

  m = Matcher[User, None]()
  m2 = Matcher[str, str]()

  m.match(user, [
    m.Type(BlacklistedUser, lambda user: warnBlacklistMonitor()),
    m.Else(lambda user: print(
      m2.match(enteredPassword, [
        m2.Value(user.password, lambda password: login(), lambda password: "You're logged in!"),
        m2.Else(lambda password: onUserFailedLogin(), lambda password: f"Your password isn't {password}!")
      ])
    ))
  ])

It's immediately clear that there are 3 return points, and that 2 of them are dependent on the other one. We've factored out the print statement, which'll make debugging / testing easier down the line. And lastly, all the return points consistently return nothing.

==================
A more fun example
==================

We can also calculate Fibonacci numbers using matching!

::

  from matcher import Matcher

  m = Matcher[int, int]()

  cases = [
      m.Values([1, 2], lambda n: 1),
      m.Else(lambda n: m.match(n-1, cases) + m.match(n-2, cases))
  ]

  print(m.match(10, cases))  # 55

This is more in line with the functional definition that fib(1) == fib(2) == 1, and fib(n) == fib(n-1) + fib(n-2).
Due to the lazy evaluation of the actions provided to the cases, we can use recursion.
