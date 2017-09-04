# PhanterMobileConstructor
Create your mobile aplication using web2py

  - On init create this folders structure if not exists:
     
        web2py
          | - cordova
                |-folderAppCordova

  - The name of folderAppCordova is the same of your web2py aplication
      Cointains the default cordova app

  - On Web2py Developer, inside of plugin_phantermobileconstructor, 
      all functions started with "www_" will be rendered in the cordova application (on buildHtml method)
      and all files in static/plugin_phantermobileconstructor/www will be copied to the www folder of cordova App

      exemple:
      
          - On controller/plugin_phantermobileconstructor.py (web2py)
              def www_index():
                  #your code
                  return dict()
              def www_other_function():
                  return DIV("my div")
                  
          - On static/plugin_phantermobileconstructor/www
              static/plugin_phantermobileconstructor/www/
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
NOTE: In Linux the server many features have not been implemented, in windows many functions are executed through batch files (.bat), below the list of commands that will have to be made manually in linux to work.

In the web2py folder, create a folder named cordova.
Then create a cordova application with the same name as your web2py application (I'll use the web2py welcome application as an example)

  -To create your first Cordova application

    $ls web2py_folder/cordova
    $cordova create welcome com.yoursite.www welcome

  -to open the phonegap server

    $ls web2py_folder/cordova/your_app_name
    $phonegap serve -p3000

  -if you prefer to use the cordova server

      $ls web2py_folder/cordova/your_app_name
      $cordova serve 3000

  -to create the apk of your application
  
      $ls web2py_folder/cordova/your_app_name
      $cordova platform remove android
      $cordova platform add android
      $cordova build android
