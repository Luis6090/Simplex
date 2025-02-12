import numpy as np

arrayVariableBasic: np.array

arrayVariableNoBasic: np.array

arrayObjectiveFunctionVariableNoBasic: np.array
arrayObjectiveFunctionVariableBasic: np.array
arrayRestrictionValues: np.array

# def pplIsPossible(arrayObjectiveFunctionVariableBasic):
#     if np.max(arrayObjectiveFunctionVariableBasic) == 1:
#         return False
#     return True

# def removeColumnsArtificiais(arrayObjectiveFunctionVariableNoBasic):
#     global arrayVariableNoBasic,arrayObjectiveFunctionVariableBasic2
#     removeIndex = np.where(arrayObjectiveFunctionVariableNoBasic == 1)
#     arrayVariableNoBasic = np.delete(arrayVariableNoBasic,removeIndex, axis=1)


def indexNegativeNumber(arrayObjectiveFunctionVariableNoBasic)->int:
    index = np.argmin(arrayObjectiveFunctionVariableNoBasic)
    return index

def verificationExistsNegativeNumber(arrayObjectiveFunctionVariableNoBasic):
    return arrayObjectiveFunctionVariableNoBasic.min() < 0

def calculateNewFOVariableNoBasic():
    global arrayVariableBasic,arrayVariableNoBasic,arrayObjectiveFunctionVariableNoBasic,arrayObjectiveFunctionVariableBasic
    arrayObjectiveFunctionVariableNoBasicCopy = arrayObjectiveFunctionVariableNoBasic - np.dot(arrayObjectiveFunctionVariableBasic, np.dot(np.linalg.inv(arrayVariableBasic), arrayVariableNoBasic))
    return arrayObjectiveFunctionVariableNoBasicCopy

def calculateNewValueRestriction():
    global arrayVariableBasic,arrayRestrictionValues
    bCopy = np.dot(np.linalg.inv(arrayVariableBasic), arrayRestrictionValues)
    return bCopy

def calculateNewCoefficientVariableNoBasic():
    global arrayVariableBasic,arrayVariableNoBasic
    invarrayVariableBasic = np.linalg.inv(arrayVariableBasic)
    rCopy =  np.dot(invarrayVariableBasic, arrayVariableNoBasic)
    return rCopy

def calculateValueFO():
    global arrayObjectiveFunctionVariableBasic,arrayVariableBasic,arrayRestrictionValues
    resultFO = np.dor(arrayObjectiveFunctionVariableBasic, np.dot(np.linalg.inv(arrayVariableBasic), arrayRestrictionValues)) 
    return resultFO

def testRatioTableau(index):
    new_b = calculateNewValueRestriction()
    newarrayVariableNoBasic = calculateNewCoefficientVariableNoBasic()[:,index]
    newarrayVariableNoBasic[newarrayVariableNoBasic == 0] = -1
    reason_test = np.divide(new_b,newarrayVariableNoBasic)
    array_positive_reason_test = reason_test[reason_test > 0]
    if array_positive_reason_test.size == 0:
        return -1
    value_min_reason_test = array_positive_reason_test.min()
    index_min_reason_test = np.where(reason_test == value_min_reason_test)

    return index_min_reason_test

def testRatioTableauOriginal(index):
    global arrayRestrictionValues,arrayVariableNoBasic
    indexLowestRatio = -1
    testRatio = 0
    for i in range (arrayRestrictionValues.size):
        comparation = arrayVariableNoBasic[i, index]
        if  comparation == 0 or arrayRestrictionValues[i] / arrayVariableNoBasic[i, index] < 0 :
            continue
        
        if i == 0:
            testRatio = arrayRestrictionValues[i] / comparation
            indexLowestRatio = i
        elif testRatio > arrayRestrictionValues[i] / comparation:
            testRatio =  arrayRestrictionValues[i] / comparation
            indexLowestRatio = i

    return indexLowestRatio

