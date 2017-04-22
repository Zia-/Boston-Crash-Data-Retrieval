# Boston-Crash-Data-Retrieval
Retrieve Boston Crash Data from http://app01.cityofboston.gov/VisionZero/ portal

Followed Methodology To Obtain Vector Data and Make it Pretty ----

1. Initial investigation revealed that data at http://app01.cityofboston.gov/VisionZero/ from MapServer is in raster format and so vector data conversion and attributes generation are almost impossible. And therefore, library like Beautiful Soap etc. can't be used directly for vector data extraction.
2. A bit of play in the Developers' Section landed us up to the ArcGIS.com portal http://www.arcgis.com/home/webmap/viewer.html?url=http%3A%2F%2Fgpd01.cityofboston.gov%3A6080%2Farcgis%2Frest%2Fservices%2Fall_injuries_yearly%2FMapServer&source=sd via http://gpd01.cityofboston.gov:6080/arcgis/rest/services.
3. It should be noted that we are asked to obtain "Collision Data", and so we will be using "crash analysis" dataset and not the "all_fatalities____" or "all_injuries____". ![alt tag](https://raw.githubusercontent.com/Zia-/Boston-Crash-Data-Retrieval/master/screenshots/1.png)
4. Going to the respective ArcGIS.com My Map page gave us the url which could be used to pull out vector data in json format. [alt tag2](https://raw.githubusercontent.com/Zia-/Boston-Crash-Data-Retrieval/master/screenshots/2.png)
5. Once we had this url all we did is to generate custom url to cover all "objectIds" for 9229 features.
6. Now run the script getDataScript.py to download and format data according to taste.
