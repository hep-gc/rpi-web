import cgi
import logging

class HtmlUtils():
    """
    Very simple class to create simple html pages to return to the client.
    Here we chose to implement it as opposed to adding a dependency to a
    library or framework.
    """
    def dictToPage(self, d, title=''):
        """
        Renders a dictionnary as a table in a HTML page.
        """
        return '<html><head><title>%s</title></head><body>%s</body></html>' % (title, self.dictToTable(d))
    
        
    def dictToTable(self, d):
        """
        Renders a dictionary as a HTML <table> element.
        Note that this method is recursive and will also render sub-dictionnaries 
        as HTML table elements.
        """
        if not isinstance(d, dict):
            return cgi.escape(str(d))
        else:
            html = '<table>'
            for key in d.keys():
                html += '<tr><th align=right>%s:</th><td>%s</td></tr>' % (cgi.escape(key), self.dictToTable(d[key]))
            html += '</table>'
            return html

