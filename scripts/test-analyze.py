#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

'''
  Analyze tests xml output
  ------------------------

  :copyright (c) 2014 Xavier Bruhiere.
  :license: Apache 2.0, see LICENSE for more details.
'''


import xmltodict
from clint.textui import colored, indent, puts


def parse_tests(filereport='.test_report.xml'):
    doc = xmltodict.parse(open(filereport, 'r').read())
    overview = {
        'tests': int(doc['testsuite']['@tests']),
        'errors': int(doc['testsuite']['@errors']),
        'failures': int(doc['testsuite']['@failures']),
        'skips': int(doc['testsuite']['@skip']),
        }
    overview.update({'successes':
                    overview['tests'] - overview['errors']
                    - overview['skips'] - overview['failures']})
    return overview, doc['testsuite']['testcase']


def analyze_test(test):
    error = test.get('error')
    failure = test.get('failure')
    if error or failure:
        puts(colored.blue('\nPinned {}.{}'.format(
            test['@classname'], test['@name'])))
    if error:
        puts(colored.blue(
            ('{}\n\t{}\n'.format(error['@type'], error['@message']))))
    if failure:
        puts(colored.blue(
            ('{}\n\t{}\n'.format(failure['@type'], failure['@message']))))


if __name__ == '__main__':
    puts(colored.blue('Analyzing tests output ...'))
    overview, report = parse_tests()
    puts(colored.blue('\nHivy tests suite report'))
    with indent():
        puts(colored.green(
            '{} successful tests'.format(overview['successes'])))
        puts(colored.green(
            '{} skipped tests'.format(overview['skips'])))
        if overview['failures'] == 0:
            puts(colored.green(
                '{} failed tests'.format(overview['failures'])))
        else:
            puts(colored.red(
                '{} failed tests'.format(overview['failures'])))
        if overview['errors'] == 0:
            puts(colored.green(
                '{} crashed tests'.format(overview['errors'])))
        else:
            puts(colored.red(
                '{} crashed tests'.format(overview['errors'])))

    puts(colored.blue('\nScanning individual tests ...'))
    for test in report:
        analyze_test(test)
