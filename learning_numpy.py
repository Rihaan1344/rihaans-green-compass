import numpy as np

"""

SECTION 1 -> referancing nd array elements

 array = np.array([
    [['A', 'B', 'C'],
     ['D', 'E', 'F'],
     ['G', 'H', 'I']],

    [['J', 'K', 'L'],
     ['M', 'N', 'O'],
     ['P', 'Q', 'R']],

    [['S', 'T', 'U'],
     ['V', 'W', 'X'],
     ['Y', 'Z', '_']]
])

word = array[1, 2, 2] + \
        str(array[0, 2, 2]).lower() + \
        str(array[0, 2, 1]).lower() + \
        str(array[0, 0, 0]).lower() + \
        str(array[0, 0, 0]).lower() + \
        str(array[1, 1, 1]).lower() 
        
print(word)
        """

""" 

SECTION 2 -> multidimensional & slicing

array = np.array([
                [1, 2, 3, 4], 
                [5, 6, 7, 8],
                [9, 10, 11, 12], 
                [13, 14, 15, 16]
                ])

array_dif = np.array([i for i in range(1, 17)]).reshape(4, 4)

print(array[2:, 2:]) """

""" vector and scalar operations

 array = np.array([1, 2, 3])

#scalar

print(array + 1)
print(array - 2)
print(array * 3)
print(array / 4)
print(array ** 5)

#vector

print(np.sqrt(array))

#can also use round, floor, ceil

#ex: convert arr of radii to areas of circles

radii = np.array([1, 2, 3])     

print(np.pi * radii ** 2) """

""" arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])

print(arr1 + arr2) """

#comparision operators

""" mapping and comparision arrays

 scores = np.array([91, 55, 100, 73, 82, 64])

print(scores == 100)
print("--------------------")
print(scores <= 60)
print("--------------------")

graded_scores = np.array([score for score in scores])
graded_scores[graded_scores < 60] = "0"
graded_scores[graded_scores >= 60] = "1"

graded_scores = np.where(scores >= 60, "pass", "fail")

print(graded_scores, scores) """
"""  broadcasting
columns = np.array([[i for i in range(1, 10)]])
rows = np.array([[i,] for i in range(1, 10)])

print(columns * rows)
 """
"""
aggr funcs

arr = np.array([[i for i in range(1, 6)] ,
                [i for i in range(6, 11)]
                ])

print(np.std(arr))
print(np.mean(arr))
print(np.min(arr))
print(np.max(arr))
print(np.argmin(arr))
print(arr[np.argmin(arr)])

print(np.argmin(np.argmin(arr)))
print(arr[np.argmin(arr), np.argmin(np.argmin(arr))])

print(np.max(arr))
print(np.argmax(arr))

print(np.sum(arr, axis=1))


"""
""" 

filtering

ages = np.array([[18, 17, 19, 23, 30, 47, 16, 65],
        [35, 52, 24, 17, 18, 48, 32, 70]])

teenagers = ages[ages < 18]
adults = ages[(ages >= 18) & (ages <= 65)]
everybody_else = ages[(ages < 18) | (ages > 65)]

print(f"{ages=}, {teenagers=}, {adults=}, {everybody_else=}")

adults = np.where(ages >= 18, ages, "adult")
#adults = adults.reshape(ages.size)
print(adults) """


""" 

random numbers

rng = np.random.default_rng(seed=1) #seed -> optional, but allows us to recreate results reliably
print(rng.integers(low = 1, high = 101, size = (3, 2))) #ints btw

np.random.seed(seed = 1) #set seed
print(np.random.uniform(low = -1, high = 1, size = (3, 2))) #gives decimals """

""" 

list shuffling

rng = np.random.default_rng()

arr = np.array(range(1, 6))
rng.shuffle(arr)

print(arr) """

rng = np.random.default_rng()

fruits = np.array(["🍎", "🍌", "🍇", "🍍", "🍊"])
fruit = rng.choice(fruits)
fruits = rng.choice(fruits, size=(2, 3))
print(fruit)
print(fruits)