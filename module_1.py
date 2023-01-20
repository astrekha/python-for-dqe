import random    # import random module


my_random_list = random.sample(range(0, 1001), 100)    # create list of 100 elements from 1 to 1000

print('List of 100 random numbers from 0 to 1000 is:')    # print created list
print(my_random_list)

for i in range(len(my_random_list)):    # for each element in list
    for j in range(i + 1, len(my_random_list)):    # for each next element in list
        if my_random_list[i] > my_random_list[j]:    # if current element > next element
            # change order of current and next element vise versa
            my_random_list[i], my_random_list[j] = my_random_list[j], my_random_list[i]

print('Sorted from min to max list of 100 random numbers from 0 to 1000 is:')    # print sorted list
print(my_random_list)

even_list = []    # declare empty list for even numbers
odd_list = []    # declare empty list for odd numbers
for n in my_random_list:    # for each element in list
    if n % 2 == 0:    # if remainder of the division to 2 is equal 0 - number is even
        even_list.append(n)    # add element to even_list
    else:    # if remainder of the division to 2 is not equal  0 - number is odd
        odd_list.append(n)     # add element to odd_list

# count sum of even elements and divide it to number of elements (for even)
avg_even_list = sum(even_list)/len(even_list)
# count sum of even elements and divide it to number of elements (for odd)
avg_odd_list = sum(odd_list)/len(odd_list)

print('Average for even numbers is:', avg_even_list)    # print average for even numbers
print('Average for odd numbers is:', avg_odd_list)    # print average for odd numbers
