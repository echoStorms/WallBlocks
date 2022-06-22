# Wallblocks

## A block wallpaper generator

I haven't worked on this project for some time, so I need to dive in and write a description of where I'm at for now.
For now I have verified it still worked on the first try! Hurray!

Next I want to make sure I understand what the dependencies are for the project and create a way to install them.

---

Wallblocks allows you to specify a folder and it will generate a wallpaper from all the images in that folder.
The image generated will be of the size of the screen you are on.


You can do the following:
- Specify a folder to generate a wallpaper from
- Specify a folder to save the wallpaper to
- Specify a style to use for the wallpaper
- Create wallpapers in batches
- TODO: Set wallpaper for MacOS on a timer

### Quick Start
- Run wallblocks like this:
```python main.py --input ~/Wallpapers -o /tmp```

- TODO: How to install: ???

- TODO: Example usage: ???


### Styles

In order to describe the style, I had to come up with a system that would allow me to describe the style of the wallpaper.

Styles are current defined in a Python as a 2D matrix (8 wide by 6 tall - list of lists) in the `layouts.py` file.

The styles are read left-to-right, top-to-bottom.

The numbers in the matrix define the dimensions as well as the orientation of the image.

1. Zero
    - No image
2. Perfect squares
    - Image is square
    - Image occupies the square root of the number
    - eg. 4 will be a 2x2 image
    - eg. 9 will be a 3x3 image
3. Positive non-perfect squares
    - Image is a horizontal rectangle
    - Image occupies the number of squares horizontally
    - eg. 2 will be a 2x1 image
    - eg. 5 will be a 5x1 image
4. Negative non-perfect squares
    - Image is a vertical rectangle
    - Image occupies the number of squares vertically
    - eg. -2 will be a 1x2 image
    - eg. -3 will be a 1x3 image

### what do i want to be able to do?

- change the style of setting the wallpaper (i.e. fill, stretched, center)
- provide cli tool
- provide gui tool for Mac

### TDD
mosaic_generator
    new_image_in_directory
    correct_image generated
wallpaper_setter
    new_image
        image_is_found
        list_is_appended
        current_image_changed
    prev_image
        list_is_used
        image_is_found
    next_image
        list_is_used
        image_is_found
    
