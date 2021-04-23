# sherlock

This is a DJango project.

## How-to

### Make your own route

1. Inside sherlock/views.py add your own method `def my_route(request, param)`
2. Inside sherlock/urls.py add your own url: `path('my_route/<int:param>/', views.my_route, name='my_route'),`
3. Now you can go to http://localhost:8000/my-route/1 and your route should be executed
