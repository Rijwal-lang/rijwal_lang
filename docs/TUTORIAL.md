# 🎓 Rijwal_Lang Tutorial for Beginners

## Lesson 1: Your First Program (5 mins)

### What is Rijwal_Lang?
Rijwal_Lang is a programming language that looks like English! Write code that's easy to read and understand.

### Write Your First Program
Open Rijwal_Lang IDE and type:

```rijwal
When Program Starts:
    Print "Hello, World!"
```

Click **▶️ Run Code** button. You should see:
```
Hello, World!
```

🎉 **Congratulations!** You just wrote your first program!

---

## Lesson 2: Variables (10 mins)

### What is a Variable?
A variable is like a box that holds a value (number, text, etc.)

### Create a Variable
```rijwal
Let name = "Alice"
Let age = 10
Let score = 95.5
```

### Use Variables
```rijwal
Let name = "Alice"
Let age = 10

When Program Starts:
    Print "Name: " + name
    Print "Age: " + age
```

**Output:**
```
Name: Alice
Age: 10
```

### Math with Variables
```rijwal
Let x = 5
Let y = 3

When Program Starts:
    Print x + y      # 8
    Print x - y      # 2
    Print x * y      # 15
    Print x / y      # 1.666...
```

---

## Lesson 3: Getting User Input (10 mins)

### Ask the User
```rijwal
When Program Starts:
    Input name
    Print "Hello, " + name
```

**When you run it:**
```
➤ name: Bob
Hello, Bob
```

### Store Input in Variables
```rijwal
When Program Starts:
    Input age
    Let next_age = age + 1
    Print "Next year you'll be " + next_age
```

**When you run it:**
```
➤ age: 10
Next year you'll be 11
```

---

## Lesson 4: Functions (15 mins)

### What is a Function?
A function is a reusable block of code. You can call it multiple times!

### Create a Simple Function
```rijwal
Function greet(name):
    Return "Hello, " + name

When Program Starts:
    Print greet("Alice")
    Print greet("Bob")
```

**Output:**
```
Hello, Alice
Hello, Bob
```

### Function with Math
```rijwal
Function double(x):
    Return x * 2

When Program Starts:
    Let number = 5
    Let doubled = double(number)
    Print doubled  # 10
```

### Function with Multiple Parameters
```rijwal
Function add(a, b):
    Return a + b

Function multiply(a, b):
    Return a * b

When Program Starts:
    Print add(5, 3)        # 8
    Print multiply(5, 3)   # 15
```

---

## Lesson 5: Strings (15 mins)

### What is a String?
A string is text, like "Hello" or "Alice"

### Create Strings
```rijwal
Let greeting = "Hello"
Let name = "World"
```

### Join Strings (Concatenation)
```rijwal
Let first = "Hello"
Let second = "World"
Let combined = first + ", " + second

When Program Starts:
    Print combined  # Hello, World
```

### String Functions
```rijwal
When Program Starts:
    Let text = "hello"
    Print upper(text)   # HELLO
    Print lower("WORLD")  # world
    Print len("abc")     # 3
```

---

## Lesson 6: Timers (10 mins)

### Repeat Code Every N Seconds
```rijwal
Every 1 second:
    Print "Tick!"
```

This will keep printing "Tick!" every second until you stop it.

### Countdown Timer
```rijwal
Let count = 5

Every 1 second:
    Print count
    Let count = count - 1
```

---

## Lesson 7: Project - Age Calculator

Combine everything you learned!

```rijwal
Function age_in_months(years):
    Return years * 12

Function age_in_days(years):
    Return years * 365

When Program Starts:
    Print "=== Age Calculator ==="
    Input age
    
    Let months = age_in_months(age)
    Let days = age_in_days(age)
    
    Print "Age in months: " + months
    Print "Age in days: " + days
```

**When you run it:**
```
=== Age Calculator ===
➤ age: 10
Age in months: 120
Age in days: 3650
```

---

## Lesson 8: Project - Temperature Converter

```rijwal
Function celsius_to_fahrenheit(celsius):
    Return celsius * 9/5 + 32

Function fahrenheit_to_celsius(fahrenheit):
    Return (fahrenheit - 32) * 5/9

When Program Starts:
    Print "=== Temperature Converter ==="
    Input celsius
    
    Let fahrenheit = celsius_to_fahrenheit(celsius)
    Print celsius + "°C = " + fahrenheit + "°F"
```

---

## Lesson 9: Importing Code from Files

### Create a file called `math_helpers.Rijwal_Lang`:
```rijwal
Function square(x):
    Return x * x

Function cube(x):
    Return x * x * x
```

### Use it in another file:
```rijwal
Import "math_helpers.Rijwal_Lang"

When Program Starts:
    Print square(5)  # 25
    Print cube(5)    # 125
```

---

## Lesson 10: Debugging Tips

### 1. Use Print to Check Values
```rijwal
Let x = 5
Print "x = " + x  # Check what x is
Let y = x * 2
Print "y = " + y  # Check what y is
```

### 2. Check Your Function
```rijwal
Function add(a, b):
    Print "Adding " + a + " and " + b  # Debug
    Return a + b

When Program Starts:
    Print add(5, 3)
```

### 3. Read Error Messages
- **Line X:** Tells you where the error is
- **Syntax Error:** Check spelling and indentation
- **Not found:** Check variable name and indentation

---

## Common Mistakes & Fixes

### Mistake 1: Forgetting Indentation
```rijwal
# ❌ Wrong
When Program Starts:
Print "Hello"

# ✅ Right
When Program Starts:
    Print "Hello"
```

### Mistake 2: Using Variable Before Let
```rijwal
# ❌ Wrong
Print x  # x not defined yet!

# ✅ Right
Let x = 5
Print x
```

### Mistake 3: Wrong Quotes
```rijwal
# ❌ Wrong
Print 'Hello  # Single quote not closed

# ✅ Right
Print "Hello"
```

### Mistake 4: Forgetting Function Parameters
```rijwal
# ❌ Wrong
Function greet:
    Return "Hello"

# ✅ Right
Function greet():
    Return "Hello"
```

---

## Practice Challenges

### Challenge 1: Calculator
Create a program that:
- Asks for two numbers
- Adds them
- Multiplies them
- Prints both results

### Challenge 2: Greeting
Create a function that:
- Takes a name
- Takes an age
- Returns a greeting with both values

### Challenge 3: Timer Countdown
Create a countdown from 10 to 1, printing each number each second.

### Challenge 4: Name Reverser
Create a function that:
- Takes a string
- Returns it reversed

### Challenge 5: Secrets Game
- Generate a random number (between 1-100)
- Ask user to guess
- Tell them if too high/low

---

## Next Steps

✅ You now know the basics of Rijwal_Lang!

### Learn More:
- 📚 Read the full [Language Reference](LANGUAGE_REFERENCE.md)
- 💻 Check the examples folder
- 🎮 Build your own projects!

### Create a Project:
Think of something cool you want to build and code it in Rijwal_Lang!

Happy coding! 🚀

---

## Quick Reference

| Keyword | Purpose |
|---------|---------|
| `Print` | Display text |
| `Let` | Create variable |
| `Input` | Get user input |
| `Function` | Define function |
| `Return` | Return from function |
| `When Program Starts` | Program entry point |
| `Every` | Repeat every N seconds |
| `Import` | Load another file |

---

Good luck! 🌟
