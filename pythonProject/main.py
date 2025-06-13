from flask import Flask, render_template, request
import karnaugh_maps as km
import images


app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def first_page():
    return render_template('first_page.html')
@app.route('/zadani_tabulkou', methods=['GET', 'POST'])
def table_input():
    return render_template('table_input.html')
@app.route('/zadani_vyrazem', methods=['GET', 'POST'])
def expression_input():
    return render_template('expression_input.html', errorText = "", prefill_value="")


@app.route('/zadani_tabulkou/vyplnit_tabulku', methods=['GET', 'POST'])
def table_input_fill_table():
    if [request.method == 'POST']:
        n = int(request.form.get('n'))
        prefill_values = [0]*(2**n)

    y = []
    alph = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M"]

    km.generate_table(n, y)
    return render_template('table_input_fill_table.html', n=n, y=y, values=[],
                           alph=alph, prefill_values=prefill_values, errorText = "")

def sort_variables(expression_part):
    sorted_variables = {}
    variables = []
    i = 0
    for variable in expression_part:
        if variable != '!':
            sorted_variables[variable] = i
            variables.append(variable)
            i += 1

    return sorted_variables, variables

def values_from_expression(request):
    expression=request.form.get('expression')
    error = False
    if expression == '':
        error = True
    y = []
    expression_parts = str(expression).replace(" ", "").split('+')
    expression_parts = list(dict.fromkeys(expression_parts)) #odstranění duplicit

    sorted_variables, variables = sort_variables(expression_parts[0])

    n = len(variables)
    km.generate_table(n, y)


    for e in expression_parts:
        if len(e.replace('!','')) != n:
            error = 2
        for part in e.replace('!',''):
            if part not in sorted_variables:
                error = 2
        for part in sorted_variables:
            if part not in e.replace('!',''):
                error = 2
        if list(e.replace('!', '')) != list(dict.fromkeys(e.replace('!', ''))):
            error = 4


    values = [0] * (2 ** n)
    for e in expression_parts:
        value = [0] * n
        i = 0
        while i < len(e):
            if e[i] == '!':
                try:
                    value[sorted_variables[e[i + 1]]] = 0
                except KeyError:
                    if e[i+1] == "!":
                        error = 5
                    else:
                        error = 2
                except IndexError:
                    error = 6
                i += 2
            elif e[i].isalpha():
                try:
                    value[sorted_variables[e[i]]] = 1
                except KeyError:
                    error = 2
                except IndexError:
                    error = 6
                i += 1
            else:
                error = 3
                i+=1

        values[y.index(value)] = 1

    return values, n, y, variables, error


def values_from_table(request_arg):
    y = []
    values = []
    i = 0
    n = int(request_arg.args.get('n'))
    value = str(request_arg.form.get(str(i)))

    error = 0
    while value != 'None':
        if not value:
            values.append('')
            error = 1
        else:
            values.append(int(value))

        i += 1
        value = str(request_arg.form.get(str(i)))

    km.generate_table(n, y)
    return values, n, y, error

def values_from_map(request_arg):
    variables = request_arg.form.get('variables').replace(' ', '').replace('[', '').replace(']','').replace('\'','').split(',')
    x_axis_list = request_arg.form.get('x_axis').replace(' ', '').replace('\'','').split('],[')
    y_axis_list = request_arg.form.get('y_axis').replace(' ', '').replace('\'','').split('],[')
    x_axis = []
    y_axis = []
    for i in range(len(x_axis_list)):
        x_axis.append(x_axis_list[i].replace('[', '').replace(']', '').split(','))
        for j in range(len(x_axis[i])):
            x_axis[i][j] = int(x_axis[i][j])

    for i in range(len(y_axis_list)):
        y_axis.append(y_axis_list[i].replace('[', '').replace(']', '').split(','))
        for j in range(len(y_axis[i])):
            y_axis[i][j] = int(y_axis[i][j])


    n = int(request_arg.args.get('n'))
    karnaugh_map_local = []
    last_i = 0
    y = []
    km.generate_table(n, y)
    for key in request_arg.form.keys():
        if key != 'send' and key!='variables' and key!='x_axis' and key!='y_axis':
            i, j = key.split('_')
            if i != last_i:
                last_i = i
                karnaugh_map_local.append([])
            karnaugh_map_local[int(i)].append(int(request_arg.form.get(key)))


    return karnaugh_map_local, n, x_axis, y_axis, variables





@app.route('/zadani_tabulkou/vyplnit_tabulku/karnaughova_mapa', methods=['GET', 'POST'])
@app.route('/zadani_vyrazem/karnaughova_mapa', methods=['GET', 'POST'])
@app.route('/zadani_mapou/karnaughova_mapa', methods=['GET', 'POST'])
def karnaugh_map_result():
    alph = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M"]
    if [request.method == 'POST']:
        if 'zadani_vyrazem' in request.url:
            values, n, y, variables, error = values_from_expression(request)

            if error == 1:
                return render_template('expression_input.html', errorText = "Výraz musí obsahovat alespoň jednu proměnnou.", prefill_value = "")
            if error == 2:
                return render_template('expression_input.html', errorText = "Výraz musí v každém členu obsahovat všechny proměnné.", prefill_value = request.form.get('expression'))
            if error == 3:
                return render_template('expression_input.html', errorText = "Proměnné musí být označeny znaky z abecedy, ne speciálními znaky.", prefill_value = request.form.get('expression'))
            if error == 4:
                return render_template('expression_input.html', errorText = "V některém sčítanci se vyskytuje vícekrát stejná proměnná.", prefill_value = request.form.get('expression'))
            if error == 5:
                return render_template('expression_input.html', errorText = 'Ve výrazu se nemůže objevit dvakrát znegovaná proměnná (dva symboly "!" za sebou).', prefill_value = request.form.get('expression'))
            if error == 6:
                return render_template('expression_input.html', errorText = "Chybný vstup.", prefill_value = request.form.get('expression'))


        elif 'zadani_mapou' in request.url:
            karnaugh_map, n, x_axis, y_axis, variables = values_from_map(request)
        else:
            values, n, y, error = values_from_table(request)
            variables = alph[:n]

            if error:
                return (render_template('table_input_fill_table.html', n=n, y=y,
                                       alph=alph, prefill_values=values, errorText ="Vyplňte prosím všechna pole."))

    if not 'zadani_mapou' in request.url:
        for i in range(len(y)):
            y[i].append(values[i])

        karnaugh_map, x_axis, y_axis = km.generate_map(n, y)

        if n % 2 == 0:
            axis = x_axis
            x_axis = y_axis
            y_axis = axis


    groups = km.find_best_groups(karnaugh_map)
    original_colors, colors = km.get_colors(karnaugh_map, groups)

    img_obj = images.MapImage(karnaugh_map, variables, groups, original_colors, x_axis, y_axis)
    img = img_obj.get_image()
    img.save("../pythonProject/static/Images/map_image.png")

    result_expression = km.get_minimized_expression(groups, x_axis, y_axis, variables)
    best_groups_exp = result_expression.split(' + ')

    return render_template('karnaugh_map_result.html', n=n, karnaugh_map=karnaugh_map,
                           x_axis=x_axis, y_axis=y_axis, variables=variables,
                           colors = colors, groups = groups, best_groups_exp = best_groups_exp, result_expression = result_expression)


if __name__ == '__main__':
    app.run(debug=False)
