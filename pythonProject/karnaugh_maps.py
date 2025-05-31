import colorsys
import math
import random



class Group:
    def __init__(self, x1, y1, x2, y2, ones):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.ones = ones
        self.neighbors = []               #slouží pro reprezentaci překrývajících se skupin pomocí grafu
        self.color_index = -1
        self.color = 0
        #self.variables_values = dict()

    def __str__(self):
        return "["+str(self.x1)+", "+str(self.y1)+"] ["+str(self.x2)+", "+str(self.y2)+"]"

    def __eq__(self, other):
        return self.x1 == other.x1 and self.y1 == other.y1 and self.x2 == other.x2 and self.y2 == other.y2

    def __hash__(self):
        return hash((self.x1,self.y1,self.x2,self.y2))

    def get_size(self):
        return math.sqrt(len(self.ones))




def print_map(a, big_table):
    for i in range(0,len(a)):
        for j in range(0,len(a[0])):
            if big_table and len(a) / 3 <= i < 2 * len(a) / 3 and len(a[0]) / 3 <= j < 2 * len(a[0]) / 3:
                print(f"\033[92m{a[i][j]:4d}\033[97m",end="")
            else:
                print(f"{a[i][j]:4d}",end="")
        print("")
def expand_table(a):
    table=a.copy()
    table=table*3
    for i in range(0,len(table)):
        table[i]=table[i]*3
    return table
def get_num_of_variables():
    while True:
        try:
            x = int(input("Počet proměnných: "))
        except ValueError:
            print("Nesprávná hodnota")
            continue

        if not x in range(1,6):
            print("Nesprávná hodnota")
            continue
        return x
def get_values(y):
    i=0
    print("Vyplňte hodnoty pravdivostní funkce:")
    while True:
        if i == len(y):
            return
        try:
            value = int(input(str(i) + str(y[i]) + " "))
        except ValueError:
            print("Nesprávná hodnota")
            continue
        if not value in range(0,2):
            print("Nesprávná hodnota")
            continue


        y[i].append(value)
        i=i+1
    return




def get_values_from_array(y, values):
    for i in range(len(y)):
        y[i].append(values[i])
    return

#y=pole, které musíme překlopit
def symmetry_v(a, n_row, n_col):
    max_index= n_col * 2 - 1
    #koeficient, který se bude hodnotám přičítat (aby pole neobsahovalo 2x stejnou hodnotu)
    s=int(n_row * n_col)

    for i in range(0, n_row):
        for j in range(0, n_col):
            a[i][max_index-j]=a[i][j]+s
def symmetry_h(a, n_row, n_col):
    max_index= n_row * 2 - 1
    s=int(n_row * n_col)

    for i in range(0, n_row):
        for j in range(0, n_col):
            a[max_index-i][j]=a[i][j]+s

def get_proportions(n):
    n_col = math.ceil(n/2)
    n_row = math.floor(n/2)
    return n_col, n_row

def generate_table_rec(n, x, y, i):
    if i == n:
        y.append(x.copy())
        return
    x[i]=0
    generate_table_rec(n, x, y, i + 1)
    x[i]=1
    generate_table_rec(n, x, y, i + 1)

#n = počet proměnných
#y = pole, do kterého se hodnoty vepíšou
def generate_table(n, y):
    x = [0]*n
    generate_table_rec(n, x, y, 0)
#start_x = 0 pokud je sudý počet proměnných, jinak start_x = 1 (a naopak pro start_y)
def generate_axes(y, start_x, start_y):
    x_axis=[]
    y_axis=[]
    for line in y:
        x = 0
        y = 0
        for i in range(start_x, len(line), 2):
            x += line[i]
        for i in range(start_y, len(line), 2):
            y += line[i]
        if x == 0:
            x_axis.append(line)
        if y == 0:
            y_axis.append(line)

    return x_axis, y_axis


def generate_map(n, y):
    n_col = 2**math.ceil(n/2)
    n_row = 2**math.floor(n/2)

    a=[]
    for i in range(0,n_row):
        a.append([-1]*n_col)
    a[0][0]=0
    a[0][1]=1
    i=0
    j=1
    while i+j < n:
        if i==j:
            symmetry_v(a, 2 ** i, 2 ** j)
            j=j+1
        else:
            symmetry_h(a, 2 ** i, 2 ** j)
            i=i+1
    x_axis=[]
    y_axis=[]
    for i in range(0,n_row):
        for j in range(0,n_col):
            if i == 0:
                x_axis.append(y[a[0][j]][:-1])
            if j == 0:
                y_axis.append(y[a[i][0]][:-1])

            a[i][j]=y[a[i][j]][n]
    return a, x_axis, y_axis

def find_all_ones(karnaugh_map):
    all_ones = []
    for i in range(0,len(karnaugh_map)):
        for j in range(0,len(karnaugh_map[0])):
            if karnaugh_map[i][j] == 1:
                all_ones.append((i,j))
    return all_ones


