#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2014 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Reference command-line example for Google Analytics Management API v3.

This application demonstrates how to use the python client library to access
all the pieces of data returned by the Google Analytics Management API v3.

The application manages autorization by saving an OAuth2.0 token in a local
file and reusing the token for subsequent requests. It then traverses the
Google Analytics Management hiearchy. It first retrieves and prints all the
authorized user's accounts, next it prints all the web properties for the
first account, then all the profiles for the first web property and finally
all the goals for the first profile. The sample then prints all the
user's advanced segments.


Before You Begin:

Update the client_secrets.json file

  You must update the clients_secrets.json file with a client id, client
  secret, and the redirect uri. You get these values by creating a new project
  in the Google APIs console and registering for OAuth2.0 for installed
  applications: https://code.google.com/apis/console

  Learn more about registering your analytics application here:
  https://developers.google.com/analytics/devguides/config/mgmt/v3/mgmtAuthorization

Sample Usage:

  $ python management_v3_reference.py

Also you can also get help on all the command-line flags the program
understands by running:

  $ python management_v3_reference.py --help
"""
from __future__ import print_function

__author__ = 'api.nickm@gmail.com (Nick Mihailovski)'

import argparse
import sys

from googleapiclient.errors import HttpError
from googleapiclient import sample_tools
from oauth2client.client import AccessTokenRefreshError


def main(argv):
  # Authenticate and construct service.
  service, flags = sample_tools.init(
      argv, 'analytics', 'v3', __doc__, __file__,
      scope='https://www.googleapis.com/auth/analytics.readonly')

  # Traverse the Management hiearchy and print results or handle errors.
  try:
    traverse_hiearchy(service)

  except TypeError as error:
    # Handle errors in constructing a query.
    print(f'There was an error in constructing your query : {error}')

  except HttpError as error:
    # Handle API errors.
    print(
        f'Arg, there was an API error : {error.resp.status} : {error._get_reason()}'
    )

  except AccessTokenRefreshError:
    print ('The credentials have been revoked or expired, please re-run'
           'the application to re-authorize')


def traverse_hiearchy(service):
  """Traverses the management API hiearchy and prints results.

  This retrieves and prints the authorized user's accounts. It then
  retrieves and prints all the web properties for the first account,
  retrieves and prints all the profiles for the first web property,
  and retrieves and prints all the goals for the first profile.

  Args:
    service: The service object built by the Google API Python client library.

  Raises:
    HttpError: If an error occurred when accessing the API.
    AccessTokenRefreshError: If the current token was invalid.
  """

  accounts = service.management().accounts().list().execute()
  print_accounts(accounts)

  if accounts.get('items'):
    firstAccountId = accounts.get('items')[0].get('id')
    webproperties = service.management().webproperties().list(
        accountId=firstAccountId).execute()

    print_webproperties(webproperties)

    if webproperties.get('items'):
      firstWebpropertyId = webproperties.get('items')[0].get('id')
      profiles = service.management().profiles().list(
          accountId=firstAccountId,
          webPropertyId=firstWebpropertyId).execute()

      print_profiles(profiles)

      if profiles.get('items'):
        firstProfileId = profiles.get('items')[0].get('id')
        goals = service.management().goals().list(
            accountId=firstAccountId,
            webPropertyId=firstWebpropertyId,
            profileId=firstProfileId).execute()

        print_goals(goals)

  print_segments(service.management().segments().list().execute())


def print_accounts(accounts_response):
  """Prints all the account info in the Accounts Collection.

  Args:
    accounts_response: The response object returned from querying the Accounts
        collection.
  """

  print('------ Account Collection -------')
  print_pagination_info(accounts_response)
  print()

  for account in accounts_response.get('items', []):
    print(f"Account ID      = {account.get('id')}")
    print(f"Kind            = {account.get('kind')}")
    print(f"Self Link       = {account.get('selfLink')}")
    print(f"Account Name    = {account.get('name')}")
    print(f"Created         = {account.get('created')}")
    print(f"Updated         = {account.get('updated')}")

    child_link = account.get('childLink')
    print(f"Child link href = {child_link.get('href')}")
    print(f"Child link type = {child_link.get('type')}")
    print()

  if not accounts_response.get('items'):
    print('No accounts found.\n')


def print_webproperties(webproperties_response):
  """Prints all the web property info in the WebProperties collection.

  Args:
    webproperties_response: The response object returned from querying the
        Webproperties collection.
  """

  print('------ Web Properties Collection -------')
  print_pagination_info(webproperties_response)
  print()

  for webproperty in webproperties_response.get('items', []):
    print(f"Kind               = {webproperty.get('kind')}")
    print(f"Account ID         = {webproperty.get('accountId')}")
    print(f"Web Property ID    = {webproperty.get('id')}")
    print(f"Internal Web Property ID = {webproperty.get('internalWebPropertyId')}")

    print(f"Website URL        = {webproperty.get('websiteUrl')}")
    print(f"Created            = {webproperty.get('created')}")
    print(f"Updated            = {webproperty.get('updated')}")

    print(f"Self Link          = {webproperty.get('selfLink')}")
    parent_link = webproperty.get('parentLink')
    print(f"Parent link href   = {parent_link.get('href')}")
    print(f"Parent link type   = {parent_link.get('type')}")
    child_link = webproperty.get('childLink')
    print(f"Child link href    = {child_link.get('href')}")
    print(f"Child link type    = {child_link.get('type')}")
    print()

  if not webproperties_response.get('items'):
    print('No webproperties found.\n')


def print_profiles(profiles_response):
  """Prints all the profile info in the Profiles Collection.

  Args:
    profiles_response: The response object returned from querying the
        Profiles collection.
  """

  print('------ Profiles Collection -------')
  print_pagination_info(profiles_response)
  print()

  for profile in profiles_response.get('items', []):
    print(f"Kind                      = {profile.get('kind')}")
    print(f"Account ID                = {profile.get('accountId')}")
    print(f"Web Property ID           = {profile.get('webPropertyId')}")
    print(f"Internal Web Property ID = {profile.get('internalWebPropertyId')}")
    print(f"Profile ID                = {profile.get('id')}")
    print(f"Profile Name              = {profile.get('name')}")

    print(f"Currency         = {profile.get('currency')}")
    print(f"Timezone         = {profile.get('timezone')}")
    print(f"Default Page     = {profile.get('defaultPage')}")

    print(
        f"Exclude Query Parameters        = {profile.get('excludeQueryParameters')}"
    )
    print(
        f"Site Search Category Parameters = {profile.get('siteSearchCategoryParameters')}"
    )
    print(
        f"Site Search Query Parameters    = {profile.get('siteSearchQueryParameters')}"
    )

    print(f"Created          = {profile.get('created')}")
    print(f"Updated          = {profile.get('updated')}")

    print(f"Self Link        = {profile.get('selfLink')}")
    parent_link = profile.get('parentLink')
    print(f"Parent link href = {parent_link.get('href')}")
    print(f"Parent link type = {parent_link.get('type')}")
    child_link = profile.get('childLink')
    print(f"Child link href  = {child_link.get('href')}")
    print(f"Child link type  = {child_link.get('type')}")
    print()

  if not profiles_response.get('items'):
    print('No profiles found.\n')


def print_goals(goals_response):
  """Prints all the goal info in the Goals collection.

  Args:
    goals_response: The response object returned from querying the Goals
        collection
  """

  print('------ Goals Collection -------')
  print_pagination_info(goals_response)
  print()

  for goal in goals_response.get('items', []):
    print(f"Goal ID     = {goal.get('id')}")
    print(f"Kind        = {goal.get('kind')}")
    print(f"Self Link        = {goal.get('selfLink')}")

    print(f"Account ID               = {goal.get('accountId')}")
    print(f"Web Property ID          = {goal.get('webPropertyId')}")
    print(f"Internal Web Property ID = {goal.get('internalWebPropertyId')}")
    print(f"Profile ID               = {goal.get('profileId')}")

    print(f"Goal Name   = {goal.get('name')}")
    print(f"Goal Value  = {goal.get('value')}")
    print(f"Goal Active = {goal.get('active')}")
    print(f"Goal Type   = {goal.get('type')}")

    print(f"Created     = {goal.get('created')}")
    print(f"Updated     = {goal.get('updated')}")

    parent_link = goal.get('parentLink')
    print(f"Parent link href = {parent_link.get('href')}")
    print(f"Parent link type = {parent_link.get('type')}")

    # Print the goal details depending on the type of goal.
    if goal.get('urlDestinationDetails'):
      print_url_destination_goal_details(
          goal.get('urlDestinationDetails'))

    elif goal.get('visitTimeOnSiteDetails'):
      print_visit_time_on_site_goal_details(
          goal.get('visitTimeOnSiteDetails'))

    elif goal.get('visitNumPagesDetails'):
      print_visit_num_pages_goal_details(
          goal.get('visitNumPagesDetails'))

    elif goal.get('eventDetails'):
      print_event_goal_details(goal.get('eventDetails'))

    print()

  if not goals_response.get('items'):
    print('No goals found.\n')


def print_url_destination_goal_details(goal_details):
  """Prints all the URL Destination goal type info.

  Args:
    goal_details: The details portion of the goal response.
  """

  print('------ Url Destination Goal -------')
  print(f"Goal URL            = {goal_details.get('url')}")
  print(f"Case Sensitive      = {goal_details.get('caseSensitive')}")
  print(f"Match Type          = {goal_details.get('matchType')}")
  print(f"First Step Required = {goal_details.get('firstStepRequired')}")

  print('------ Url Destination Goal Steps -------')
  for goal_step in goal_details.get('steps', []):
    print(f"Step Number  = {goal_step.get('number')}")
    print(f"Step Name    = {goal_step.get('name')}")
    print(f"Step URL     = {goal_step.get('url')}")

  if not goal_details.get('steps'):
    print('No Steps Configured')


def print_visit_time_on_site_goal_details(goal_details):
  """Prints all the Visit Time On Site goal type info.

  Args:
    goal_details: The details portion of the goal response.
  """

  print('------ Visit Time On Site Goal -------')
  print(f"Comparison Type  = {goal_details.get('comparisonType')}")
  print(f"comparison Value = {goal_details.get('comparisonValue')}")


def print_visit_num_pages_goal_details(goal_details):
  """Prints all the Visit Num Pages goal type info.

  Args:
    goal_details: The details portion of the goal response.
  """

  print('------ Visit Num Pages Goal -------')
  print(f"Comparison Type  = {goal_details.get('comparisonType')}")
  print(f"comparison Value = {goal_details.get('comparisonValue')}")


def print_event_goal_details(goal_details):
  """Prints all the Event goal type info.

  Args:
    goal_details: The details portion of the goal response.
  """

  print('------ Event Goal -------')
  print(f"Use Event Value  = {goal_details.get('useEventValue')}")

  for event_condition in goal_details.get('eventConditions', []):
    event_type = event_condition.get('type')
    print(f'Type             = {event_type}')

    if event_type in ('CATEGORY', 'ACTION', 'LABEL'):
      print(f"Match Type       = {event_condition.get('matchType')}")
      print(f"Expression       = {event_condition.get('expression')}")
    else:  # VALUE type.
      print(f"Comparison Type  = {event_condition.get('comparisonType')}")
      print(f"Comparison Value = {event_condition.get('comparisonValue')}")


def print_segments(segments_response):
  """Prints all the segment info in the Segments collection.

  Args:
    segments_response: The response object returned from querying the
        Segments collection.
  """

  print('------ Segments Collection -------')
  print_pagination_info(segments_response)
  print()

  for segment in segments_response.get('items', []):
    print(f"Segment ID = {segment.get('id')}")
    print(f"Kind       = {segment.get('kind')}")
    print(f"Self Link  = {segment.get('selfLink')}")
    print(f"Name       = {segment.get('name')}")
    print(f"Definition = {segment.get('definition')}")
    print(f"Created    = {segment.get('created')}")
    print(f"Updated    = {segment.get('updated')}")
    print()


def print_pagination_info(management_response):
  """Prints common pagination details.

  Args:
    management_response: The common reponse object for each collection in the
        Management API.
  """

  print(f"Items per page = {management_response.get('itemsPerPage')}")
  print(f"Total Results  = {management_response.get('totalResults')}")
  print(f"Start Index    = {management_response.get('startIndex')}")

  # These only have values if other result pages exist.
  if management_response.get('previousLink'):
    print(f"Previous Link  = {management_response.get('previousLink')}")
  if management_response.get('nextLink'):
    print(f"Next Link      = {management_response.get('nextLink')}")


if __name__ == '__main__':
  main(sys.argv)

