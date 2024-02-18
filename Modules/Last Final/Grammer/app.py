from flask import Flask, render_template, request
import language_tool_python

app = Flask(__name__)

def grammar_check(text):
    tool = language_tool_python.LanguageTool('en-US')
    matches = tool.check(text)

    results = []
    for match in matches:
        result = {
            "Error": match.ruleId,
            "Message": match.message,
            "Suggestions": match.replacements
        }
        results.append(result)

    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_grammar', methods=['POST'])
def check_grammar():
    if request.method == 'POST':
        paragraph_input = request.form['paragraphInput']
        results = grammar_check(paragraph_input)

        return render_template('result.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
