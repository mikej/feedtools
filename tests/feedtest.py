import feeds

f = feeds.Feeds()

print [e.link for e in f.get_recent('stackoverflow.xml')]

f.close()
