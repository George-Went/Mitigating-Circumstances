# OAuth

OAuth is about allowing other applications access to your own application, an example of this is the usage of OAuth to allow for the ability to sign into application using google sign in 

OAuth is about *authorisation* , not authentication.
Authorisation: Asking for permission to do stuff
Authentication: Proving that you are the correct person to do stuff 

OAuth does not pass authenticaion data between services, meanint that even if your using googles API to allow loggin in via Google accounts, google does not know the authenication data between youir website and the user. 

## How OAuth works 
There are 3 main users in an OAuth transaction: 
* user: John
* Consumer: Mitigating circumstances web app 
* Service: Google 

### Step 1 - The user shows intent 

> User: I would like to log in using my Google account 
> Consumer: Okay, let me ask google for permission

### Step 2 - The consumer gets permission

> Consumer: I have a user that wants to log in with a Google account 
> Service: Okay, Here is a *Token* and a *Secret* 

The secret is used to prevent a malicious site from forging a request to the consumer, so a fake site cant ask for a legitimate token, the token is used to show proof that the the site has a legitimate connection to the service (The mitigating circumstances web app is actually a app using google auth), attacks such as this are called *Cross-Site Request Forgery* (CSRF)

### Step 3 - The user is redirected to the service provider 

> Consumer: okay user, google wants approval from you so that my website can use the google account to log in, take this token with you so it know that i am the one asking for permission.
> [The site directs the user to google login]

### Step 4 - User gives permission 

> User: Google, can this site use my account to log in? 
> Service: Only if the site has a *Request Token*
> User: [User provides request token]
> Service: Ok - the consumer now has the ability to use your google account

### Step 5 - The consumer obtains a Access Token

> Consumer: can i trade this *request token* in, to allow the user to log in with google? 
> Service: okay - here is a *access token* and a *secret* 

### Step 6 - Consumer accesses protected resources 

> Consumer: Can this user log in with his google account, i have a access token
> Service: OK

Due to this process, the User never had to share his google login credentials with the mitigating circumstances website, only google. In its place, a series of tokens were used to provide authorisation. 

## Other Examples 
A Good analogy is the valet key to the car - when dropping off a car, a valet key allows a secondary user to start and move the car - but not open the boot.

This is similar to the usage of tokens - instead of the user passing their login data to the site, so that the site can log into google, the user logs into google, then provides a key (access token) to the site which it can then use to access *certian* resources. The site also needs to provide proof to google (request token) that the user is asking for google permission to use their google acocunt on this site. 

The seceret is used so that the user and the site can verrify themselves as legitimate, in the same way that the valet key is different for each car - other wise the valet could access multiple cars with the same key (token). 