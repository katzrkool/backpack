import dominate
from dominate.tags import *
from dominate.util import raw

def genHTML(data, urlRoot):
    doc = dominate.document('Grades')

    with doc.head:
        link(rel='stylesheet', href='{}static/style.css'.format(urlRoot), type='text/css')

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
                                        td(x['name'])
                                        td(x['score'])
                            with tfoot():
                                if 'analytics' in i:
                                    with tr(colspan=2):
                                        td('Disclaimer: If your teacher uses weighted grades, all of the analytics below are invalid', colspan=2, _class='disclaimer')
                                    for x in i['analytics']:
                                        with tr(colspan=2):
                                            td(i['analytics'][x], colspan=2, _class=x)

        footer(raw('<p>Arrows made by <a href="https://fontawesome.com">Font Awesome</a>.\n<a href="https://fontawesome.com/license/free">License</a>. No changes to images were made. <a href="faq">Information/FAQ</a>'))
        script(type='text/javascript', src='{}static/grades.js'.format(urlRoot))

    return doc.render()
