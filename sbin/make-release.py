#!/usr/bin/env python
import logging
import os
import re
import shutil
import sys
from argparse import ArgumentParser
from distutils.version import LooseVersion
from subprocess import check_output
from git import Repo


def print_output(output):
    print('\n'.join(output.decode().splitlines()))


def parse_arguments():
    p = ArgumentParser(
        description="Prepare or make release", )
    p.add_argument('action',
                   help='Version to release', )
    p.add_argument('type',
                   choices=['major', 'minor', 'bugfix'],
                   help='Type of change', )
    p.add_argument('--debug',
                   action='store_true',
                   help='Print debug messages', )
    p.add_argument('--dry-run',
                   action='store_true',
                   help='Print commands but do not execute', )
    p.add_argument('--repo',
                   choices=['pypi', 'testpypi'],
                   default='testpypi',
                   help='Show manual page', )
    p.add_argument('--man-page',
                   action='store_true',
                   help='Show manual page', )
    p.add_argument('--verbose',
                   action='store_true',
                   help='Print information messages', )
    p.add_argument('--version',
                   help='Override version', )
    args = p.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    elif args.verbose:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.ERROR)
    return args


def get_previous_release(repo):
    tags = [str(t) for t in repo.tags
            if t.tag and re.match('\d+\.\d+\.\d+$', str(t))]
    if tags:
        tags = sorted(tags, key=lambda x: LooseVersion(x))
        return tags[-1]
    return None


def find_issues(message):
    lines = message.splitlines()
    issues = []
    for line in lines:
        if re.match('^\s*([^\s]*)?\s*(#\d+)\s*(\w.*?)?\s*$', line):
            issues.append(line)
    return issues


def step_version(previous, step_type):
    s = {'major': 0, 'minor': 1, 'bugfix': 2}
    i = s[step_type]
    p = previous.split('.')
    p[i] = 1 + int(p[i])
    return '.'.join(str(e) for e in p)


if __name__ == '__main__':
    args = parse_arguments()

    # Crude release program
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dist_dir = os.path.join(root, 'dist')
    setup_file = os.path.join(root, 'setup.py')
    release_file = os.path.join(root, 'release.txt')
    message = []
    repo = Repo(root)

    try:
        working_tree = repo.working_tree_dir
    except AssertionError:
        print('No working tree. Unable to release.')
        exit(1)

    previous = get_previous_release(repo)

    if previous:
        version = step_version(previous, args.type)
    else:
        version = '0.1.0'

    if args.action == 'prepare':
        subjects = []
        issues = []
        messages_lines = []

        if previous:
            print('Previous: {}'.format(previous))
            # 1. Compare the SHA1 in the release info with HEAD
            for commit in repo.iter_commits('{}...HEAD'.format(previous)):
                subjects.append(commit.summary)
                issues.extend(find_issues(commit.message))

        with open(release_file, 'w') as fp:
            fp.write('Release {}\n\n'.format(version))
            for subject in subjects + issues:
                print('* {}'.format(subject))
                fp.write('* {}\n'.format(subject))
        print('Release information stored in {}. Edit the file and then'
              ' re-run with the "release" action to perform a release.'
              ''.format(release_file))

    elif args.action == 'release':

        if os.path.exists(release_file):
            with open(release_file) as fp:
                message = fp.read()

        print(message)

        ans = input('Continue? ').strip()

        if ans not in ['y', 'yes']:
            exit()

        if os.path.exists(dist_dir):
            if args.dry_run:
                print('rmtree {}'.format(dist_dir))
            else:
                shutil.rmtree(dist_dir)

        os.environ['ABADGE_RELEASE_VERSION'] = version
        build_command = ['python', setup_file, 'sdist', 'bdist_wheel']
        tag_command = ['git', 'tag', '-a', version, '-F', release_file]
        publish_command = ['git', 'push', '--tags', 'origin', version]
        deploy_command = 'twine upload dist/* -r {}'.format(args.repo)

        if args.dry_run:
            print(build_command)
            print(tag_command)
            print(publish_command)
            print(deploy_command)
        else:
            print('Building')
            print(' '.join(build_command))
            print_output(check_output(build_command))

            print('Creating tag')
            print(' '.join(tag_command))
            print_output(check_output(tag_command))

            print('Pushing tag')
            print(' '.join(publish_command))
            print_output(check_output(publish_command))

            print('Deploying to PYPI')
            print(publish_command)
            print_output(check_output(deploy_command))

    else:
        raise ValueError('{}: Error: unknown action. Valid are: prepare,'
                         ' release'.format(args.action))

    print('Done.')
