# encoding: utf-8

from lxml.html import tostring


def extract_tail(node):
    return node.tail.strip()


def extract_inner_html(node):
    node.tag = 'div'
    content = tostring(node)
    content = content.split('<div>')[1].split('</div>')[0]
    return content


def extract_integer(value):
    return value.split('(')[1].split('B')[0].strip()


def extract_datetime(value):
    return value.split('GMT')[0].strip()
