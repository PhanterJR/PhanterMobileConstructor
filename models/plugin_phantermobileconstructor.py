# -*- coding: utf-8 -*-
# python 3 comtability
from __future__ import print_function
from io import open

# battery inclued
import os
import zipfile
from PIL import Image as PilImage

# personal import
from plugin_phantermobileconstructor.phantermenubar import PhanterMenubar
from plugin_phantermobileconstructor.phanterandroidvalidator import RECOMMENDED_MIN_SIZE, IS_PNG

if not os.path.exists(os.path.join(request.folder, 'controllers', 'www.py')) \
        and not os.path.exists(os.path.join(request.folder, 'static', 'www')) \
        and not os.path.exists(os.path.join(request.folder, 'models', 'www.py')) \
        and not os.path.exists(os.path.join(request.folder, 'views', 'www')) \
        and (request.controller=='plugin_phantermobileconstructor') \
        and (request.function=='index'):
    from plugin_phantermobileconstructor.phanterandroid import PhanterAndroid
    from plugin_phantermobileconstructor.phanterajaxdevelopment import PhanterAjaxDevelopment
    print('creating controller "www.py", model "www.py", www static folder files and www in views.')
    zip_ref = zipfile.ZipFile(os.path.join(request.folder,  'modules',
        'plugin_phantermobileconstructor', 'phanterandroidpack', 'www.zip'), 'r')
    zip_ref.extractall(os.path.join(request.folder))
    zip_ref.close()    
    phanterandroid = PhanterAndroid('www')

response.toolbar_mob = DIV(
    DIV(A(T('Web2py ToolBar'), _style="color: #440808;", _href="#caixa_response_toolbar"),
      _class='botao_response_toolbar',
      _style='cursor:pointer; position: fixed;right: 0; bottom: 45px; width: 93px; padding: 5px; background-color: orange; text-transform: uppercase; font-weight: bold;font-size: 8pt;padding-left: 10px;box-shadow: -1px 2px 3px black;',
      _onclick='$("#caixa_response_toolbar").toggle();'),
    DIV(response.toolbar(),
      _id='caixa_response_toolbar',
      _style='background-color:white; padding:5px; display:none;'),
    _style='position:relative; z-index:1005; width:100%;')


if request.controller == 'plugin_phantermobileconstructor':

    lista_links = [DIV(DIV(I(_class="glyphicon glyphicon-menu-hamburger"), _alvo=".grupo_links", _class='botao_hamburguer responsivo'),
                       DIV(A(DIV(XML("&#160;"), _class='botao_conexao responsivo'), _href="http://www.conexaodidata.com.br"),
                           A(DIV("PhanterMobile Constructor", _class='menu_item responsivo'),
                             _href=URL('plugin_phantermobileconstructor', 'index')),
                           A(DIV("Admin", _class='menu_item responsivo'),
                             _href=URL('admin', 'default', 'index')),
                           A(DIV("Appadmin", _class='menu_item responsivo'), _href=URL(
                               'appadmin', 'index')),
                           _class='grupo_links responsivo')),
                   ]
    response.nav_phantermenubar = PhanterMenubar(
        *lista_links, _class="barra_navegacao responsivo")

db.define_table('plugin_phantermobileconstructor_keystore',
                Field('keytool', 'string',
                      label=CAT(T('keytool'), 
                        SPAN(" ?",
                            _class="help",
                            _title=T("Program keytool from JavaDK."))),
                      requires=IS_NOT_EMPTY(),
                      ),
                Field('keyname', 'string', default='phantermobile',
                      label=CAT(T("keyname"),
                        SPAN(" ?",
                            _class='help',
                            _title=T("Name of keystore"))),
                      requires=IS_NOT_EMPTY(),
                      ),
                Field('aliasname', 'string', default='PhanterMobile',
                      label=CAT(T("aliasname"),
                        SPAN(" ?",
                            _class='help',
                            _title=T("Alias of keystore"))),
                      requires=IS_NOT_EMPTY(),
                      ),
                Field('validity', 'string', default="10000",
                      label=CAT(T("validity"),
                        SPAN(" ?",
                            _class='help', 
                            _title=T("Days to expirates the certifield"))),
                      requires=IS_NOT_EMPTY(),
                      ),
                Field('storepass', 'string',
                      label=CAT(T("storepass"),
                        SPAN(" ?",
                            _class='help',
                            _title=T("keystore password"))),
                      requires=IS_NOT_EMPTY(),
                      ),
                Field('keypass', 'string',
                      label=CAT(T("keypass"),
                        SPAN(" ?",
                            _class='help',
                            _title=T('key password'))),
                      requires=IS_NOT_EMPTY(),
                      ),
                Field('common_name', 'string', default='PhanterJR',
                      label=CAT(T("common_name"),
                        SPAN(" ?", 
                            _class='help', 
                            _title=T("Adicional Infomation (eg. Your Name)"))),
                      requires=IS_NOT_EMPTY(),
                      ),
                Field('organization_unit', 'string', default="PhanterMobile",
                      label=CAT(T("organization_unit"),
                        SPAN(" ?",
                            _class='help',
                            _title=T("Organization unit (eg. PhanterMobile)"))),
                      requires=IS_NOT_EMPTY(),
                      ),
                Field('organization', 'string', default="Conexao Didata",
                      label=CAT(T("organization"),
                        SPAN(" ?",
                            _class='help', 
                            _title=T("Your Organization (eg. Conexão Didata)"))),
                      requires=IS_NOT_EMPTY(),
                      ),
                Field('district', 'string', default="Aracaju",
                      label=CAT(T("district"),
                        SPAN(" ?",
                            _class='help',
                            _title=T("Your District (eg. Aracaju)"))),
                      requires=IS_NOT_EMPTY(),
                      ),
                Field('yourstate', 'string', default="Sergipe",
                      label=CAT(T("state"),
                        SPAN(" ?",
                            _class='help',
                            _title=T("Your State (eg. Sergipe)"))),
                      requires=IS_NOT_EMPTY(),
                      ),
                Field('country', 'string', default="BR",
                      label=CAT(T("country"),
                        SPAN(" ?",
                            _class='help',
                            _title=T("Your Country (eg. BR)"))),
                      requires=IS_NOT_EMPTY(),
                      ),
                Field('appkeystore', 'upload', autodelete=True),
                )

