import json

folder = 'RickG'
input_file = f'{folder}/arc-agi_test_challenges.json'
output_file = f'{folder}/submission.json'
html_file = f'{folder}.html'

colors = [
    [ 'black', '#000000' ],
    [ 'blue', '#1E93FF' ],
    [ 'red', '#F93C31' ],
    [ 'green', '#4FCC30' ],
    [ 'yellow', '#FFDC00' ],
    [ 'gray', '#999999' ],
    [ 'magenta', '#E53AA3' ],
    [ 'orange', '#FF851B' ],
    [ 'bluelight', '#87D8F1' ],
    [ 'maroon', '#921231' ]
]
cell_size = 20

# Open the files
with open(input_file, 'r') as f:
    inputs = json.load(f)
with open(output_file, 'r') as f:
    outputs = json.load(f)

# Start
html = '<!DOCTYPE html><head><meta charset="UTF-8"/><title>ARC-PRIZE-2</title>'
html = f'{html}<style>body{{display:flex;flex-wrap:wrap;gap:30px;justify-content:center;}}'
html = f'{html}.puzzle{{border:1px solid #000;padding:10px;}}\n'
html = f'{html}.puzzle>div{{display:flex;gap:10px;margin-bottom:10px;}}'
html = f'{html}.mtx{{display:flex;flex-wrap:wrap;}}\n.mtx>div{{width:{cell_size}px;height:{cell_size}px;}}\n'
for color in colors:
    html = f'{html}.mtx>.{color[0]}{{background-color:{color[1]};}}\n'
html = f'{html}</style></head><body>\n'

# Matrix to HTML
def matrixHTML(mtx):
    global cell_size
    if not len(mtx) or not len(mtx[0]):
        print('Err: Wrong Matrix')
        return '<div>(WRONG MATRIX)</div>'
    w, h = len(mtx[0]), len(mtx)
    html = f'<div style="width:{w*cell_size}px;height:{h*cell_size}px" class="mtx">\n'
    for row in mtx:
        for col in row:
            html = f'{html}<div class="{colors[col][0]}"></div>\n'
    html = f'{html}</div>'
    return html

# Treatment
puzzles_index = list(inputs.keys())
nb_tests = len(puzzles_index)
for i in range(0, nb_tests):
    print(f'{i} / {nb_tests}')
    if i > len(puzzles_index): break
    puzzle_id = puzzles_index[i]
    # Check the solution
    if not puzzle_id in outputs:
        print(f'Warn: Puzzle #{puzzle_id} has no solution.')
        continue
    # Get the puzzle and write it
    puzzle, solve = inputs[puzzle_id], outputs[puzzle_id]
    html = f'{html}<div class="puzzle">\n'
    html = f'{html}<p><b>Puzzle #{puzzle_id}</b></p>\n'
    # Train
    html = f'{html}<p>Train:</p>\n'
    for train in puzzle['train']:
        html = f'{html}<div>\n'
        html = f'{html}{matrixHTML(train["input"])}\n'
        html = f'{html}<div>-></div>\n'
        html = f'{html}{matrixHTML(train["output"])}\n'
        html = f'{html}</div>\n'
    # Test
    html = f'{html}<p>Test:</p>\n'
    for test in puzzle['test']:
        test_index = puzzle['test'].index(test)
        my_input = matrixHTML(test["input"])
        for attempt in range(1,3):
            html = f'{html}<p><b>attempt_{attempt}</b></p>'
            html = f'{html}<div>\n'
            html = f'{html}{my_input}\n'
            html = f'{html}<div>-></div>\n'
            html = f'{html}{matrixHTML(solve[test_index][f"attempt_{attempt}"])}\n'
            html = f'{html}</div>\n'
    html = f'{html}</div>\n'

# End
html = f'{html}</body></html>'

# Write HTML file
with open(html_file, 'w') as f:
    f.write(html)

print(f'Output: {html_file}')