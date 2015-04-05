#!/usr/bin/env python
# encoding: utf-8

from logging import basicConfig, CRITICAL

from grab.spider import Spider, Task
from grab.tools.structured import Structure as x

from models import database, Category, Torrent, Removed
import settings
import converters


class PirateBaySpider(Spider):
    def task_generator(self):
        for pk in xrange(settings.START_ID, settings.END_ID):
            if Torrent.filter(id=pk).exists():
                continue
            if Removed.filter(id=pk).exists():
                continue

            yield Task(url='https://thepiratebay.se/torrent/{}/'.format(pk),
                       name='page',
                       pk=pk)

    def task_page(self, grab, task):
        if grab.response.code != 200:
            with database.transaction():
                Removed.create(id=task.pk)
            return

        data = grab.doc.structure(
            '//*[@id="detailsframe"]',
            x(
                './*[@id="details"]',
                category='.//dt[.="Type:"]/following-sibling::dd/a/text()',
                size=('.//dt[.="Size:"]/following-sibling::dd/text()',
                      converters.extract_integer),
                created=('.//dt[.="Uploaded:"]/following-sibling::dd/text()',
                         converters.extract_datetime),
                hash=('.//dt[.="Info Hash:"]/following-sibling::dd',
                      converters.extract_tail),
            ),
            nfo=('//*[@class="nfo"]/pre', converters.extract_inner_html),
            magnet='//*[@class="download"]/a/@href',
            title='./*[@id="title"]/text()',
        )[0]
        data.update({
            'id': task.pk,
        })

        with database.transaction():
            category = Category.get_or_create(name=data.pop('category', ''))
            Torrent.create(category=category,
                           **data)


if __name__ == '__main__':
    basicConfig(level=CRITICAL)

    spider = PirateBaySpider(thread_number=24)
    spider.run()
