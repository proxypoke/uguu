# uguu - generate flexget config files.
#
# Author: slowpoke <mail+git@slowpoke.io>
#
# This program is free software under the non-terms
# of the Anti-License. Do whatever the fuck you want.
#
# Github: https://www.github.com/proxypoke/uguu
# (Shortlink: https://git.io/uguu)
#
# Format options for vim. Please adhere to them.
# vim: set et ts=4 sw=4 tw=80:

from distutils.core import setup

setup(name='uguu',
      version='1.1.0',
      author='slowpoke',
      author_email='mail+git@slowpoke.io',
      url='https://github.com/proxypoke/uguu',
      description='generate Flexget config files',
      requires=['pyyaml'],
      scripts=['uguu'],
      data_files=[
          ('/usr/share/man/man1', ['man/uguu.1.gz']),
          ('/usr/share/doc/uguu', ['README.asciidoc', 'uguu_conf.yml']),
      ],
      classifiers=[
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'License :: Freely Distributable',
          'Operating System :: POSIX',
          'Topic :: Communications :: File Sharing',
          'Development Status :: 4 - Beta',
      ],
      long_description='''
        uguu is a tool to generate flexget configuration
        files, which aren't well suited to some use cases, one being having a
        separate feed for every
        series, which is important for fast moving RSS feeds such as
        Nyaatorrents, or simply if one likes
        to download a series without batches using flexget.
        '''
      )
