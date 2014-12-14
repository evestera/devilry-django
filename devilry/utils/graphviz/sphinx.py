def indent_dotcode(dotcode, indent):
    return '\n'.join(['%s%s' % (indent, line)
        for line in dotcode.split('\n')])

def sphinx_format(dotcode):
    dotcode = indent_dotcode(dotcode, '    ')
    warning_comment = '.. Autogenerated graphviz code. Do not edit manually.'
    dotcode = "%s\n\n.. graphviz::\n\n%s" % (warning_comment, dotcode)
    return dotcode