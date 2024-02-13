from flask import Flask, render_template,request
from markupsafe import escape
from vsearch import search4letters
app = Flask(__name__)

def log_request(req:'current flask request',res:str)->None:
    with open('vsearch.log','a') as log:
        print(req.form,file=log)
        print(req.remote_addr,file=log)
        print(req.user_agent,file=log)
        print(res,file=log)


@app.route('/')
@app.route('/entry')
def message() -> 'html':
    return render_template('entry.html',the_title='here we do things!')

@app.route('/search4',methods=['POST'])
def search()-> 'html':
    phrase = request.form['phrase']
    letters = request.form['letters']
    results = str(search4letters(phrase,letters))
    footer = 'footer here'
    log_request(request, results)
    return render_template('results.html',the_phrase=phrase,
                           the_letters=letters,the_results=results,
                           the_title = 'here are your results nerd!',
                           the_footer = footer)

@app.route('/viewlog')
def showlogs() -> str:
    with open('vsearch.log') as log:
        contents = log.read()
    return escape(contents)


if __name__ == '__main__':
    app.run(debug=True)