def swapColumns(indexColumnVariableEnter,indexColumnExitVariable):
    global arrayVariableBasic,arrayVariableNoBasic,arrayObjectiveFunctionVariableNoBasic,arrayObjectiveFunctionVariableBasic

    swapColumns = arrayObjectiveFunctionVariableBasic[indexColumnExitVariable] 
    arrayObjectiveFunctionVariableBasic[indexColumnExitVariable] = arrayObjectiveFunctionVariableNoBasic[indexColumnVariableEnter]
    arrayObjectiveFunctionVariableNoBasic[indexColumnVariableEnter] = swapColumns

    for i in range (len(arrayVariableNoBasic)):
        swapColumns = arrayVariableBasic[i,indexColumnExitVariable]
        arrayVariableBasic[i,indexColumnExitVariable] =  arrayVariableNoBasic[i,indexColumnVariableEnter]
        arrayVariableNoBasic[i,indexColumnVariableEnter] = swapColumns
    pass
    
def pivoment():
    newArrayObjectiveFunctionVariableNoBasic = calculateNewFOVariableNoBasic()
    verificationNegativeNumber = verificationExistsNegativeNumber(newArrayObjectiveFunctionVariableNoBasic)
    indexColumnExitVariablePivoment = None

    if verificationNegativeNumber == True:
        indexColumnVariableEnterPivoment = indexNegativeNumber(newArrayObjectiveFunctionVariableNoBasic)
        indexColumnExitVariablePivoment = testRatioTableau(indexColumnVariableEnterPivoment)
        if indexColumnExitVariablePivoment is not None and indexColumnExitVariablePivoment != -1:
            swapColumns(indexColumnVariableEnterPivoment, indexColumnExitVariablePivoment)  
        else:
            verificationNegativeNumber = False


    return verificationNegativeNumber, indexColumnExitVariablePivoment
    
def simplex(typeProblem):
    global arrayVariableBasic,arrayVariableNoBasic,arrayObjectiveFunctionVariableNoBasic,arrayObjectiveFunctionVariableBasic
    indexColumnExitVariable = None
    verificationPPLPossible = None
    verification = None
    
    negativeNumber = verificationExistsNegativeNumber(arrayObjectiveFunctionVariableNoBasic)
    if negativeNumber == True:
        indexColumnVariableEnter = indexNegativeNumber(arrayObjectiveFunctionVariableNoBasic)
        indexColumnExitVariable = testRatioTableauOriginal(indexColumnVariableEnter)
        if indexColumnExitVariable is not None and indexColumnExitVariable != -1:
            swapColumns(indexColumnVariableEnter, indexColumnExitVariable)

    if indexColumnExitVariable is not None and indexColumnExitVariable != -1 or typeProblem[:3] == 'Min' or typeProblem[:3] == 'min':
        while True:
            boolean, verification = pivoment()
            if boolean == False: break

    verificationPPLIlimited = verification if indexColumnExitVariable != -1 else indexColumnExitVariable
    if arrayObjectiveFunctionVariableBasic.max() > 0:
        verificationPPLPossible == False


    if verificationPPLIlimited == -1:
        print('Esse problema é ilimitado')
    elif verificationPPLPossible == False:
        print('Não existe solução para esse problema')
    else: 
        FO = np.dot(arrayObjectiveFunctionVariableBasic, np.dot(np.linalg.inv(arrayVariableBasic), arrayRestrictionValues))
        print(f'arrayRestrictionValues: {arrayRestrictionValues}')
        print(f'arrayVariableBasic: {arrayVariableBasic}')
        print(f'arrayVariableNoBasic: {arrayVariableNoBasic}')
        print(f'arrayObjectiveFunctionVariableNoBasic: {arrayObjectiveFunctionVariableNoBasic}')
        print(f'arrayObjectiveFunctionVariableBasic: {arrayObjectiveFunctionVariableBasic}')
        print(f'Resultado: {FO}')
        pass

