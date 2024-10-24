test = True

def AddProduct():
    pID = input("Enter Product ID: ")
    pName = input("Enter Product Name: ")
    pDescription = input("Enter Product Description: ")
    pQuantity = input("Enter Product Quantity: ")
    pPrice = input("Enter Price: ")
    #Append to a file
    product =(pID + "\t" +pName+"\t"+pDescription+"\t"
              +pQuantity+"\t"+pPrice)
    file1 = open("Product.txt", 'a')
    file1.write(product +"\n")
    file1.close()
    print("Product ID"+pID+"has been added!")

def ViewProduct():
    productList = readProduct()
    for eachRow in productList:
        print("Product ID : "+eachRow[0]+"\t\t Name: "
        + eachRow[1] + "\t\t Description : " + eachRow[2]
        + "\t\t Quantity : " + eachRow[3]+ "\t\t Price : "
        + eachRow[4])

def readProduct():
    lines = []
    with open('Product.txt', 'r') as file:
        for eachLine in file:
            eachLine = eachLine.replace("\n", "")
            eachLine = eachLine.split("\t")
            lines.append(eachLine)
    return lines

def DeleteProduct():
    
def prodMngt():
    print("[A]dd Product \t [U]pdate Product")
    print("[D]elete Product \t [V]iew Product")
    prodOp = input("Enter Operation: ")
    if prodOp == "A":
        AddProduct()
    elif prodOp == "D":
        DeleteProduct()
    elif prodOp == "U":
        UpdateProduct()
    elif prodOp == "V":
        ViewProduct()
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