# Storage APKs and app info
db.define_table('plugin_phantermobileconstructor_apps',
                Field('appname', 'string', default=request.application,
                      label=T('App Name'), requires=IS_NOT_EMPTY()),
                Field('idapp', 'string',
                      default="com.yoursite.%s" % request.application,
                      label=CAT(T('ID'), 
                        SPAN(" ?",
                            _class="help", 
                            _title=T("Specifies the app's reverse-domain identifier, and the version its full \
                                version number expressed in major/minor/patch notation."))),
                      requires=IS_NOT_EMPTY()
                      ),
                Field('description', 'text',
                      default="A sample from PhanterMobile Constructor using web2py, phonegap and cordova.",
                      label=CAT(T('Description'), 
                        SPAN(" ?",
                            _class="help", 
                            _title=T("Specifies metadata that may appear within app-store listings.")))
                      ),
                Field('apkversion', 'string',
                      default="0.0.1",
                      label=CAT(T('Version'), 
                        SPAN(" ?",
                            _class="help", 
                            _title=T("Full version number expressed in major/minor/patch notation."))),
                      requires=IS_NOT_EMPTY()
                      ),
                Field('authorname', 'string',
                      default="PhanterMobile",
                      label=CAT(T('Name of the author'), 
                        SPAN(" ?",
                            _class="help", 
                            _title=T("Name that may appear within app-store lisitngs."))),
                      requires=IS_NOT_EMPTY()
                      ),
                Field('authoremail', 'string',
                      default="contato@conexaodidata.com.br",
                      label=CAT(T('Email of the author'), 
                        SPAN(" ?",
                            _class="help", 
                            _title=T("Email that may appear within app-store lisitngs."))),
                      requires=[IS_NOT_EMPTY(), IS_EMAIL()]
                      ),
                Field('authorwebsite', 'string',
                      default="http://conexaodidata.com.br/phantermobileconstructor",
                      label=CAT(T('Website of the author'), 
                        SPAN(" ?",
                            _class="help", 
                            _title=T("Website that may appear within app-store lisitngs."))),
                      requires=IS_NOT_EMPTY()
                      ),
                Field('externalacess', 'list:string',
                      default=["*"],
                      label=CAT(T('Access origin'), 
                        SPAN(" ?",
                            _class="help", 
                            _title=T("Defines the set of external domains the app is allowed to communicate with."))),
                      ),
                Field('allownavigation', 'list:string',
                      label=CAT(T('Allow Navigation'), 
                        SPAN(" ?",
                            _class="help", 
                            _title=T("Defines the set of external domains the WebView is allowed to navigate to."))),
                      ),
                Field('allowintent', 'list:string',
                      default=["http://*/*", "https://*/*",
                               "tel:*", "sms:*", "mailto:*", "geo:*"],
                      label=CAT(T('Allow-Intent'), 
                        SPAN(" ?",
                            _class="help", 
                            _title=T("Defines which URLs the app is allowed to ask the system to open."))),
                      requires=IS_NOT_EMPTY()
                      )
                )

db.define_table('plugin_phantermobileconstructor_apks',
                Field('application', 'reference plugin_phantermobileconstructor_apps', 
                    default=db(db.plugin_phantermobileconstructor_apps).select().first().id if not \
                        db(db.plugin_phantermobileconstructor_apps).isempty() else '', 
                    requires=IS_IN_DB(db, db.plugin_phantermobileconstructor_apps, "%(appname)s - %(idapp)s - %(apkversion)s")),
                Field('apklevel', 'string', default='debug',
                      label=CAT(T('Build type'), 
                        SPAN(" ?",
                            _class="help", 
                            _title=T("Perform a release build or Perform a debug build"))),
                      requires=IS_IN_SET(['debug', 'release'])),
                Field('signed', 'boolean', default=False),
                Field('apkfile', 'upload', autodelete=True),
                )

