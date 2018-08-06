import dominate
from dominate.tags import *

def genHTML(data):
    doc = dominate.document('Grades')

    with doc.head:
        link(rel='stylesheet', href='style.css', type='text/css')

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

        script(type='text/javascript', src='grades.js')

    return doc.render()