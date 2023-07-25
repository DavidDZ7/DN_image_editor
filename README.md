# DN_image_editor
A Python-based image editor made by [David Norman Díaz Estrada](https://www.linkedin.com/in/dnde7/)



------------------
**Color Mapping:**<br/>
------------------
The Color Mapping filter allows to apply any 8-color palette to an input image.
The current version has the following features:
<ul>
  <li>Edit and save any custom palette to the palette database.</li>
  <li>Palette generation based on a linear gradient between any two colors.</li>
  <li>Palette extraction from any image using the k-means algorithm (tones from image).</li>
  <li>Color mapping modes: Fuzzy, Euclidean, and Light-based.</li>
  <li>The Fuzzy mode allows the user to adjust the "weight" of each color during mapping by moving the sliders.</li>
</ul>

Here is an example of color Mapping using a photo I took in Oslo:
<img src="readmeFiles/DN_app_01.png" >

These are some other examples with diverse palettes:
<img src="readmeFiles/examples_paletteMapping.png" >


------------------
**Installation:**<br/>
------------------
DN Image Editor requires the following dependencies: OpenCV, Scikit-learn, NumPy, Matplotlib, Tkinter, CustomTkinter, and Pillow.

First, clone this repo, you can do:
```
git clone https://github.com/DavidDZ7/DN_image_editor.git
```
Then, go to Anaconda prompt and navigate to the folder repo and proceed as follows:
```
conda create --name DNimageEditor python=3.7.7
conda activate DNimageEditor
pip install -r requirements.txt
```
Your environment is now ready, you can launch DN Image Editor by running:
```
python GUI_DN_Image_Editor.py
```


