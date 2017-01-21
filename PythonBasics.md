# Python Basics

## The basics

## Loops
### `while` loops
A `while` loop repeats its content as long as a condition is true / valid. The general structure is:

```Python
while (<condition>):
    <list of actions>
```

For example, consider the following program:
```Python
a = 10
while (a > 7):
    b = 2 * a
    print(a, b)
print("done")
```

The execution of this program is:
* `a` is assigned to be 10
* Iteration 0: a = 10, so (a > 7) is `True`, so the loop executes and prints "10 20"
* Iteration 1: a = 9, so (a > 7) is `True`, so the loop executes and prints "9 18"
* Iteration 2: a = 8, so (a > 7) is `True`, so the loop executes and prints "8 16"
* Iteration 3: a = 7, so (a > 7) is `False`, so the loop ends
* The program prints "done"

So the following is printed:
```
10 20
9 18
8 16
done
```

### `for` loops
Each time a `for` loop is executed, an element from a set is chosen to be the value of a variable. The loop ends when all elements have been used. The general structure is:

```Python
for <variable> in range(<a list>):
    <list of actions>
```

For example, consider the following program:
```Python
a = ["Math", "Physics", "Chemistry", "Biology"]
for course in a:
    print(course, "101")
print("done")
```

The execution of this program is:
* `a` is assigned to be a list of course names
* Iteration 0: course = "Math", the program prints "Math 101"
* Iteration 1: course = "Physics", the program prints "Physics 101"
* Iteration 2: course = "Chemistry", the program prints "Chemistry 101"
* Iteration 3: course = "Biology", the program prints "Biology 101"
* The program prints "done"

So the following is printed:
```
Math 101
Physics 101
Chemistry 101
Biology 101
done
```

Another common use of `for` loops is associated with the `range()` syntex. For example, the following program

```Python
for i in range(5):
    print(i)
```
prints `0 1 2 3 4`. Each time, i is assigned to the next integer, from 0 (inclusive) to the argument of `range()` (exclusive) - in this case, 5.

### `while` vs `for`
In most cases, both `while` and `for` loops can be used to implement the same function. It's really just a matter of efficiency.

For example, the example for `while` loops can be rewritten using a `for` loop as:

```Python
a = [10, 9, 8]
for i in a:
    print (i, 2 * i)
print("done")
```

Similarly, the first example for `for` loops can be rewritten using a `while` loop as:
```Python
a = ["Math", "Physics", "Chemistry", "Biology"]
b = 3
while (b >= 0):
    print(a[b], "101")
print("done")
```
So the third, second, first, and zeroth (note that in Python we count from 0) are used. The program prints the same thing.

But clearly, the original examples are more efficient.


## Dictionary
A dictionary is like a list, except that each of its element has a _key_ (i.e. a name) instead of an _index_. In other words, it is a set of key-value pairs. Its general structure is:
```Python
<var name> = {<key 1>: <value 1>,
              <key 2>: <value 2>,
              ...
              <key n>: <value n>,
```

For example, the following is a dictionary that describes the students names and their IDs.
```Python
students = {10000001: "Andy Wang",
            10000002: "Bill Anderson",
            10000003: "Candy Ali"}
```

Then, if we just call
```
print(students[10000001])
```
`Andy Wang` will be printed.

We can also construct a dictionary that maps 