import cv2
from PIL import Image
import requests
import json
import sys

with open('variables.json') as variables:
    variables = json.loads(variables.read())
    video_file = sys.argv[1] if len(sys.argv) > 1 else variables['VIDEO_FILE']
    cap = cv2.VideoCapture(video_file)
    frame_quantity = variables['FRAME_QUANTITY'] if variables['FRAME_QUANTITY'] > 0 and variables['FRAME_QUANTITY'] <= int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) else int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    pixel_density = variables['PIXEL_DENSITY']
    aspect_ratio = variables['ASPECT_RATIO'] if 'ASPECT_RATIO' in variables else int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) / int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    unicode_art = []

    for i in range(frame_quantity):
        ret, frame = cap.read()
        if not ret:
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        pil_img = Image.fromarray(gray_frame)
        term_height = int(pixel_density / aspect_ratio)
        pil_img = pil_img.resize((pixel_density, int(term_height * 0.47472119645)))

        unicode_frame = []
        for y in range(pil_img.height):
            row = ''
            for x in range(pil_img.width):
                pixel = pil_img.getpixel((x, y))
                intensity = pixel / 255
                if intensity > 0.8:
                    row += ' '
                elif intensity > 0.6:
                    row += '.'
                elif intensity > 0.4:
                    row += '*'
                elif intensity > 0.2:
                    row += ':'
                else:
                    row += '#'
            unicode_frame.append(row)

        unicode_art.append('\n'.join(unicode_frame))
        sys.stdout.write(f'\rConverting {frame_quantity} frames from {video_file}...{round((len(unicode_art)* 1/((frame_quantity)/100)))}%')
        sys.stdout.flush()

    with open('data.js', 'w') as f:
        f.write('export default [')
        if len(unicode_art) > 0:
            for idx, u in enumerate(unicode_art):
                if (idx == ((len(unicode_art)) - 1)):
                    f.write('`\n' + u + '\n`];')
                else:
                    f.write('`\n' + u + '\n`,\n')
            sys.stdout.write(f'\rVideo converted successfully.                                              ')
            sys.stdout.write(f'\nObject output: ./data.js')
            sys.stdout.flush()
        else:
            sys.stdout.write(f'\Error converting video.')
            sys.stdout.flush()