def merge_groups(group_1, group_2):
    return Group(group_1.x1, group_1.y1, group_2.x2, group_2.y2, group_1.ones+group_2.ones)

def is_between(point_1, point_2, point):
    return point_1[0] <= point[0] <= point_2[0] and point_1[1] <= point[1] <= point_2[1]


def are_overlapping_groups(group_1, group_2):
    for one_1 in group_1.ones:
        for one_2 in group_2.ones:
            if  one_1 == one_2:
                return True
    return False
def are_neighbor_groups(group_1, group_2, n_row, n_col):
    if group_1.get_size() != group_2.get_size():
        return 0, 0
    if are_overlapping_groups(group_1, group_2) and group_1 != group_2:
        return 0, 0

    result = 0
    changed = 0
    #vedle sebe
    if group_1.x1 == group_2.x1 and group_1.x2 == group_2.x2:
        if group_1.y2 == group_2.y1 - 1 or group_1.y2 == group_2.y1 + n_col - 1:
            result = 1
            changed += 1

        elif group_2.y2 == group_1.y1 - 1 or group_2.y2 == group_1.y1 + n_col - 1:
            result = 2

    #pod sebou
    if group_1.y1 == group_2.y1 and group_1.y2 == group_2.y2:
        if group_1.x2 == group_2.x1 - 1 or group_1.x2 == group_2.x1 + n_row - 1:
            result = 3
            changed += 1

        elif group_2.x2 == group_1.x1 - 1 or group_2.x2 == group_1.x1 + n_row - 1:
            result = 4

    return result, changed


def remove_useless_groups_first_step(all_ones, all_groups):
    one_in_group = [False]*len(all_ones)

    useful_groups = set()
#skupiny musíme prohledávat od největší
    for i in range(len(all_groups)-1, -1,-1):
        for j in range(len(all_groups[i])):
            for one in all_ones:
                if one in all_groups[i][j].ones:
                    if not one_in_group[all_ones.index(one)]:
                        one_in_group[all_ones.index(one)] = True
                        useful_groups.add(all_groups[i][j])

            if False not in one_in_group:
                return list(useful_groups)
    return []
def remove_useless_groups_second_step(all_groups):
    all_groups_copy = all_groups.copy()
    for group_x in all_groups_copy:
        useless = True
        for one in group_x.ones:
            is_in_group = False
            for group_y in all_groups:
                if group_x == group_y:
                    continue
                if one in group_y.ones:
                    is_in_group = True

            if not is_in_group:
                useless = False
                break

        if useless:
            all_groups.remove(group_x)
def remove_useless_groups(all_ones, all_groups):
    all_groups = remove_useless_groups_first_step(all_ones, all_groups)
    remove_useless_groups_second_step(all_groups)
    return all_groups

def shift_group_to_look_better(group_x, n_row, n_col):
    neighbor_groups, changed = are_neighbor_groups(group_x, group_x, n_row, n_col)
    #smyčka je přes celou mapu
    if changed == 2:
        group_x.x1 = 0
        group_x.y1 = 0
        group_x.x2 = n_row - 1
        group_x.y2 = n_col - 1
    elif neighbor_groups == 1 or neighbor_groups == 2:
        group_x.y1 = 0
        group_x.y2 = n_col - 1
    elif neighbor_groups == 3 or neighbor_groups == 4:
        group_x.x1 = 0
        group_x.x2 = n_row - 1
    return group_x

def find_best_groups(karnaugh_map):
    all_ones = find_all_ones(karnaugh_map)
    all_groups = []
    n_row = len(karnaugh_map)
    n_col = len(karnaugh_map[0])

    # všechny jedničky tvoří minimální smyčku velikosti 1 (ty nevznikají skládáním)
    new_groups = set()
    for one in all_ones:
        new_groups.add(Group(one[0], one[1], one[0], one[1], [one]))
    all_groups.append(list(new_groups))

    line_index=1
    while True:
        new_groups = set()
        for i in range(0, len(all_groups[line_index - 1])):
            for j in range(i + 1, len(all_groups[line_index - 1])):
                group_1 = all_groups[line_index - 1][i]
                group_2 = all_groups[line_index - 1][j]

                neighbor_groups = are_neighbor_groups(group_1, group_2, len(karnaugh_map), len(karnaugh_map[0]))[0]

                if neighbor_groups == 1 or neighbor_groups == 3:
                    new_groups.add(shift_group_to_look_better(merge_groups(group_1, group_2), n_row, n_col))

                elif neighbor_groups == 2 or neighbor_groups == 4:
                    new_groups.add(shift_group_to_look_better(merge_groups(group_2, group_1), n_row, n_col))

        if len(new_groups) == 0:
            break
        all_groups.append(list(new_groups))
        line_index+=1

    all_groups = remove_useless_groups(all_ones, all_groups)
    return all_groups

