# ------ imports ------ #
import traceback
import PySimpleGUI as Psg
import io
from PIL import Image

# for testing / configuration purposes => sg.main()

# ------ theme ------ #
Psg.theme('Light Green')

# ------ menu ------ #
menu_def = [
    ['&File', ['Open', '---', 'Close']],
    ['&Edit', ['Print Results']],
    ['&Extras', ['About']]
]

# ------ options ------ #
thresh = [
    [Psg.Text('Threshold')],
    [Psg.Slider(key='Threshold',
                range=(0, 255),
                default_value=0,
                size=(20, 15),
                orientation='horizontal')]
]

options = [
    [Psg.Column(thresh, pad=(10, 10))],
    [Psg.Text(key='-EXPAND3-', pad=0), Psg.Button('Count', key='count_button', pad=(10, 15)),
     Psg.Text(key='-EXPAND4-', pad=0)]
]

# ------ picture area ------ #
pic = [
    [Psg.Image(r'/home/franzi/CV Projekt 2021/pictures/test/Placeholder.svg', key='picture', pad=(5, (3, 10)))],
    [Psg.Text(' ', key='path', font=('Ubuntu', 11, 'italic'), text_color='#919191')],
    [
        Psg.Text('Counted objects: ', pad=(5, 25), font=('Ubuntu', 14, 'bold italic')),
        Psg.Text(' ', key='result', font=('Ubuntu', 14))
    ]
]

# ------ error message box ------ #


err_box = [
    [Psg.Multiline(key='err',
                   font=('Ubuntu', 10),
                   autoscroll=True,
                   size=(35, 25),
                   auto_refresh=True,
                   do_not_clear=True,
                   disabled=True)]
]

# ------ layout ------ #
layout = [
    [Psg.Menu(menu_def, font=('Ubuntu', 11), tearoff=True)],
    [Psg.Text(key='-EXPAND1-', pad=0)],  # no functionality, simply used to center certain elements
    [
        Psg.Frame(' Options ', options, vertical_alignment='t'),
        Psg.Column(pic, justification='c', pad=(100, 3), vertical_alignment='t'),
        Psg.Column(err_box, vertical_alignment='t')
    ],
    [Psg.Text(key='-EXPAND2-', pad=0)]  # no functionality, simply used to center certain elements

]

# ------ main ------ #
window = Psg.Window('Analyzing pictures and counting objects',
                    layout,
                    font=('Ubuntu', 12),
                    resizable=True,
                    finalize=True,
                    location=(0, 0))

# resizing the window to fullscreen without making the titlebar/toolbar disappear
width = window.TKroot.winfo_screenwidth()
height = window.TKroot.winfo_screenheight()
window.TKroot.geometry("%dx%d" % (width, height))

# expanding empty container elements to adjust element position
window['-EXPAND1-'].expand(True, True, True)
window['-EXPAND2-'].expand(True, True, True)
window['-EXPAND3-'].expand(True, True, False)
window['-EXPAND4-'].expand(True, True, False)

while True:
    event, values = window.read()
    print(event, values)

    if event == 'Open':
        file_path = Psg.popup_get_file(' ', title='Please chose a file', no_window=True)

        # opening the image and converting it into a byte stream to display it inside the main window
        try:
            image = Image.open(file_path)
            image.thumbnail((800, 800))
            bio = io.BytesIO()
            image.save(bio, format='PNG')

            window['picture'].update(data=bio.getvalue())
            window['path'].update(file_path)

        except AttributeError as ae:
            tb = traceback.format_exc()

            window['err'].update(window['err'].get() + 'No image has been selected.')

            print(
                '\n*********** THIS ERROR MAY BE IGNORED AS IT IS NOT FATAL OR DOES NOT CAUSE THE PROGRAM TO CRASH. ***********\n')
            print(f'Message: {ae}\n\n{tb}')
            print(
                '************************************************************************************************************\n')
            pass

    if event == Psg.WIN_CLOSED or event == 'Close':
        break

window.close()

# TODO
# TODO: add an 'About' window
# TODO: add a 'Print Results' function
