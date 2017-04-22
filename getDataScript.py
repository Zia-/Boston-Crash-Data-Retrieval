import urllib2, sys, os, json, datetime

### Usage:
# python ~/getDataScript.py ~/data_formatRaw.txt ~/data_format1.csv ~/data_format2.csv

def generateUrls(urlHead, urlIDsRange, urlTail):
    # Only 1000 features could be extracted from the server at a time
    urlList = []
    urlIDs = ""
    count = 0
    for i in range(urlIDsRange[0], urlIDsRange[1]):
        # Generating Urls per 1000 features and appending in a list
        if count % 1000 == 0 and count != 0:
            urlList.append(urlHead + urlIDs[:-1] + urlTail)
            urlIDs = ""
        urlIDs = urlIDs + str(i) + ","
        count += 1
    urlList.append(urlHead + urlIDs[:-1] + urlTail)
    print "Urls Generated"
    return urlList

def getDataFeatures(urls):
    # Store obtained data in dictionary format into a list
    def formatJson(data):
        for i in range(len(data['features'])):
            lat = data['features'][i]['geometry']['y']
            lng = data['features'][i]['geometry']['x']
            try:
                dateFormat = datetime.datetime.strptime(data['features'][i]['attributes']['Date'], "%m/%d/%Y %H:%M:%S %p")
            except:
                try:
                    dateFormat = datetime.datetime.strptime(data['features'][i]['attributes']['Date'], "%m/%d/%Y %H:%M:%S")
                except:
                    dateFormat = datetime.datetime.strptime(data['features'][i]['attributes']['Date'], "%m/%d/%Y")
            date = dateFormat.date()
            time = dateFormat.time()
            count = data['features'][i]['attributes']['Count']
            incident = data['features'][i]['attributes']['Incident']
            mode = data['features'][i]['attributes']['Mode']
            fid = data['features'][i]['attributes']['FID']
            key, value = ['lat','lng','date','time','count','incident','mode','fid'], [lat,lng,date,time,count,incident,mode,fid]
            dataList.append(dict(zip(key,value)))
    dataList = []
    for i in range(len(urls)):
        formatJson(json.loads(urllib2.urlopen(urls[i]).read()))
    print "Data Downloaded"
    return dataList

def writeResult2File(formatFun, data, resultFilePath):
    def writeFunc(formatFun, data, resultFilePath):
        # Function to save data in preferred format
        resultFile = open(os.path.join(resultFilePath), 'a')
        if formatFun == "formatRaw":
            # Raw Format.
            resultFile.write("%s\n" % data)
            resultFile.write("\n")
        elif formatFun == "format1":
            # First Format. Answer to Question 4 from the Quiz
            resultFile.write("%s,%s,%s,%s,%s\n" % ('INCIDENT','DATE','MODE','COUNT',''))
            dataString = ""
            for i in range(len(data)):
                dataString = dataString +  str(data[i]['incident'])+','+str(data[i]['date'])+' '+str(data[i]['time'])+','+str(data[i]['mode'])+','+str(data[i]['count'])+','+'('+str(data[i]['lat'])+','+str(data[i]['lng'])+')'+'\n'
            resultFile.write(dataString)
        elif formatFun == "format2":
            # `Second`Format. Answer to Question 5 from the Quiz
            resultFile.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % ('status/scripts','REPORTID','USERID','REPORTTYPEID','ADDEDBY','HOSTID','LATITUDE','LONGITUDE','RADIUSIMPACT','DESCRIPTION','PRICE','REPORTSTATUSID','DATE','TIME','CREATEDTIME','LASTMODIFIEDTIME','ADDRESS','TOTALNUMBERINJURED','TOTALNUMBERKILLED','VEHICLETYPECODE'))
            dataString = ""
            for i in range(len(data)):
                dataString = dataString +  ',,,,,,'+str(data[i]['lat'])+','+str(data[i]['lng'])+',,,,,'+str(data[i]['date'])+','+str(data[i]['time'])+',,,,,,'+'\n'
            resultFile.write(dataString)
        resultFile.close()
        print "Data Saved"
    try:
        # Try and Except in case already a file with passed name exists in the directory
        os.remove(resultFilePath)
        writeFunc(formatFun, data, resultFilePath)
    except:
        writeFunc(formatFun, data, resultFilePath)

if __name__ == '__main__':
    urls = generateUrls("http://gpd01.cityofboston.gov:6080/arcgis/rest/services/crashes_analysis/MapServer/6/query?f=json&returnGeometry=true&spatialRel=esriSpatialRelIntersects&objectIds=", [0,9229], "&outFields=*&outSR=102100") # Generate Urls
    data = getDataFeatures(urls) # Get Data from Server
    writeResult2File("formatRaw", data, sys.argv[1]) # Write Data to file in raw format.
    writeResult2File("format1", data, sys.argv[2]) # Write Data to file in first format
    writeResult2File("format2", data, sys.argv[3]) #  Write Data to file in second format
