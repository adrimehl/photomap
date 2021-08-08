# photomap - Create maps with markers and pictures at the locations where the picture was taken

This Program lets you run through all the pictures in a given folder and results in a .html openstreetmap layer file which shows the location of the pictures with a marker. If you hover over the marker, the date of when the picture was taken gets shown, if you click on the marker, a frame pops up that shows the picture. 
You can choose between different options on how the data should be represented:

* Marker: Choice between the default marker or a chosen picture as marker
* Clustering: Chosse if the markers should be clustered when zoomed out or not


# Motivation and Disclaimer

The idea came up after a long road trip to show all the pictures of the journey on a map instead of scrolling through the folder. This is a nice feature if you have moved around a lot and want to give a short and quick overview of all the places you've been. It's also a nice way of getting a timeline of your last year if you plot all the pictures that you did on your phone within the last year (Covid times 2020/21 must be exciting ;)).

# Usage

Usage is easy. The different settings can be defined in lines 19-28:

* add the link to the folder with the pictures. All pictures that have information of the GPS location are being used, if no GPS information is available, the pictures will not be used. 
* Chosse if a customized marker should be used: If True, then choose which image should be used.
* Define if clustering of the markers should be activated or not
* Define the center of the  loaction if the map gets opened

# Examples
Markers with clustering:\
<img src="https://github.com/adrimehl/photomap/blob/main/Example_with_clustering.PNG" width="700">

Markers without clustering:\
<img src="https://github.com/adrimehl/photomap/blob/main/Example_without_clustering.PNG" width="700">

Example of picture:\
<img src="https://github.com/adrimehl/photomap/blob/main/Example_image_shown.png" width="700">



# Author

Adrian Mehl
