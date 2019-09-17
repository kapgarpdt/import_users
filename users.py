
#!/usr/bin/env python
#
# Copyright (c) 2016, PagerDuty, Inc. <info@pagerduty.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of PagerDuty Inc nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL PAGERDUTY INC BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import requests
import json
#import csv
import pandas


# Update to match your API key
API_KEY = 'put your key here'
PD_EMAIL = 'email@adobe.com'
ID = 'none'
TEAMID = 'none'

df = pandas.read_csv('users.csv')
#NAME = (df["name"])[0]
#print(NAME)
for idx, row in df.iterrows():
	# Update to match your PagerDuty email address
	NAME = df['name'][idx]
	print(NAME)
	EMAIL = df['email'][idx]
	ROLE = df['role'][idx]  # Can be one of admin, user, limited_user, read_only_user  # NOQA
	def create_user():
		url = 'https://api.pagerduty.com/users'
		#print(url)
		headers = {
			'Accept': 'application/vnd.pagerduty+json;version=2',
			'Authorization': 'Token token={token}'.format(token=API_KEY),
			'Content-type': 'application/json',
			'From': PD_EMAIL
		}
		payload = {
			'user': {
				'type': 'user',
				'name': NAME,
				'email': EMAIL,
				'role': ROLE
			}
	}
		r = requests.post(url, headers=headers, data=json.dumps(payload))
		#print('Status Code: {code}'.format(code=r.status_code))
		data = r.json()
		#print(data.keys())
		global ID
		ID = data[u'user'][u'id']
		#print(ID)
	if __name__ == '__main__':
		create_user()
	# Update to match your chosen parameters
	TYPE = 'phone_contact_method'  # Can be one of email_contact_method, sms_contact_method, phone_contact_method, or push_notification_contact_method  # NOQA
	ADDRESS = str(df['phonenumber'][idx])
	LABEL = 'Work'
	def create_user_contact_method():
		url = 'https://api.pagerduty.com/users/{id}/contact_methods'.format(id=ID)
		#print(url)
		headers = {
			'Accept': 'application/vnd.pagerduty+json;version=2',
			'Authorization': 'Token token={token}'.format(token=API_KEY),
			'Content-type': 'application/json'
		}
		payload = {
			'contact_method': {
				'type': TYPE,
				'address': ADDRESS,
				'label': LABEL
			}
		}
		r = requests.post(url, headers=headers, data=json.dumps(payload))
		#print('Status Code: {code}'.format(code=r.status_code))
		#print(r.json())
	if __name__ == '__main__':
		create_user_contact_method()
	def get_team_id_method():
		TEAMS = df['teams'][idx]
		TEAMSA = TEAMS.split(';')
		print(TEAMSA)
		for item in TEAMSA:
			url = 'https://api.pagerduty.com/teams?query={team}'.format(team=item)
			#print(url)
			headers = {
				'Accept': 'application/vnd.pagerduty+json;version=2',
				'Authorization': 'Token token={token}'.format(token=API_KEY),
				'Content-type': 'application/json'
			}
			r = requests.get(url, headers=headers)
			#print('Status Code: {code}'.format(code=r.status_code))
			data = r.json()
			#print(data)
			global TEAMID
			TEAMID = data[u'teams'][0][u'id']
			#print(TEAMID)
			def add_user_to_teams_method():
				url = 'https://api.pagerduty.com/teams/{teamid}/users/{user_id}'.format(teamid=TEAMID, user_id=ID)
				print(url)
				headers = {
					'Accept': 'application/vnd.pagerduty+json;version=2',
					'Authorization': 'Token token={token}'.format(token=API_KEY),
					'Content-type': 'application/json'
				}
				payload = {
					"role": "responder"
				}
				r = requests.put(url, headers=headers, data=json.dumps(payload))
				print('Status Code: {code}'.format(code=r.status_code))
				#print(r.json())
			if __name__ == '__main__':
				add_user_to_teams_method()
	if __name__ == '__main__':
		get_team_id_method()