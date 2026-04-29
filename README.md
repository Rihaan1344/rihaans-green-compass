# **Welcome to Rihaan's Green Compass**

I, Rihaan, student of 9J, studying in Oakridge International School have developed this app on account of _Earth Day 2026._

If you have a tree you wish to identify, simply take a photo of the bark of the tree and leaf of the tree, and upload it to the code. It'll automatically give you the _scientific taxonomy_ and a poster, consisting of the _classification_ and _images_ you uploaded!

This is the github repository with all the code!

If you are a non-developer, and a user, you may run the application properly at this [link](https://coding-but-better-dxagxmwkxdwy5nubjc5jrh.streamlit.app/).

> [!TIP]
> ### The `static` folder contains pairs of images taken from the same tree(_bark and leaf_), and you can use them for testing!

***

> [!CAUTION] 
> ## The following is a technical comment for developers!

This app uses two API keys: [PlantnetAPI](https://my.plantnet.org/) and [IMGbbAPI](https://api.imgbb.com/).

They are very simple APIs, with _no authentication chaos_. You can use `post requests` with the python `requests` module to interact with the APIs.

**PlantNet API** is used to _classify the tree from the images_, and requires image in form of binary(or certain other forms, check documentation). It gives you a quota of _500 requests per day_, which is a lot, especially for free!

**ImgBB API** is used for _uploading the image_, because to generate a QR Code, the python `qrcode` module requires a link. It gives _1000 uses per day_ which is excellent!

Also, for **verson 1 of the app**, instead of generating on the image on my own, I used an API known as [TemplatedAPI](https://templated.io/docs/) where you basically create a template on your own on the webpage, then make `http requests` with all the data you want to fill in _placeholders_, which you can again define during creation of the template.

However, templated API is limited to _50 uses_ for **life**, which is why I decided to switch my logic.

You can get your own keys and run it locally with the links provided. 

Of course I didn't push my .env file and variables! And you better not make that mistake either, sneaky devs :)

Okay, bye!
