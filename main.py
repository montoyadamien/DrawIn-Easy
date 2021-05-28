import colors
import requests
from PIL import Image
from pynput.mouse import Controller, Button
from pynput import mouse
import time
from screeninfo import get_monitors

mouse_controller = Controller()

NO_STATE = None
FIRST_POINT_STATE = 1
SECOND_POINT_STATE = 2

PEN_RADIUS = 3

resolutions = [
    '2560x1440'
]


class DrawInEasy:
    currentState = NO_STATE
    screen_resolution = None

    firstPicCoordinates = None
    secondPicCoordinates = None

    base_picture = None
    points_to_draw = None
    width = None
    height = None

    def __init__(self):
        self.enter_resolution()

    def enter_resolution(self):
        main_monitor = get_monitors()[0]
        self.screen_resolution = str(main_monitor.width) + 'x' + str(main_monitor.height)
        print('-> Getting your main screen resolution -', self.screen_resolution)
        if self.screen_resolution not in resolutions:
            exit('Error -> your screen resolution must be in ' + str(resolutions))
        else:
            while 1:
                self.load_picture()

    def is_url_image(self, image_url):
        try:
            image_formats = ('image/png', 'image/jpeg', 'image/jpg')
            r = requests.head(image_url)
            if r.headers['content-type'] in image_formats:
                return True
            return False
        except:
            return False

    def on_click(self, x, y, button, pressed):
        if pressed:
            print(x, y)
            if self.currentState == FIRST_POINT_STATE:
                self.firstPicCoordinates = (x, y)
            elif self.currentState == SECOND_POINT_STATE:
                self.secondPicCoordinates = (x, y)
        if not pressed:
            return False

    def reset_state(self):
        self.currentState = NO_STATE
        self.firstPicCoordinates = None
        self.secondPicCoordinates = None
        self.base_picture = None
        self.points_to_draw = None
        self.width = None
        self.height = None

    def load_picture(self):
        self.reset_state()
        print('-> Enter the picture URL - [.png, .jpg, .jpeg]')
        picture_link = input()
        if self.is_url_image(picture_link):
            self.base_picture = Image.open(requests.get(picture_link, stream=True).raw)
            print('-> Choose in Gartic Phone workplan the first point to start drawing (top left corner of the picture)')
            self.currentState = FIRST_POINT_STATE
            with mouse.Listener(on_click=self.on_click) as listener:
                listener.join()
            print('-> Choose in Gartic Phone workplan the second point to end drawing (bottom right corner of the picture)')
            self.currentState = SECOND_POINT_STATE
            with mouse.Listener(on_click=self.on_click) as listener:
                listener.join()
            if self.firstPicCoordinates[0] >= self.secondPicCoordinates[0]:
                print('Error ->  x1 must be < x2')
            elif self.firstPicCoordinates[1] >= self.secondPicCoordinates[1]:
                print('Error -> y1 must be < y2')
            else:
                self.pre_draw_picture()
        else:
            print('Error -> only png, jpeg and jpg are allowed')

    def is_picture_contains_transparency(self):
        return self.base_picture.mode in ('RGBA', 'LA') \
               or (self.base_picture.mode == 'P' and 'transparency' in self.base_picture.info)

    def pre_draw_picture(self):
        print('Making calculations with your picture, please wait...')
        if not self.is_picture_contains_transparency():  # force the type to be rgba and using a 3pixel-alpha tuple
            self.base_picture = self.base_picture.convert('RGBA')
        width = self.secondPicCoordinates[0] - self.firstPicCoordinates[0]
        height = self.secondPicCoordinates[1] - self.firstPicCoordinates[1]
        self.base_picture.thumbnail((width, height), Image.ANTIALIAS)
        self.width, self.height = self.base_picture.size
        for x in range(0, self.width):
            for y in range(0, self.height):
                r, g, b, a = self.base_picture.getpixel((x, y))
                closest_color = list(colors.closest((r, g, b, 255)))
                closest_color[3] = a
                self.base_picture.putpixel((x, y), tuple(closest_color))
        horizontal_clicks, horizontal_coords_to_draw = self.calculate_number_click_to_draw_lines(True)
        vertical_clicks, vertical_coords_to_draw = self.calculate_number_click_to_draw_lines(False)
        if horizontal_clicks <= vertical_clicks:
            print('Drawing horizontal lines will be faster')
            self.draw_lines(horizontal_coords_to_draw)
        else:
            print('Drawing vertical lines will be faster')
            self.draw_lines(vertical_coords_to_draw)

    def extract_number_lines_and_lines_to_draw(self, array_with_coords, number_lines, total_points, is_horizontal):
        final_colors = []  # type: list[tuple]
        white_coords = colors.get_location_white_color(self.screen_resolution)
        white_values = None
        if white_coords in array_with_coords:
            white_values = (white_coords, array_with_coords[white_coords])
            del array_with_coords[white_coords]

        for key in array_with_coords:
            points_for_color = 0
            coords = array_with_coords[key]  # type: list
            coords_len = len(coords)
            for i in range(0, coords_len):
                coords1 = coords[i][0]  # type: tuple
                coords2 = coords[i][1]  # type: tuple
                if is_horizontal:
                    points_for_color += coords2[0] - coords1[0]
                else:
                    points_for_color += coords2[1] - coords1[1]
            # if the color takes less than 0.5% of the drawing, do not draw these points
            if (points_for_color / total_points) * 100 < 0.5:
                number_lines -= coords_len
            else:
                final_colors.append((key, array_with_coords[key]))
        # draw the white lines at the end
        if white_values is not None:
            final_colors.append(white_values)
        return number_lines, final_colors

    def calculate_number_click_to_draw_lines(self, is_horizontal):
        number_lines = 0
        total_points = 0
        array_with_coords = {}
        if is_horizontal:
            i_increment = self.height
            j_increment = self.width
        else:
            i_increment = self.width
            j_increment = self.height
        for i in range(0, i_increment, PEN_RADIUS):
            last_color = None
            previous_j = 0
            for j in range(0, j_increment, PEN_RADIUS):
                if is_horizontal:
                    rgb = self.base_picture.getpixel((j, i))
                else:
                    rgb = self.base_picture.getpixel((i, j))
                if j == 0:
                    if rgb[3] >= 128:  # only draw pixel with more than 50% opacity
                        last_color = rgb
                    else:
                        last_color = -1
                elif rgb != last_color or j >= j_increment - PEN_RADIUS:
                    if last_color != -1 and rgb[:3] != last_color[:3]:
                        number_lines += 1
                        final_color = list(last_color)
                        final_color[3] = 255
                        color_index = colors.gartic_colors.index(tuple(final_color))
                        color_location_click = colors.gartic_colors_location[color_index][self.screen_resolution]
                        if color_location_click not in array_with_coords:
                            array_with_coords[color_location_click] = []  # type: list
                        if is_horizontal:
                            final_i = i + self.firstPicCoordinates[1]
                            final_previous_j = previous_j + self.firstPicCoordinates[0]
                            final_j_to_move = j + self.firstPicCoordinates[0]
                            array_with_coords[color_location_click].append([(final_previous_j, final_i), (final_j_to_move, final_i)])
                        else:
                            final_i = i + self.firstPicCoordinates[0]
                            final_previous_j = previous_j + self.firstPicCoordinates[1]
                            final_j_to_move = j + self.firstPicCoordinates[1]
                            array_with_coords[color_location_click].append([(final_i, final_previous_j), (final_i, final_j_to_move)])
                        total_points += final_j_to_move - final_previous_j
                    previous_j = j
                    if rgb[3] >= 128:
                        last_color = rgb
                    else:
                        last_color = -1
        return self.extract_number_lines_and_lines_to_draw(array_with_coords, number_lines, total_points, is_horizontal)

    def draw_lines(self, array_with_coords):
        for location_click in array_with_coords:
            print('Drawing the color', location_click[0], '...')
            mouse_controller.position = location_click[0]
            mouse_controller.press(Button.left)
            mouse_controller.release(Button.left)
            lines = location_click[1]
            for locations in lines:
                loc1 = locations[0]
                loc2 = locations[1]
                y_move = loc2[1] - loc1[1]
                x_move = loc2[0] - loc1[0]
                mouse_controller.position = loc1
                mouse_controller.press(Button.left)
                time.sleep(0.002)
                mouse_controller.move(x_move, y_move)
                time.sleep(0.002)
                mouse_controller.release(Button.left)

if __name__ == '__main__':
    DrawInEasy().__init__()
