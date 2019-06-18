# Use an official Python runtime as a parent image
FROM nginx 

COPY default.conf /etc/nginx/conf.d/default.conf

ADD dist /usr/share/nginx/html

CMD ["nginx", "-g", "daemon off;"]

