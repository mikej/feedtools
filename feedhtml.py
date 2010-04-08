import feeds

def simple_format_link(entry):
    return "<a href=\"%s\">%s</a>" % (entry.link, entry.title)

def get_feed_html(feed_url, n = 5, list_css_class = "feed-default", link_formatter = simple_format_link):
    f = feeds.Feeds()
    html = '<ul class="feed-entries %s">\n' % list_css_class
    for e in f.get_recent('so.xml', n, "Answer by%"):
        html = html + ("    <li>%s</li>\n" % link_formatter(e))
    f.close()
    html = html + "</ul>"
    return html

if __name__ == '__main__':
    import sys
    print get_feed_html(sys.argv[1])
