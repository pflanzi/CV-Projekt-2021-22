# ------ imports ------ #
import traceback
import PySimpleGUI as Sg
import io
from PIL import Image
import main
from main import DetectionAlgorithm as dA
import cv2

# for testing / configuration purposes => Sg.main()

# ------------ variables and GUI elements ----------- #
file_path = ''

# ------ theme ------ #
Sg.theme('Light Green')

# ------ drop down menu ------ #
menu_def = [
    ['&File', ['Open', '---', 'Close']],
    ['&Edit', ['Print Results']],
    ['&Extras', ['About']]
]

# ------ options ------ #

min_option = [
    [Sg.Text(key='-EXPAND5-', pad=0)],
    [Sg.Text('min radius')]
]

max_option = [
    [Sg.Text(key='-EXPAND6-', pad=0)],
    [Sg.Text('max radius')]
]

radii = [
    [Sg.Text('enclosing circles', font=('Ubuntu', 13, 'bold'), justification='c', expand_x=True, expand_y=True)],
    [Sg.Column(min_option),
     Sg.Text(key='-EXPAND7-', pad=5),
     Sg.Slider(key='min_r',
               range=(0, 1000),
               default_value=0,
               size=(20, 15),
               orientation='horizontal',
               enable_events=True)],
    [Sg.Column(max_option),
     Sg.Text(key='-EXPAND8-', pad=5),
     Sg.Slider(key='max_r',
               range=(0, 1000),
               default_value=0,
               size=(20, 15),
               orientation='horizontal',
               enable_events=True)]
]

options = [
    [Sg.Column(radii, pad=(10, 10))],
    [Sg.Text(key='-EXPAND3-', pad=0), Sg.Button('Count', key='count_button', pad=(10, 15)),
     Sg.Text(key='-EXPAND4-', pad=0)]
]

# ------ picture area ------ #
pic = [
    [Sg.Image('../images/Placeholder.svg', key='picture', pad=(5, (3, 10)))],
    [Sg.Text(' ', key='path', font=('Ubuntu', 11, 'italic'), text_color='#919191')],
    [
        Sg.Text('Counted objects: ', pad=(5, 25), font=('Ubuntu', 14, 'bold')),
        Sg.Text(' ', key='result', font=('Ubuntu', 14))
    ]
]

# ------ error message box ------ #
err_box = [
    [Sg.Multiline(key='err',
                  font=('Ubuntu', 10),
                  autoscroll=True,
                  size=(35, 30),
                  auto_refresh=True,
                  do_not_clear=True,
                  disabled=True)]
]

# ------ layout ------ #
layout = [
    [Sg.Menu(menu_def, font=('Ubuntu', 11), tearoff=True)],
    [Sg.Text(key='-EXPAND1-', pad=0)],
    [
        Sg.Frame(' Options ', options, vertical_alignment='t'),
        Sg.Column(pic, justification='c', pad=(100, 3), vertical_alignment='t'),
        Sg.Column(err_box, vertical_alignment='t')
    ],
    [Sg.Text(key='-EXPAND2-', pad=0)]

]

# ------ main ------ #
window = Sg.Window('Counting apples',
                   layout,
                   font=('Ubuntu', 12),
                   resizable=True,
                   finalize=True,
                   location=(0, 0))

# resizing the window to fullscreen without making the titlebar/toolbar disappear
width = window.TKroot.winfo_screenwidth() * 0.75
height = window.TKroot.winfo_screenheight() * 0.75
window.TKroot.geometry("%dx%d" % (width, height))

# expanding empty container elements to adjust element position
window['-EXPAND1-'].expand(True, True, True)        # image centering
window['-EXPAND2-'].expand(True, True, True)        # image centering
window['-EXPAND3-'].expand(True, True, False)       # count button centering
window['-EXPAND4-'].expand(True, True, False)       # count button centering
window['-EXPAND5-'].expand(True, True, False)
window['-EXPAND6-'].expand(True, True, False)
window['-EXPAND7-'].expand(True, True, True)
window['-EXPAND8-'].expand(True, True, True)

# event listener
while True:
    event, values = window.read()
    # print(event, values)

    print(int(values['min_r']))

    if event == 'Open':
        file_path = Sg.popup_get_file(' ', title='Please chose a file', no_window=True)

        # opening the image and converting it into a byte stream to display it inside the main window
        try:
            image = Image.open(file_path)
            image.thumbnail((500, 500))  # change max size of the displayed image, preserves aspect ratio
            bio = io.BytesIO()
            image.save(bio, format='PNG')

            window['picture'].update(data=bio.getvalue())
            window['path'].update(file_path)

        except AttributeError as ae:
            tb = traceback.format_exc()

            window['err'].update(window['err'].get() + 'No image has been selected.')

            print('\n***********************************\n')
            print('\nThis error may be ignored as it does not cause any serious issues.\n')
            print(f'Message: {ae}\n\n{tb}\n')
            print('\n***********************************\n')

    if event == 'count_button':
        program = dA()

        if file_path == '':
            window['err'].update(window['err'].get() + 'Please select a valid image.\n')
        else:
            min_rad = int(values['min_r'])
            max_rad = int(values['max_r'])

            if min_rad == 0 or max_rad == 0:
                window['err'].update(window['err'].get() + 'Radii must be >0.\n')

            elif min_rad >= max_rad:
                window['err'].update(window['err'].get() + 'Min radius can\'t be bigger than max radius.\n')

            else:
                result = program.main(file_path, min_rad, max_rad)  # type => numpy.ndarray

                img_bytes = cv2.imencode('.png', result)[1].tobytes()
                window['picture'].update(data=img_bytes)

    if event == Sg.WIN_CLOSED or event == 'Close':
        break

window.close()

# ***** TODO
# TODO: add an 'About' window
# TODO: add a 'Print Results' function or remove it
