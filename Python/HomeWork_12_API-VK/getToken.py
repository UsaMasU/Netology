from urllib.parse import urlencode

APP_ID = 6775694
AUTH_URL = 'https://oauth.vk.com/authorize?'

auth_data = {
    'client_id': APP_ID,
    'display': 'page',
    'redirect_uri': 'https://oauth.vk.com/blank.html',
    'response_type': 'token',
    'scope': 'friends,status',
    'v': '5.52'
}

#print(urlencode(auth_data))
print(AUTH_URL + urlencode(auth_data))

#token = '878ad39f8ea0555a5aab43e165e1676f2fc9daf74a0e365916e0d6593bdad51f9dc8adc20d551f90d8b52'
#token = '4c79e49b6b6a1f3dd441d29270b1284908c8f7122658b40d9b932c75d6c44a7fe4f5c3925d7bfbaf24b84'
#token = '4e06e638afb7e977427901cbd33bca24aebc82ecd7c1df5928aa691539f23006d6396485abf9ff6f6a46f'
#token = '26a99f6746dcf526520d7c440125bab2f8754616108153d0bd01cb81e33846156a5174613aa1b0b04aa7b'
#token = '8dc0f86a6cbd06c479e4d3c5f01bec52e8e6b05fed859c95e6c46fce8b56abd99ef02dcadca4713744d1b'
token = 'c2798ba0462903dff1c1f1a3ca833f5fb058f7af8e30a87e75f33d311e4362bc16ebfa83b7f41fe91666c'