def groups_to_graph(groups, all_ones):
    for one in all_ones:
        overlapping = []
        for group_x in groups:
            if one in group_x.ones:
                overlapping.append(group_x)

        for group_x in overlapping:
            group_x.neighbors += overlapping.copy()
            group_x.neighbors.remove(group_x)
def go_trough_graph(groups):
    for group_x in groups:
        if group_x.color_index != -1:
            continue

        queue = [group_x]
        groups_cluster = [group_x]
        n_colors = 0
        while len(queue) > 0:
            group_current = queue.pop(0)
            for group_next in group_current.neighbors:
                if group_next.color_index == -1:
                    group_next.color_index = 0
                    queue.append(group_next)
                    groups_cluster.append(group_next)

            neighbor_colors = []
            for n_g in group_current.neighbors:
                neighbor_colors.append(n_g.color_index)

            color_index = 1
            while True:
                if color_index not in neighbor_colors:
                    group_current.color_index = color_index
                    if n_colors < color_index:
                        n_colors = color_index
                    break
                color_index += 1
        distribute_colors(groups_cluster, n_colors)
def distribute_colors(groups_cluster, n_colors):
    try:
        hue =   1 / n_colors / 2
    except ZeroDivisionError:
        return
    saturation = 1
    value = 1

    for group_x in groups_cluster:
        group_x.color = colorsys.hsv_to_rgb(group_x.color_index * hue, saturation, value)
        group_x.color = tuple([256 * x for x in group_x.color])
        group_x.color = tuple(map(int, group_x.color))

def new_colors(groups):
    try:
        hue =   1 / len(groups)
    except ZeroDivisionError:
        return
    saturation = 1
    value = 1

    for i in range(len(groups)):
        groups[i].color = colorsys.hsv_to_rgb(i * hue, saturation, value)
        groups[i].color = tuple([256 * x for x in groups[i].color])
        groups[i].color = tuple(map(int, groups[i].color))

def get_colors(karnaugh_map, groups):
    new_colors(groups)

    original_colors = {}

    i = len(groups)-1
    while i >= 0:
        original_colors[groups[i]] = groups[i].color
        i-=1

    colors = {}
    for group_x in groups:
        for one in group_x.ones:
            if one in colors.keys():
                colors[one].append(group_x.color)
            else:
                colors[one] = [group_x.color]


    for one in colors.keys():
        r = g = b = 0
        c = colors[one]
        for color in c:
            r += color[0]
            g += color[1]
            b += color[2]

        r /= len(c)
        g /= len(c)
        b /= len(c)
        colors[one] = (int(r), int(g), int(b))


    result = []
    for i in range(len(karnaugh_map)):
        result.append([])
        for j in range(len(karnaugh_map[i])):
            if karnaugh_map[i][j]==1:
                result[i].append(colors[(i, j)])
            else:
                result[i].append((256, 256 , 256))

    return original_colors, result


def get_colors_1(karnaugh_map, groups):
    all_ones = find_all_ones(karnaugh_map)

    original_colors = {}
    for group_x in groups:
        original_colors[group_x] = (random.randint(50, 186), random.randint(50, 156), random.randint(50, 256))

    colors = {}
    for one in all_ones:
        c = []
        for group_x in groups:
            if one in group_x.ones:
                c.append(original_colors[group_x])
        r = g = b = 0
        for color in c:
            r += color[0]
            g += color[1]
            b += color[2]
        r /= len(c)
        g /= len(c)
        b /= len(c)

        colors[one] = (int(r), int(g), int(b))

    result = []
    for i in range(len(karnaugh_map)):
        result.append([])
        for j in range(len(karnaugh_map[i])):
            if karnaugh_map[i][j]==1:
                result[i].append(('#%02X%02X%02X' % (colors[(i,j)])))
            else:
                result[i].append(('#%02X%02X%02X' % (256,256,256)))

    return original_colors, result


def get_minimized_expression(groups, x_axis, y_axis, variables):
    results = []
    for group_x in groups:
        values_for_variables = {v: -1 for v in range(len(variables))}

        for one in group_x.ones:
            x = one[0]
            y = one[1]
            for i in range(1, len(variables), 2):
                if values_for_variables[i] == -1:
                    values_for_variables[i] = y_axis[x][i]
                elif values_for_variables[i] != y_axis[x][i]:
                    values_for_variables[i] = 2

            for i in range(0, len(variables), 2):
                if values_for_variables[i] == -1:
                    values_for_variables[i] = x_axis[y][i]
                elif values_for_variables[i] != x_axis[y][i]:
                    values_for_variables[i] = 2


        result = ""
        for key in values_for_variables.keys():
            if values_for_variables[key] == 0:
                result += "!" + variables[key]
            elif values_for_variables[key] == 1:
                result += variables[key]
        results += result

        if group_x != groups[-1]:
            results += " + "

    return "".join(results)
