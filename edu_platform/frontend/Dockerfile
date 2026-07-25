# Frontend Dockerfile (Nginx Alpine)
FROM nginx:alpine

# Custom Nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Static files
COPY . /usr/share/nginx/html

EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"]
