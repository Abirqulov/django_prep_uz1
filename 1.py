# friends = input("how many friends do you have? = ")
# a = []
# for i in range(int(friends)):
#     name = input('Wat is your friend name? = ')
#     movie_name = input("The name of your friend’s favorite movie? = ")
#     m = (str(name) + ":" + str(movie_name))
#     a.append(m)
# print(a)


x = [z for z in range(5)]
x[::-1][1] = 5
print(x)