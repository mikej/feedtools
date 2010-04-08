import feedhtml

def format_so_question_link(entry):
    SO_PREFIX = "Answer by mikej for "
    if entry.title.startswith(SO_PREFIX):
        title = entry.title[len(SO_PREFIX):]
    else:
        title = entry.title
    return '<a href="%s">%s</a>' % (entry.link, title)

print feedhtml.get_feed_html('so.xml', list_css_class = "so-answers", link_formatter = format_so_question_link)
