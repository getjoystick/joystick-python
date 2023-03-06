# Redis cache

This is an example which uses `pip` to install the library and show
how with Joystick Python client you may flexibly configure your own cache provider

## How to run?

1.  Change working directory to this folder
2.  Run command:

```bash
docker-compose build && \
 JOYSTICK_API_KEY='TpVZbqcB4ZMIv5skGSQTUJ2mANVHeGHT' \
 JOYSTICK_CONFIG_ID='cid1' \
 docker-compose up --force-recreate --scale app=5
```

4.  It will build the simple infrastructure with:


    - Redis
    - Nginx as a load balancer
    - 5 instances of the app


## What can I see here?

Once you run the application Nginx will listen port `8000` and it can be accessible
via [http://127.0.0.1:8000/]. You can see that the response time for the first call is bigger then
for subsequent calls. The first request makes the API call to Joystick and the next ones are 
retrieved from Redis as a cache provider.

Also you may notice that `server_id` field changes for almost every call, that means that different 
instances of the same app are getting the information from shared cache, requiring only one instance 
to call the Joystick only once before being cached for all other instances.

If you wait for 10 seconds – you will that the next call will take more time. That is because we 
configured `cache_expiration_seconds` to 10 seconds.

You can use this version of the cache provider for your own needs as a template