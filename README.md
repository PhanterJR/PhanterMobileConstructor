# PhanterMobile Constructor
Create your mobile aplication using web2py

Requeriments:

  - windows (suport linux in tests)
  - web2py
  - python 2.7 (suport python 3 in tests)
  - cordova (npm install -g cordova)
  - phonegap (optional server, npm install -g phonegap)
  - corsproxy (ajax CORS suport, npm install -g corsproxy)
  - psutil (pip install psutil)
  - javaSDK (Javac(cordova requirements) and Keytool(sing apk))
  - Android Studio and androidSDK (cordova requirements)

Structure:

  - On init create this folders structure if not exists:
     
        web2py
          | - cordova
                |-folderAppCordova

  - The name of folderAppCordova is the same of your web2py aplication
      Cointains the default cordova app

  - In the first run of the plugin, if you create a www controller, a www templates, a www folder will be created in the views and in the static folder, where it is placed as views and files.
The following structure will be created in cordova in relation to the structure of web2py:

      exemple:
      
          - On controller/www.py (web2py)
              def index():
                  #your code
                  return dict()
              def Other_function():
                  return DIV("my div")
                  
          - On static/www
              static/www/
                      |-css/
                          |-mycss.css
                          |-outhes.css
                      |-images/
                          |-myimage.jpg
                      |-js/
                          |-Jquery.js
                          
          - will generate the following structure in the cordova application:
              folderAppCordova/
                  |-www/
                      |-index.html
                      |-outher_function.html
                      |-css/
                          |-mycss.css
                          |-outhes.css
                      |-images/
                          |-myimage.jpg
                      |-js/
                          |-Jquery.js


Features
  
  - Edit config.xml (cordova project)
  - Views in cordova server or phonegap server
  - Create keystore (keytool)
  - Build debug and release APK (Stored by version in sqllite database)
