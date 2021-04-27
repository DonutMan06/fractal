![fractals_picture](https://github.com/DonutMan06/DonutMan06/blob/main/fractal.png)


# fractal
A simple Python GUI that dynamically draws custom fractals

Just download the Python script and run it.
It will display a Matplotlib basic GUI where you can update :
* the order k of the fractal
* the alpha parameter of the fractal, which drives the amplitude ratio
* the omega parameter of the fractal, which drives the edge number of the fractal

Please be aware that above order-2, the equations are just numerically estimated.
Even if there is no boundary in the code, you should avoid order above 8, since it will imply a (very) huge amount of points.

For a better description of the equations used here, please refer to [my blog](http://blog.les-vigneron.fr/mathematique/cas-de-folie-circulaire/).
