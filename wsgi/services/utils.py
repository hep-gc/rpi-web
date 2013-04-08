import cgi

class HtmlUtils():
    """
    Very simple class to create simple html pages to return to the client.
    Here we chose to implement it as opposed to adding a dependency to a
    library or framework.
    """
    def dictToPage(self, d, title=''):
        return '<html><head><title>%s</title></head><body>%s</body></html>' % (title, self.dictToTable(d))
        
    def dictToTable(self, d):
        html = '<table>'
        for key in d.keys():
            html += '<tr><th align=right>%s:</th><td>%s</td></tr>' % (cgi.escape(key), cgi.escape(d[key]))
        html += '</table>'
        return html

