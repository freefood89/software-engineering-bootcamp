# Part B

The objective of Part A isL

- Implement an unauthenticated API in AWS using chalice
- Implement a UI button that triggers an API call

## Setup

1. Install chalice cli
2. Use chalice to create a new project using their walkthrough

`chalice new-project backend`

3. Run your API locally with `chalice local`

4. Set your `AWS_PROFILE` and deploy the backend!

`cd backend`
`chalice deploy`

Take note of the output produced when deploying. It should look something like the following:

```
Creating deployment package.
Reusing existing deployment package.
Updating policy for IAM role: backend-dev
Updating lambda function: backend-dev
Updating lambda function: backend-dev-auth
Updating rest API
Resources deployed:
  - Lambda ARN: arn:aws:lambda:us-east-1:000000000000:function:backend-dev
  - Lambda ARN: arn:aws:lambda:us-east-1:000000000000:function:backend-dev-auth
  - Rest API URL: https://kbpvpsxs50.execute-api.us-east-1.amazonaws.com/api/
```

The Rest API URL provided at the bottom will be used to configure your frontend code later.

# Instructions

Much of the work here will be around building a client for the Frontend that can hit the serverless backend. Because it's pretty slow to update CloudFront. It may be a good idea to get everything working locally.

1. Build and deploy an API endpoint (for example, GET /gg) that returns a message:

`{ "message": "gg" }`

**Make sure to read up on how to set up CORS** because your backend and frontend will be served from different domains.

2. Create a `.env` file configuring React to use the API URL like the following:

`REACT_APP_BACKEND_DOMAIN=https://kbpvpsxs50.execute-api.us-east-1.amazonaws.com`

Of course, you should use whatever url was provided when deploying the API.

3. Create a basic API client in javascript for your frontend to use. Use the following as a template:

```javascript
import axios from 'axios'

class Client {
  constructor() {
     this._client = axios.create({
      baseURL: `${process.env.REACT_APP_BACKEND_DOMAIN}/api/`,
      timeout: 1000,
    })
  }

  getGg() {
    return this._client.get('/gg')
  }

  // TODO - don't worry about this part yet...
  // createSession(code) {
  //   return axios.get(`${process.env.REACT_APP_BACKEND_DOMAIN}/api/authorize?code=${code}`)
  //     .then(response => {
  //       this._client = axios.create({
  //         baseURL: `${process.env.REACT_APP_BACKEND_DOMAIN}/api/`,
  //         timeout: 1000,
  //         headers: {'Authorization': `${response.data.id_token}`}
  //       })
  //     })
  //     .catch(error => {
  //       if (error.response) {
  //         console.error(`Login Failed: ${error.response.status}`)
  //       } else {
  //         console.error(error)
  //       }
  //     })
  // }
}
```

4. Hook the client up using a React context provider so that the client is instantiated only on page loads and it can be injected using a context consumer. In this step the `this._client` is the only thing that's persisted, but eventually we will persist session.

5. Create a button, which will trigger the api call on click and display the response message in the console, DOM, or in an alert.

6. Deploy the frontend! You may need to perform a cache invalidation on Cloudfront for `index.html` if your frontend is not updating. 

Since webpack will create unique filenames for your JS bundle, you only need to update the html file that references those bundles for Cloudfront to get your updates.