test = True

def AddProduct():
    file1 = open("Product.txt", 'a')
    productList = readProduct()
    for eachRow in productList:
        pID = input("Enter Product ID: ")
        if pID not in eachRow[0]:
            pName = input("Enter Product Name: ")
            pDescription = input("Enter Product Description: ")
            pQuantity = input("Enter Product Quantity: ")
            pPrice = input("Enter Price: ")
            #Append to a file
            product =(pID + "\t" +pName+"\t"+pDescription+"\t"
                      +pQuantity+"\t"+pPrice)
            file1.write(product +"\n")
            file1.close()
            print("Product ID "+pID+"has been added!")
            break
        else:
            print(f"This product you're trying to input {pID} already exists")

def ViewProduct():
    productList = readProduct()
    for eachRow in productList:
        print("Product ID : "+eachRow[0]+"\t\t Name: "
        +eachRow[1]+ "\t\t Description : "+eachRow[2]
        +"\t\t Quantity : "+eachRow[3]+ "\t\t Price : "
        +eachRow[4])

def readProduct():
    lines = []
    with open('Product.txt', 'r') as file:
        for eachLine in file:
            eachLine = eachLine.replace("\n", "")
            eachLine = eachLine.split("\t")
            lines.append(eachLine)
    return lines


def DeleteProduct():
    prodID = input("Enter Product ID to Delete: ")
    productList = readProduct()
    for eachrow in productList:
        if eachrow[0]==prodID:
            productList.remove(eachrow)
            SaveProduct(productList)
            print("Product ID " + prodID + " has been deleted.")
        else:
            print("This Product ID does not exist!")
            break

def SaveProduct(prodList):
    file = open('Product.txt', 'w')
    for eachrow in prodList:
        line = (eachrow[0] +"\t"+eachrow[1]+"\t"+eachrow[2]
                +"\t"+eachrow[3]+"\t"+eachrow[4]+"\n")
        file.write(line)
    file.close()

# Update function Assignment
# [N]ame [D]escription
# [Q]uantity [P]rice

# Ex:
# Enter Product ID: 001
# Enter the detail to update: N
# Enter new value: Pencil

# Will call for readProduct function and productList variable

def UpdateProduct():
    prodID = input("Enter Product ID: ")
    productList = readProduct()
    for eachrow in productList:
        if eachrow[0] == prodID:
            print(eachrow)
            print("[N]ame \t [D]escription")
            print("[Q]Quantity \t [P]rice")
            prodDetails = input("Enter the detail to Update: ")
            prodNewValue = input("Enter new Value: ")
            if prodDetails == "N":
                eachrow.pop(1)
                eachrow.insert(1, prodNewValue)
            elif prodDetails == "D":
                eachrow.pop(2)
                eachrow.insert(2, prodNewValue)
            elif prodDetails == "Q":
                eachrow.pop(3)
                eachrow.insert(3, prodNewValue)
            elif prodDetails == "P":
                eachrow.pop(4)
                eachrow.insert(4, prodNewValue)
            else:
                print("Invalid Input")
    SaveProduct(productList)
    print("Product ID "+prodID+" detail has been Updated.")
    ViewProduct()

def prodMngt():
    print("[A]dd Product \t [U]pdate Product")
    print("[D]elete Product \t [V]iew Product")
    print("[E]xit Program")
    prodOp = input("Enter Operation: ")
    if prodOp == "A":
        AddProduct()
    elif prodOp == "D":
        DeleteProduct()
    elif prodOp == "U":
        UpdateProduct()
    elif prodOp == "V":
        ViewProduct()
    elif prodOp == "E":
        print("Exiting Program!")
        exit()
    else:
        print("Invalid Input")

def userMngt():
    pass


while(test):
    print("******************************************")
    print("[U]user Management \t [P]roduct Management")
    operation = input("Input an operation: ")
    print("******************************************")
    if operation == "U":
        userMngt()
    elif operation =="P":
        prodMngt()
    else:
        print("Invalid Operation")
