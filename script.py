import random
import base64
import json
from html2image import Html2Image

print(' - - - - - - - - N F T   G R I D   L I N E S   G E N E R A T O R - - - - - - - -')

size = int(120)

full_dimension = int(3000)
dimension = int(full_dimension - (size * 2))
grid = int(dimension / size)

color_list = ['amber', 'red', 'green', 'orange', 'blue', 'pink', 'purple', 'lime', 'aqua']
variant_list = ['', '-reverse', '-curve-vertical', '-curve-horizontal', '-reverse-curve-vertical', '-reverse-curve-horizontal']

left = int(120)
top = int(120)

hti = Html2Image(
    output_path='dist',
    custom_flags=['--virtual-time-budget=10000', '--hide-scrollbars', '--disk-cache-dir=/tmp', '--user-data-dir=/tmp', '--crash-dumps-dir=/tmp']
)

cells = str('')

for v in range(3):
    print('Start create a variantion N%s' % v)

    row = []

    for y in range(grid):
        col = []

        if y != 0:
            top = size * (y + 1)

        for x in range(grid):
            if x != 0:
                left = size * (x + 1)

            color = random.randint(0, len(color_list) - 1)
            variant = random.randint(0, len(variant_list) - 1)

            name = color_list[color] + variant_list[variant]

            image_64 = str('')
            with open('images/lines/%s.png' % (name), 'rb') as image_file:
                image_64 = base64.b64encode(image_file.read())

            image = 'data:image/png;base64,%s' % (image_64.decode('utf-8'))

            col.append('{}{}'.format(color, variant))

            cells += '<div class="cell" style="left: %spx; top: %spx;"><img src="data:%s" alt="" /></div>' % (left, top, image)

        left = size
        row.append(col)
    else:
        html = "<body>%s</body>" % (cells)

        grid = random.randint(1, 4)

        bg_64 = str('')
        with open('images/grid/grid%s.png' % (grid), 'rb') as image_file:
            bg_64 = base64.b64encode(image_file.read())

        name = 'v-%s%s' % (grid, v)

        variation = open('dist/%s.json' % (name), 'w')
        variation.write(json.dumps({ 'd': row }, sort_keys=True, indent=4))
        variation.close()

        hti.screenshot(
            html_str=html,
            css_str='body{width:3000px;height:3000px;position:relative;background:url("data:image/png;base64,%s") no-repeat;padding:0;margin:0}.cell{position:absolute;z-index:2;top:120px;left:120px;width:120px;height:120px}' % (bg_64.decode('utf-8')),
            size=(3000, 3000),
            save_as='%s.png' % (name),
        )

        print('End create a variantion N%s' % v)
