import csv
import glob


def _file_length(dataPath):
    # how many records are there in the dataPath file
    with open(dataPath,'rb') as fff:
        length = 0
        reader = csv.reader(fff)
        for i, line in enumerate(reader):
            length = i
        fff.flush()
        fff.close()
        return length + 1


def _pair_boundary_or_not(dataPath):
    # determine whether the exit/entrance are paired
    with open(dataPath, 'rb') as fff:
        boundaryCount = 0
        reader = csv.reader(fff)
        for i, line in enumerate(reader):
            if line[5] == 'r':
                boundaryCount += 1
        fff.flush()
        fff.close()
        if boundaryCount % 2 == 0:
            return True
        else:
            return False


def _concatenate_based_on_order(regionID, fileID):
    # put all the data in parallel processing procedure together to form the whole data set

    destPath = 'the\\directory\\where\\your\\want\\to\\store\\the\\merged\\data'.format(str(regionID))
    path = 'the\\results\\directory\\of\\your\\parallel\\processing\\procedure'.format(str(regionID))
    fileformat = '.csv'
    file_number = fileID

    with open(destPath, 'wb') as output:
        writer = csv.writer(output)
        for i in range(1, file_number + 1, 1):
            filePath = path + str(i) + fileformat
            with open(filePath, 'rb') as separate:
                reader = csv.reader(separate)
                for i, matched in enumerate(reader):
                    writer.writerow(matched)
                separate.flush()
                separate.close()
        output.flush()
        output.close()


def _extract_use_data(regionID, areaID):
    # the whole map is divided into 40 regions and regionID is the index, areaID is the order of files
    # extract the boundary data and the noise data that are useful in walkway inference
    directory = 'your\\data\\directory\\with\\data\\classification\\labels'.format(str(regionID), str(areaID))
    counter = 0
    for oneDayDataRawPath in glob.glob(directory + "/*.csv"):
        counter += 1
        dest1 = oneDayDataRawPath[:oneDayDataRawPath.rfind('\\')]
        dest2 = '\\useful\\'
        dest3 = oneDayDataRawPath[oneDayDataRawPath.rfind('\\'):-4]
        oneDayDataUse = dest1 + dest2 + dest3 + '_useful.csv'
        if _file_length(oneDayDataRawPath) > 3:
            with open(oneDayDataRawPath, 'rb') as iFile:
                reader = csv.reader(iFile)
                with open(oneDayDataUse, 'wb') as oFile:
                    writer = csv.writer(oFile)
                    for i, line in enumerate(reader):
                        if line[5] == 'r' or line[6] == 'Noise':
                            writer.writerow(line)
                    oFile.flush()
                    oFile.close()
                iFile.flush()
                iFile.close()


def _remove_bondary_data(regionID,areaID):
    # remove the isolate boundary data between which there is no other locations
    directory = 'your\\data\\directory\\with\\data\\classification\\labels\\useful\\'.format(str(regionID), str(areaID))
    counter = 0
    for test in glob.glob(directory + "/*.csv"):
        counter += 1
        if _file_length(test) > 2:
            indicator_raw = []
            with open(test, 'rb') as iFile:
                reader = csv.reader(iFile)
                for line in reader:
                    if line[5] == 'b':
                        indicator_raw.append(1)
                    else:
                        indicator_raw.append(0)
                iFile.flush()
                iFile.close()
            indicator_raw[0] = 0
            indicator_update = []
            for i in range(len(indicator_raw)):
                if i == 0:
                    if indicator_raw[1] == 1:
                        indicator_update.append(1)
                    else:
                        indicator_update.append(0)
                elif i == len(indicator_raw) - 1:
                    if indicator_raw[i-1] == 1:
                        indicator_update.append(1)
                    else:
                        indicator_update.append(0)
                elif indicator_raw[i] or indicator_raw[i-1] or indicator_raw[i+1]:
                    indicator_update.append(1)
                else:
                    indicator_update.append(0)
            dest1 = test[:test.rfind('\\')]
            dest2 = '\\onlyBoundaryAndBetween\\'
            dest3 = test[test.rfind('\\'):-4]
            oneDayDataUsed = dest1 + dest2 + dest3 + '_used.csv'
            with open(oneDayDataUsed, 'wb') as ooFile:
                writer_removeBoundary = csv.writer(ooFile)
                with open(test, 'rb') as iiFile:
                    reader_removeBoundary = csv.reader(iiFile)
                    for i, line in enumerate(reader_removeBoundary):
                        if indicator_update[i] == 1:
                            writer_removeBoundary.writerow(line)
                    iiFile.flush()
                    iiFile.close()
                ooFile.flush()
                ooFile.close()


def _concatenate_files(regionID, areaID):
    # put all the separated files together
    dataPath = 'your\\results\\directory\\dataAll.csv'.format(str(regionID), str(areaID))
    filesPath = 'separated\\files\\directory\\useful\\onlyBoundaryAndBetween\\'.format(str(regionID), str(areaID))
    with open(dataPath, 'wb') as oFile:
        writer = csv.writer(oFile)
        for oneDayUsefulData in glob.glob(filesPath + "/*.csv"):
            if _pair_boundary_or_not(oneDayUsefulData):
                # ensure the locations at boundary are paired
                with open(oneDayUsefulData, 'rb') as iFile:
                    reader = csv.reader(iFile)
                    for i, line in enumerate(reader):
                        writer.writerow(line)
                    iFile.flush()
                    iFile.close()
        oFile.flush()
        oFile.close()


def _remove_boundary_without_between_data(regionID,areaID):
    # remove those boundary data between which there are not observations
    dataP1Path = 'your\\target\\file\\directory\\dataAll.csv'.format(str(regionID), str(areaID), str(areaID))
    testList = []
    with open(dataP1Path, 'rb') as testFile:
        reader = csv.reader(testFile)
        for i, line in enumerate(reader):
            if line[5] == 'r':
                testList.append(1)
            else:
                testList.append(0)
        testFile.flush()
        testFile.close()

    reserveGoodBoundary = []
    for i in range(len(testList)):
        if testList[i] == 1:
            if i == 0:
                if testList[i + 1] == 0:
                    reserveGoodBoundary.append(1)
                else:
                    reserveGoodBoundary.append(0)
            elif i == len(testList) - 1:
                if testList[i - 1] == 0:
                    reserveGoodBoundary.append(1)
                else:
                    reserveGoodBoundary.append(0)
            else:
                if testList[i - 1] == testList[i + 1]:
                    reserveGoodBoundary.append(0)
                else:
                    reserveGoodBoundary.append(1)
        else:
            reserveGoodBoundary.append(1)

    newPath = 'the\\directory\\of\\your\\new\\file\\dataAll_withoutBadBoundary.csv'.format(str(regionID), str(areaID), str(areaID))

    with open(newPath, 'wb') as ooFile:
        writer_removeBoundary = csv.writer(ooFile)
        with open(dataP1Path, 'rb') as iiFile:
            reader_removeBoundary = csv.reader(iiFile)
            for i, line in enumerate(reader_removeBoundary):
                if reserveGoodBoundary[i] == 1:
                    writer_removeBoundary.writerow(line)
            iiFile.flush()
            iiFile.close()
        ooFile.flush()
        ooFile.close()
