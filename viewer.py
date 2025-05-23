import json

parent = 'RickG/'
input_file = f'{parent}arc-agi_test_challenges.json'
output_file = f'{parent}submission.json'
html_file = 'RickG.html'

colors = [
    '#000000',
    '#1E93FF',
    '#F93C31',
    '#4FCC30',
    '#FFDC00',
    '#999999',
    '#E53AA3',
    '#FF851B',
    '#87D8F1',
    '#921231'
]

# Open the files
with open(input_file, 'r') as f:
    inputs = json.load(f)
with open(output_file, 'r') as f:
    outputs = json.load(f)

# Start
html = '<!DOCTYPE html><head><meta charset="UTF-8"/><title>ARC-PRIZE-2</title></head>'
html = f'{html}<body style="display:flex;flex-wrap:wrap;gap:30px;justify-content:center;">\n'

# Matrix to HTML
def matrixHTML(mtx, size=20):
    w, h = len(mtx[0]), len(mtx)
    html = f'<div style="display:flex;flex-wrap:wrap;width:{w*size}px;height:{h*size}px">\n'
    for row in mtx:
        for col in row:
            color = colors[col]
            html = f'{html}<div style="width:{size}px;height:{size}px;background-color:{color}"></div>\n'
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
    html = f'{html}<div style="border:1px solid #000;padding:10px;">\n'
    html = f'{html}<p><b>Puzzle #{puzzle_id}</b></p>\n'
    # Train
    html = f'{html}<p>Train:</p>\n'
    for train in puzzle['train']:
        html = f'{html}<div style="display:flex;gap:10px;margin-bottom:10px;">\n'
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
            html = f'{html}<div style="display:flex;gap:10px;margin-bottom:10px;">\n'
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