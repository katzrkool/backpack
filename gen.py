import dominate
from dominate.tags import *

def genHTML(classes, grades):
    doc = dominate.document('Grades')

    with doc.head:
        link(rel='stylesheet', href='style.css', type='text/css')

    with doc:
        with div(id='main'):
            for i in range(0,len(classes)):
                with div(_class='surround'):
                    h1('{}: {}'.format(classes[i], grades[i]), _class='grade')
                    with div(_class='progress'):
                        div()
        script(type='text/javascript', src='grades.js')

    return doc.render()