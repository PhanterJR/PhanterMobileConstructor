# PhanterMobileConstructor
Plugin do Web2py para criação de aplicativos mobile utilizando cordova phonegap

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
          - On controller plugin_phantermobileconstructor.py
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
