from PIL import Image, ImageDraw, ImageFont


class MapImage:
    def __init__(self, karnaugh_map, variables, groups, colors, x_axis, y_axis):
        self.karnaugh_map = karnaugh_map
        self.groups = groups
        self.colors = colors
        self.variables = variables

        self.n_rows = len(karnaugh_map)
        self.n_cols = len(karnaugh_map[0])
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.gap = 0.2 + 1/(10*len(variables))
        


        self.img = Image.new("RGB", (1000*self.n_cols, 1000*self.n_rows), (255, 255, 255))
        self.img_draw = ImageDraw.Draw(self.img)
        self.img_width, self.img_height= self.img.size


        self.unit = (self.img_width * (1 - self.gap) - self.img_width * self.gap) / self.n_cols
        #self.font = ImageFont.truetype("static/styles/times.ttf", int(self.unit / 2))
        self.font = ImageFont.load_default(int(self.unit / 2))

        self.draw_grid()
        self.fill_grid()
        self.draw_groups()
        self.draw_coordinates()
        self.crop_image()

    def get_image(self):
        return self.img

    #vstup: souřadnice v tabulce (v mapě)
    #výstup: souřadnice v obrázku (kam se to má vykreslit)
    def get_coordinates_for_text(self, x, y):
        x_result = self.img_width * self.gap + y * self.unit + 0.35 * self.unit
        y_result = self.img_height * self.gap + x * self.unit + 0.2 * self.unit
        return x_result, y_result


    def draw_grid(self):
        self.img_draw.rectangle(((self.img_width * self.gap, self.img_height * self.gap),
                                (self.img_width  * (1 - self.gap), self.img_height   * (1 - self.gap))),
                                outline=(0, 0, 0), width=10)

        #podélné čáry
        for i in range(1, self.n_rows):
            self.img_draw.line(
                ((self.img_width * self.gap, self.img_height * self.gap + i * self.unit),
                (self.img_width * (1 - self.gap), self.img_height * self.gap + i * self.unit)),
                fill=(0, 0, 0), width=10)
        #svislé čáry
        for i in range(1, self.n_cols):
            self.img_draw.line(
                ((self.img_width * self.gap + i * self.unit, self.img_height * self.gap),
                 (self.img_width * self.gap + i * self.unit, self.img_height * (1 - self.gap))),
                fill=(0, 0, 0), width=10)
    def fill_grid(self):

        for x in range(0, self.n_rows):
            for y in range(0, self.n_cols):
                self.img_draw.text((self.get_coordinates_for_text(x, y)),
                                   text=str(self.karnaugh_map[x][y]), fill=(0, 0, 0),
                                   font = self.font, align="left", padding=0)
                """
                self.img_draw.text((self.get_coordinates_for_text(x, y)),
                                   text=str(self.karnaugh_map[x][y]), fill=(0, 0, 0),
                                   font=ImageFont.load_default(int(self.unit / 2)), align="left", padding=0)
                """


    def draw_groups(self):
        #self.gap = self.gap * 1.1
        mini = 25

        start_point_width = self.img_width * self.gap
        start_point_height = self.img_height * self.gap


        for group in self.groups:

            top_left_point_x = start_point_width + group.y1 * self.unit + mini
            top_left_point_y = start_point_height + group.x1 * self.unit + mini
            down_right_point_x = start_point_width + (group.y2 + 1) * self.unit - mini
            down_right_point_y = start_point_height + (group.x2 + 1) * self.unit - mini

            if group.x1 <= group.x2 and group.y1 <= group.y2:
                self.img_draw.rounded_rectangle(
                    ((top_left_point_x, top_left_point_y), (down_right_point_x, down_right_point_y)),
                        radius=400, outline=self.colors[group], width=30)

            elif group.x1 <= group.x2 and group.y1 > group.y2:
                self.img_draw.rounded_rectangle(
                    ((top_left_point_x, top_left_point_y), (self.img_width * (1 - self.gap) + self.unit, down_right_point_y)),
                        radius=400, outline=self.colors[group], width=30)

                self.img_draw.rounded_rectangle(
                    ((start_point_width - self.unit, top_left_point_y), (down_right_point_x, down_right_point_y)),
                        radius=400, outline=self.colors[group], width=30)

            elif group.x1 > group.x2 and group.y1 <= group.y2:
                self.img_draw.rounded_rectangle(
                    ((top_left_point_x, top_left_point_y), (down_right_point_x, self.img_height * (1 - self.gap) + self.unit)),
                        radius=400, outline=self.colors[group], width=30)

                self.img_draw.rounded_rectangle(
                    ((top_left_point_x, start_point_height - self.unit), (down_right_point_x, down_right_point_y)),
                        radius=400, outline=self.colors[group], width=30)

            elif group.x1 > group.x2 and group.y1 > group.y2:
                self.img_draw.rounded_rectangle(
                    ((top_left_point_x, top_left_point_y),
                        (self.img_width * (1 - self.gap) + self.unit, self.img_height * (1 - self.gap) + self.unit)),
                        radius=400, outline=self.colors[group], width=30)

                self.img_draw.rounded_rectangle(
                    ((start_point_width - self.unit, start_point_height - self.unit), (down_right_point_x, down_right_point_y)),
                        radius=400, outline=self.colors[group], width=30)

                self.img_draw.rounded_rectangle(
                    ((top_left_point_x, start_point_height - self.unit),
                        (self.img_width * (1 - self.gap) + self.unit, down_right_point_y)),
                        radius=400, outline=self.colors[group], width=30)

                self.img_draw.rounded_rectangle(
                    ((start_point_width - self.unit, top_left_point_y),
                        (down_right_point_x, self.img_height * (1 - self.gap) + self.unit)),
                        radius=400, outline=self.colors[group], width=20)

    def draw_frame(self):
        self.img_draw.rectangle(((0,0), (self.img_width, self.img_height*self.gap)),fill="white")
        self.img_draw.rectangle(((0,self.img_height*(1-self.gap)), (self.img_width, self.img_height)),fill="white")
        self.img_draw.rectangle(((0,0), (self.img_width*self.gap, self.img_height)),fill="white")
        self.img_draw.rectangle(((self.img_width*(1-self.gap),0), (self.img_width, self.img_height)),fill="white")

    def draw_coordinates_up(self, i, distances_from_table):
        for j in range(len(self.x_axis)):
            if self.x_axis[j][i] == 1:
                self.img_draw.line(
                    ((self.img_width * self.gap + self.unit * j, self.img_height * self.gap - distances_from_table[i]),
                     (self.img_width * self.gap + self.unit * (j + 1),
                      self.img_height * self.gap - distances_from_table[i])),
                    fill="black", width=10)
                summary = 0
                for k in range(len(self.variables)):
                    summary += self.x_axis[j][k]
                if summary == 1:
                    self.img_draw.text((self.img_width * self.gap + self.unit * j + self.unit / 3,
                                        self.img_height * self.gap - distances_from_table[i] - self.unit * 0.6),
                                       font=self.font, text=self.variables[i],
                                       fill="black")
    def draw_coordinates_left(self, i, distances_from_table):
        for j in range(len(self.y_axis)):
            if self.y_axis[j][i] == 1:
                self.img_draw.line(
                    ((self.img_width * self.gap - distances_from_table[i], self.img_height * self.gap + self.unit * j),
                     (self.img_width * self.gap - distances_from_table[i],
                      self.img_height * self.gap + self.unit * (j + 1))),
                    fill="black", width=10)
                summary = 0
                for k in range(len(self.variables)):
                    summary += self.x_axis[j][k]
                if summary == 1:
                    self.img_draw.text((self.img_width * self.gap - distances_from_table[i] - self.unit * 0.5,
                                        self.img_height * self.gap + self.unit * j + self.unit * 0.2),
                                       font=self.font, text=self.variables[i],
                                       fill="black")
    def draw_coordinates_down(self, i, distances_from_table):
        for j in range(len(self.x_axis)):
            if self.x_axis[j][i] == 1:
                self.img_draw.line(((self.img_width * self.gap + self.unit * j,
                                     self.img_height * (1 - self.gap) + distances_from_table[i]),
                                    (self.img_width * self.gap + self.unit * (j + 1),
                                     self.img_height * (1 - self.gap) + distances_from_table[i])),
                                   fill="black", width=10)
                summary = 0
                for k in range(len(self.variables)):
                    summary += self.x_axis[j][k]
                if summary == 1:
                    self.img_draw.text((self.img_width * self.gap + self.unit * j + self.unit / 2.5,
                                        self.img_height * (1 - self.gap) + distances_from_table[i] + self.unit * 0.1),
                                       font=self.font, text=self.variables[i],
                                       fill="black")
    def draw_coordinates_right(self, i, distances_from_table):
        for j in range(len(self.y_axis)):
            if self.y_axis[j][i] == 1:
                self.img_draw.line(((self.img_width * (1 - self.gap) + distances_from_table[i],
                                     self.img_height * self.gap + self.unit * j),
                                    (self.img_width * (1 - self.gap) + distances_from_table[i],
                                     self.img_height * self.gap + self.unit * (j + 1))),
                                   fill="black", width=10)
                summary = 0
                for k in range(len(self.variables)):
                    summary += self.x_axis[j][k]
                if summary == 1:
                    self.img_draw.text((self.img_width * (1 - self.gap) + distances_from_table[i] + self.unit * 0.07,
                                        self.img_height * self.gap + self.unit * j + self.unit * 0.2),
                                       font=self.font, text=self.variables[i],
                                       fill="black")
        
    def draw_coordinates(self):
        self.draw_frame()
        unit_distance = 100

        distances_from_table = []
        for j in range(len(self.variables)):
            distances_from_table.append(unit_distance * (int(j / 4) + 1))

        i = 0
        while i < len(self.variables):
            self.draw_coordinates_up(i, distances_from_table)
            i += 1
            if i >= len(self.variables):
                break
            self.draw_coordinates_left(i, distances_from_table)
            i += 1
            if i >= len(self.variables):
                break
            self.draw_coordinates_down(i, distances_from_table)
            i += 1
            if i >= len(self.variables):
                break
            self.draw_coordinates_right(i, distances_from_table)
            i += 1

    def crop_image(self):
        if len(self.variables) % 2 == 1:
            self.img = self.img.crop((int(0.12*self.img_width), 0,int(0.87*self.img_width), int(self.img_height)))

