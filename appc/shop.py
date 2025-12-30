arr, counter = ['Headpdhones', 'Laptop', 'Smartphone', 'Tablet', 'Smartwatch'], 0
while True:
    print("Напиши Next или Previous или Stop чтобы закончить:")
    a = input()
    if a == "Next":
        counter += 1
        if counter == len(arr):
            counter = 0
        print(arr[counter])
    elif a == "Previous":
        counter -= 1
        if counter < 0:
            counter = len(arr) - 1
        print(arr[counter])
    else:
        break 
#Емое как это сделать в телеграм боте?
'''
arr, counter = ['Headpdhones', 'Laptop', 'Smartphone', 'Tablet', 'Smartwatch'], 0
router.messsage()
'''