def addColumn(matrixSign,tablue,matrixObjectiveFunction):
    numRow = tablue.shape[0]
    matrixSign = np.char.strip(matrixSign)
    filtearrayVariableNoBasic = matrixSign[matrixSign == '>=']
    numColumn = len(filtearrayVariableNoBasic)
    variableExcessColumn = np.zeros((numRow,numColumn))
    objectiveFunctionVariableExcess = np.zeros(numColumn)
    
    for row in range(len(matrixSign)):
        if matrixSign[row] == '>=':
            variableExcessColumn[row,row] = -1

    newTablue = np.hstack([tablue, variableExcessColumn])
    newObjectiveFunction = np.hstack([matrixObjectiveFunction, objectiveFunctionVariableExcess])
    indexArtificialVariable = np.flatnonzero((matrixSign == '>=') | (matrixSign == '='))

    return indexArtificialVariable, newTablue, newObjectiveFunction

def identifyArtificialVariable(matrixIndexArtificialVariable, matrixObjectiveFunctionVariableBasic, matrixObjectiveFunctionVariableNoBasic):
    highestValue = np.abs(matrixObjectiveFunctionVariableNoBasic).max()
    for row in range(len(matrixIndexArtificialVariable)):
        index = int(matrixObjectiveFunctionVariableNoBasic[row])
        matrixObjectiveFunctionVariableBasic[:index] = highestValue * 5

    pass

def inputData():
    global arrayVariableNoBasic, arrayVariableBasic, arrayObjectiveFunctionVariableNoBasic, arrayObjectiveFunctionVariableBasic, arrayRestrictionValues

    quantityVariable = int(input("Quantas váriaveis tem o problema: "))
    quantityRestrictions = int(input("Quantas restrições tem o problema: "))
    typeProblem = str(input("Informe o tipo do problema(Maximizar ou Minimizar): "))

    arrayVariableNoBasic = np.zeros((quantityRestrictions,quantityVariable))
    arrayVariableBasic = np.eye(quantityRestrictions)
    arrayRestrictionValues = np.zeros(quantityRestrictions)
    arrayObjectiveFunctionVariableNoBasic = np.zeros(quantityVariable)
    arrayObjectiveFunctionVariableBasic = np.zeros(quantityRestrictions)
    signOfRestrictions = []

    for rows in range(quantityRestrictions):
        print(f"\nInsira os coeficientes da linha{rows + 1}: ")
        sign = str(input(f"Qual sinal da restrição[{rows}]('<=', '>=', '='): "))
        signOfRestrictions.append(sign)
        for columns in range(quantityVariable):
            arrayVariableNoBasic[rows, columns] = float(input(f"Valor para posição [{rows}][{columns}]: "))
            
    for rows in range(quantityRestrictions):
        arrayRestrictionValues[rows] = float(input(f"Insira os valor da restrição[{rows}]: "))

    for columns in range(quantityVariable):
        arrayObjectiveFunctionVariableNoBasic[columns] = float(input(f"Insira os coeficientes da função objetivo: "))

    artificialVariableColumn = None
    for row in range(len(signOfRestrictions)):
        if np.any((signOfRestrictions[row] == '>=') | (signOfRestrictions[row] == '=')):
            artificialVariableColumn, arrayVariableNoBasic, arrayObjectiveFunctionVariableNoBasic = addColumn(signOfRestrictions, arrayVariableNoBasic, arrayObjectiveFunctionVariableNoBasic)
            break

    if artificialVariableColumn is not None and len(artificialVariableColumn) != 0:
        identifyArtificialVariable(artificialVariableColumn, arrayObjectiveFunctionVariableBasic, arrayObjectiveFunctionVariableNoBasic)

    if typeProblem[:3] == "Max" or typeProblem[:3] == 'max':
        arrayObjectiveFunctionVariableNoBasic = arrayObjectiveFunctionVariableNoBasic * -1   

    simplex(typeProblem)

inputData()