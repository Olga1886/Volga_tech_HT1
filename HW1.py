# Упражнение 0
names = ['Петров', 'Сидоров']
tabs = [123, 124]
for i in range(len(names)):
  print(f"{names[i]} {tabs[i]}")


# Упражнение 1
digits = [5, 2, 3]
squared_digits = [x**2 for x in digits]
squared_digits.sort()
print(squared_digits)


# Упражнение 2
tpl = (1, 2, 3, 4)
print(tpl[-1])


# Упражнение 3
tupl = (1, 2, 3)
new_tupl = tupl[:-1] + (4,)
print(new_tupl)


# Упражнение 4
str = 'hello kitty'
words = 'hello kitty'.split()
print(words[-2:])


# Упражнение 5
s1 = 'abcdabcd' # дано
s2 = 'cdcdef' # дано

common_leters = set(s1) & set(s2)
print(len(common_leters))


# Task 1. 796. Rotate String
def rotateString(s, goal):
  if len(s) != len(goal):
    return False

  s_doubled = s + s
  return goal in s_doubled


s = "abcde"
goal = "cdeab"
print(rotateString(s, goal))  # Output: True

s = "abcde"
goal = "abced"
print(rotateString(s, goal))  # Output: False

#Task 2. 1455. Check If a Word Occurs As a Prefix of Any Word in a Sentence
def isPrefixOfWord(sentence, searchWord):
  words = sentence.split()
  for i, word in enumerate(words):
    if word.startswith(searchWord):
      return i + 1
  return -1

sentence = "i love eating burger"
searchWord = "burg"
print(isPrefixOfWord(sentence, searchWord))  # Output: 4

sentence = "this problem is an easy problem"
searchWord = "pro"
print(isPrefixOfWord(sentence, searchWord))  # Output: 2

sentence = "i am tired"
searchWord = "you"
print(isPrefixOfWord(sentence, searchWord))  # Output: -1

