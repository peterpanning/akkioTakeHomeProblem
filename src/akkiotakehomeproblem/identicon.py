from PIL import Image, ImageDraw, ImageColor
import random

"""
Problem statement: 

Users often work collaboratively in digital environments where a profile picture is not available. 

Some platforms have attempted to solve this problem with the creation of randomly generated, unique icons for each user 
([github](https://github.blog/2013-08-14-identicons/), 
[slack](https://slack.zendesk.com/hc/article_attachments/360048182573/Screen_Shot_2019-10-01_at_5.08.29_PM.png), 
[ethereum wallets](https://github.com/ethereum/blockies)) sometimes called *Identicons*. 

Given an arbitrary string, create an image that can serve as a unique identifier for a user of a B2B productivity app 
like slack, notion, etc.

**Requirements**

Given an arbitrary string, generate an image 

Images should be reasonably unique 

No dedicated identicon-generating library 

Define a set of objectives to accomplish with your identicon. Here are some hypothetical objectives:

* Legibility at some scale or set of scales 
* Uniqueness vs similarity -- should similar strings look similar?  
* Appearance -- how do we avoid generating images that look bad? 


**Objectives** 

* Size/shape constraints: 
    * Images will be generated at 1200x1200 by default. Users can request 20x20 - 1600x1600. 
    * Images will be square to avoid vertical/horizontal stretching/compression  
* Uniqueness vs similarity: 
    * Identicons will be unique by username. We will not give any special consideration to similar names 
      creating similar or different identicons beyond this uniqueness. If we wanted to, we could create a custom
      hash method to enable this with choice of entropy generation. 
* Appearance: 
    * Identicons will be composed of rectangles to avoid aliasing when enlarging the image 
    * Identicons should be vertically symmetrical to imitate human faces
    * Exactly three RGB colors 

"""


class FillData:
    def __init__(self, bits_array, color):
        self.bits_array = bits_array
        self.color = color


def fill_grid(draw, grid_size, square_size, padding, fills, *args, **kwargs):
    for fill in fills:
        # Fill the grid based on the binary strings
        for y in range(grid_size):
            # Only draw left half, mirror the rest, +1 // 2 handles evens and odds w/o off-by-ones
            for x in range((grid_size + 1) // 2):
                index = x + y * (grid_size // 2 + 1)
                if fill.bits_array[index] == '1':
                    x1 = padding + x * square_size
                    y1 = padding + y * square_size
                    x2 = x1 + square_size
                    y2 = y1 + square_size
                    draw.rectangle([x1, y1, x2, y2], fill=fill.color)

                    # Mirror the square to the other side
                    x1 = padding + (grid_size - 1 - x) * square_size
                    x2 = x1 + square_size
                    draw.rectangle([x1, y1, x2, y2], fill=fill.color)


def generate_identicon(text, image_size=1200, grid_size=7):
    if image_size < 20:
        raise ValueError("Image size must be greater than or equal to 20")
    if image_size > 1600:
        raise ValueError("Image size must be less than or equal to 1600")

    # Generate two random strings of 0s and 1s for shapes. Image size is guaranteed long enough,
    # array could probably be shorter
    # Use of username as seed guarantees reproducibility in this context, but with a slightly different
    # implementation (calls to random without re-seeding) could allow a user to re-roll their identicon
    random.seed(text)
    primary_bits = format(random.getrandbits(image_size), '0b')
    secondary_bits = format(random.getrandbits(image_size), '0b')

    # Assign three random web-safe colors to background, primary, and secondary
    colors = random.sample(list(ImageColor.colormap.keys()), 3)
    background_color, primary_fill_color, secondary_fill_color = colors

    # Draw background
    image = Image.new('RGB', (image_size, image_size), background_color)
    draw = ImageDraw.Draw(image)

    padding = image_size // 20

    # Determine the size of each square in the grid
    square_size = (image_size - padding * 2) // grid_size

    fill_data = [
        FillData(primary_bits, primary_fill_color),
        FillData(secondary_bits, secondary_fill_color)
    ]

    fill_grid(draw, grid_size, square_size, padding, fill_data)

    return image
