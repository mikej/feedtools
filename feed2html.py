import feeds

def simple_format_link(entry):
    return "<a href=\"%s\">%s</a>" % (entry.link, entry.title)

def get_feed_html(feed_url, n = 5, pattern = None, list_css_class = "feed-default", link_formatter = simple_format_link):
    f = feeds.Feeds()
    html = '<ul class="feed-entries %s">\n' % list_css_class
    for e in f.get_recent(f._get_feed_id(feed_url, False), n, pattern):
        html = html + ("    <li>%s</li>\n" % link_formatter(e))
    f.close()
    html = html + "</ul>"
    return html

if __name__ == '__main__':
    import sys
    print get_feed_html(sys.argv[1])
