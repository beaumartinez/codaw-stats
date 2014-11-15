#! /usr/bin/env python

from argparse import ArgumentParser
import json
import pprint

import requests


def codaw(email, password, network):
    # Normal form data doesn't work, it has to be JSON
    data = {
        'email': email,
        'password': password,
    }
    data = json.dumps(data)

    login_response = requests.post('https://ec2-api.prod.beachheadstudio.com/aw/si/login', data=data, headers={
        'bh-country-code': 'US',
        'bh-lang': 'en',
        'bh-client-os': 'android',
        'Content-Type': 'application/json'
    })
    user = login_response.json()

    user_id = user['unoId']

    # The cookies are in a weird format so requests doesn't parse them all; _rest contains the token so we fetch that
    cookies = tuple(login_response.cookies)[0]._rest

    stats_response = requests.get('https://ec2-api.prod.beachheadstudio.com/aw/user/{}/stats'.format(user_id), cookies=cookies, headers={
        'bh-country-code': 'US',
        'bh-lang': 'en',
        'bh-client-os': 'android',
        'bh-network': network,
    })
    stats = stats_response.json()

    pprint.pprint(stats)
    print 'https://ec2-api.prod.beachheadstudio.com/aw/user/{}/selfie?network=psn'.format(user_id)


if __name__ == '__main__':
    parser = ArgumentParser(description='Fetch your COD AW stats, from the same service the mobile apps use.')
    parser.add_argument('email', help='Email')
    parser.add_argument('password', help='Password')
    parser.add_argument('network', choices=('psn', 'uno', 'xbl'), help='Network (PlayStation, Steam, or Xbox)')

    args = parser.parse_args()

    codaw(args.email, args.password, args.network)