db.define_table('plugin_phantermobileconstructor_icon',
    Field('icon', 'upload', autodelete=True)
    )

db.define_table('plugin_phantermobileconstructor_splash',
    Field('splash_portrait', 'upload', autodelete=True),
    Field('splash_landscape', 'upload', autodelete=True)
    )

db.plugin_phantermobileconstructor_icon.icon.requires=[IS_PNG()]
db.plugin_phantermobileconstructor_splash.splash_portrait.requires=[IS_PNG()]
db.plugin_phantermobileconstructor_splash.splash_landscape.requires=[IS_PNG()]

db.define_table('plugin_phantermobileconstructor_plugins',
    Field('plugin_battery_status', 'boolean', default=False,
        label=CAT(T('Battery Status'), 
            SPAN(" ?",
                _class="help_plugs", 
                _title=T("Get events for device battery level.")))
        ),
    Field('plugin_camera', 'boolean', default=False,
        label=CAT(T('Camera'), 
            SPAN(" ?",
                _class="help_plugs", 
                _title=T("Take pictures with the device camera.")))
        ),
    Field('plugin_console', 'boolean', default=False,
        label=CAT(T('Console'), 
            SPAN(" ?",
                _class="help_plugs", 
                _title=T("Get JavaScript logs in your native logs.")))
        ),
    Field('plugin_contacts', 'boolean', default=False,
        label=CAT(T('Contacts'), 
            SPAN(" ?",
                _class="help_plugs", 
                _title=T("Manage the contacts on the device.")))
        ),
    Field('plugin_device', 'boolean', default=False,
        label=CAT(T('Device'), 
            SPAN(" ?",
                _class="help_plugs", 
                _title=T("Get device information.")))
        ),
    Field('plugin_device_motion', 'boolean', default=False,
        label=CAT(T('Device Motion'), 
            SPAN(" ?",
                _class="help_plugs", 
                _title=T("Access accelerometer data.")))
        ),
    Field('plugin_device_orientation', 'boolean', default=False,
        label=CAT(T('Device Orientation'), 
            SPAN(" ?",
                _class="help_plugs", 
                _title=T("Access compass data.")))
        ),
    Field('plugin_dialogs', 'boolean', default=False,
        label=CAT(T('Dialogs'), 
            SPAN(" ?",
                _class="help_plugs", 
                _title=T("Use native dialog UI elements")))
        ),
    Field('plugin_file', 'boolean', default=False,
        label=CAT(T('File'), 
            SPAN(" ?",
                _class="help_plugs", 
                _title=T("Read/write files on the device.")))
        ),
    Field('plugin_file_transfer', 'boolean', default=False,
        label=CAT(T('File Transfer'), 
            SPAN(" ?",
                _class="help_plugs", 
                _title=T("Upload and download files.")))
        ),
    Field('plugin_geolocation', 'boolean', default=False,
        label=CAT(T('Geolocation'), 
            SPAN(" ?",
                _class="help_plugs", 
                _title=T("Access GPS data.")))
        ),
    Field('plugin_globalization', 'boolean', default=False,
        label=CAT(T('Globalization'), 
            SPAN(" ?",
                _class="help_plugs", 
                _title=T("Access locale data.")))
        ),
    Field('plugin_inappbrowser', 'boolean', default=False,
        label=CAT(T('Inappbrowser'), 
            SPAN(" ?",
                _class="help_plugs", 
                _title=T("Open an in-app browser window.")))
        ),
    Field('plugin_media', 'boolean', default=False,
        label=CAT(T('Media'), 
            SPAN(" ?",
                _class="help_plugs", 
                _title=T("Record and play audio on the device.")))
        ),
    Field('plugin_media_capture', 'boolean', default=False,
        label=CAT(T('Media Capture'), 
            SPAN(" ?",
                _class="help_plugs", 
                _title=T("Capture audio, video, and images.")))
        ),
    Field('plugin_network_information', 'boolean', default=False,
        label=CAT(T('Network Information'), 
            SPAN(" ?",
                _class="help_plugs", 
                _title=T("Get information about wireless connectivity.")))
        ),
    Field('plugin_vibration', 'boolean', default=False,
        label=CAT(T('Vibration'), 
            SPAN(" ?",
                _class="help_plugs", 
                _title=T("Vibrate the device.")))
        ),
    Field('plugin_statusbar', 'boolean', default=False,
        label=CAT(T('Statusbar'), 
            SPAN(" ?",
                _class="help_plugs", 
                _title=T("Control the device status bar.")))
   ), 
)






