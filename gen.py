import dominate
from dominate.tags import *
from dominate.util import raw

def genHTML(data):
    doc = dominate.document('Grades')

    with doc.head:
        link(rel='stylesheet', href='static/style.css', type='text/css')

    with doc:
        with div(id='main'):
            for i in data:
                with span(_class='surround'):
                    h1('{}: {}'.format(i['class'], i['grade']), _class='grade')
                    with span(_class='progress'):
                        with span():
                            span()
                    if len(i['assignments']) > 0:
                        with table(_class='assignments'):
                            with thead().add(tr()):
                                th('Assignment')
                                th('Score')
                            with tbody():
                                for x in i['assignments']:
                                    with tr():
                                        td(x)
                                        td(i['assignments'][x])
                            with tfoot().add(tr(colspan=2)):
                                if 'analytics' in i:
                                    for x in i['analytics']:
                                        td(i['analytics'][x], colspan=2)

        footer(raw('<p>Arrows made by <a href="https://fontawesome.com">Font Awesome</a>.\n<a href="https://fontawesome.com/license">License</a>. No changes to images were made.'))
        script(type='text/javascript', src='static/grades.js')

    return doc.render()